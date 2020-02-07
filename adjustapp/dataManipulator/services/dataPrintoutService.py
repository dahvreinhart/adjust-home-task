from dataManipulator.models import PerformanceMetricItem
from decimal import *


def getData(fieldsClause, filtersClause, groupByClause, orderByClause):
    """Simple DB access method to make the final query call"""
    rawQuery = buildRawQuery(
        fieldsClause,
        filtersClause,
        groupByClause,
        orderByClause
    )
    return PerformanceMetricItem.objects.raw(rawQuery)

def validateQueryParams(fields, filters, groupBy, orderBy):
    """
    Validation method to make sure there are no structural defects in the
    query parameters or invalid fields attempting to be utilized. Exceptions
    are raised on violations.
    """
    possibleFields = getAllFieldNamesList()

    # Ensure only correct fields are being selected
    if fields:
        for field in fields.split(','):
            if field not in possibleFields:
                raise Exception('INVALID FIELD NAME: {}'.format(field))

    # Ensure only correct fields are being used for groupings
    if groupBy:
        for field in groupBy.split(','):
            if field not in possibleFields:
                raise Exception('INVALID GROUPING FIELD NAME: {}'.format(field))

    # Ensure only correct fields are being filtered on
    if filters:
        separateFilters = filters.split(',')
        for singleFilter in separateFilters:
            filterPieces = singleFilter.split('|')
            if len(separateFilters) > 1 and len(filterPieces) not in [3, 4, 5]:
                # This filter must contain a 3-part condition expression
                # Optionally, it could also contain a 'NOT' operator and/or a logical operator 
                raise Exception('INVALID FILTER STRUCTURE: {}'.format(singleFilter))
            elif len(separateFilters) == 1 and len(filterPieces) not in [3, 4]:
                # This filter must contain a 3-part condition expression
                # Optionally, it could also contain a 'NOT' operator
                raise Exception('INVALID FILTER STRUCTURE: {}'.format(singleFilter))
    
    # Ensure only correct fields are being used to order and that ordering is properly structured
    if orderBy:
        orderingParams = orderBy.split(',')
        if len(orderingParams) != 2:
            raise Exception(
                'INVALID ORDERING STRUCTURE: ordering param must be in the format `orderby=<FIELDNAME>,<DIRECTION>`'
            )

        orderByField, orderByDirection = orderingParams
        if orderByField not in possibleFields:
            raise Exception('INVALID ORDERING FIELD NAME: {}'.format(orderByField))
        if orderByDirection.lower() not in ['asc', 'desc']:
            raise Exception('INVALID ORDERING DIRECTION: {}'.format(orderByDirection))

def parseFieldParams(fields, groupBy):
    """
    Build the query syntax to be used in the SELECT section of the eventual DB call.
    If no fields are defined, all fields will be shown by default.

    Field params must be in the format:
        fields=FIELD1,FIELD2, ...
    """
    # Not specifying any fields defaults to getting them all
    if not fields:
        fields = getAllFieldNamesList()
        fields = ','.join(fields)

    # If a grouping is defined, aggregate the necessary numerical fields
    if groupBy:
        groupingFields = groupBy.split(',')
        summableFieldsNoRounding = ['impressions', 'clicks', 'installs']
        summableFieldsWithRounding = ['spend', 'revenue']
        for field in fields.split(','):
            if field not in groupingFields:
                if field in summableFieldsNoRounding:
                    fields = fields.replace(field, 'SUM({}) AS {}'.format(field, field))
                elif field in summableFieldsWithRounding:
                    fields = fields.replace(field, 'ROUND(SUM({}), 2) AS {}'.format(field, field))
                elif field == 'cpi':
                    fields = fields.replace(field, 'ROUND(SUM(spend)/SUM(installs), 2) AS cpi')
            elif field == 'cpi':
                fields = fields.replace('cpi', 'ROUND(spend/installs, 2) AS cpi')
    elif 'cpi' in fields.split(','):
        fields = fields.replace('cpi', 'ROUND(spend/installs, 2) AS cpi')
  
    return fields

def parseFilterParams(filters):
    """
    Build the query syntax to be used in the WHERE section of the eventual DB call.

    Field params must be in the format:
        filters=NOT|field|arithmeticOperator|value|logicalOperator, ...

        Where the 'NOT' and 'logicalOperator' terms are optional
    """
    if not filters:
        return ''

    # Begin the clause
    filterClause = 'WHERE'

    separateFilters = filters.split(',')
    if len(separateFilters) == 1:
        # Only one filter is present
        filterPieces = separateFilters[0].split('|')
        if filterPieces[0].lower().startswith('not'):
            # Must be in the form <NOT> <FIELDNAME><ARITHMETICOPERATOR><VALUE>
            filterClause = '{} {} {}{}{}'.format(
                filterClause,
                filterPieces[0],
                filterPieces[1],
                filterPieces[2],
                filterPieces[3],
            )
        else:
            # Must be in the form <FIELDNAME><ARITHMETICOPERATOR><VALUE>
            filterClause = '{} {}{}{}'.format(
                filterClause,
                filterPieces[0],
                filterPieces[1],
                filterPieces[2],
            )
    else:
        # Multiple filters are present
        for separateFilter in separateFilters:
            filterPieces = separateFilter.split('|')
            if filterPieces[0].lower().startswith('not'):
                if len(filterPieces) == 4:
                    # Must be the final filter and in the form <NOT> <FIELDNAME><ARITHMETICOPERATOR><VALUE>
                    filterClause = '{} {} {}{}{}'.format(
                        filterClause,
                        filterPieces[0],
                        filterPieces[1],
                        filterPieces[2],
                        filterPieces[3],
                    )
                else:
                    # Must be in the form <NOT> <FIELDNAME><ARITHMETICOPERATOR><VALUE> <LOGICALOPERATOR>
                    filterClause = '{} {} {}{}{} {} '.format(
                        filterClause,
                        filterPieces[0],
                        filterPieces[1],
                        filterPieces[2],
                        filterPieces[3],
                        filterPieces[4],
                    )
            else:
                if len(filterPieces) == 3:
                    # Must be the final filter and in the form <FIELDNAME><ARITHMETICOPERATOR><VALUE>
                    filterClause = '{} {}{}{}'.format(
                        filterClause,
                        filterPieces[0],
                        filterPieces[1],
                        filterPieces[2]
                    )
                else:
                    # Must be in the form <FIELDNAME><ARITHMETICOPERATOR><VALUE> <LOGICALOPERATOR>
                    filterClause = '{} {}{}{} {}'.format(
                        filterClause,
                        filterPieces[0],
                        filterPieces[1],
                        filterPieces[2],
                        filterPieces[3],
                    )

    return filterClause

def parseGroupByParams(groupBy):
    """
    Build the query syntax to be used in the GROUP BY section of the eventual DB call.

    groupBy params must be in the format:
        groupBy=FIELD1,FIELD2, ...
    """
    return 'GROUP BY {}'.format(groupBy) if groupBy else ''

def parseOrderByParams(orderBy):
    """
    Build the query syntax to be used in the ORDER BY section of the eventual DB call.

    orderBy params must be in the format:
        orderBy=FIELDNAME,DIRECTION

        Where 'DIRECTION' is either 'ASC' or 'DESC'
    """
    return 'ORDER BY {}'.format(orderBy.replace(',', ' ')) if orderBy else ''

def buildRawQuery(fieldsClause, filtersClause, groupByClause, orderByClause):
    """
    Take the various computer and formatted query clauses and build the raw SQL
    query from them.
    """
    return '''
        SELECT
            id,{}
        FROM dataManipulator_performancemetricitem
        {}
        {}
        {}
    '''.format(fieldsClause, filtersClause, groupByClause, orderByClause)

def getFieldsToDisplay(fields):
    """
    Return the list of fields we want to display on the front end. If a list of
    fields has been defined, onyl show that list of fields. Otherwise, show all
    fields including calculated CPI.
    """
    if fields:
        return [field for field in fields.split(',') if field != 'id']
    else:
        return getAllFieldNamesList()

def getAllFieldNamesList():
    """Helper method to get all fields able to be manipulated."""
    fields = [field.name for field in PerformanceMetricItem._meta.fields if field.name != 'id']
    fields.append('cpi')
    return fields

