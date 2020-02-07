from django.shortcuts import render
from django.views.generic import TemplateView
from dataManipulator.services import dataPrintoutService
from dataManipulator.models import PerformanceMetricItem


class HomePageView(TemplateView):

    def get(self, request, **kwargs):
        """Simple homepage function"""
        return render(request, 'index.html', context=None)

class DataPrintout(TemplateView):

    def get(self, request, **kwargs):
        """
        Function for getting a manipulated set of data from local storage.
        Accepts any combination of fields, filters, groupings and orderings.
        For a list of the expected formats, see either the various parse functions
        in dataPrintoutService or the documentation contained in the project README.
        """
        # Strip the query params off the request object
        fields, filters, groupBy, orderBy = [request.GET.get(field, '') for field in ['fields', 'filters', 'groupby', 'orderby']]

        # Validate the incoming query params
        dataPrintoutService.validateQueryParams(fields, filters, groupBy, orderBy)

        # Parse query params into usable query syntax
        fieldsClause = dataPrintoutService.parseFieldParams(fields, groupBy)
        filtersClause = dataPrintoutService.parseFilterParams(filters)
        groupByClause = dataPrintoutService.parseGroupByParams(groupBy)
        orderByClause = dataPrintoutService.parseOrderByParams(orderBy)

        # Fetch the data using the dynamically built query
        data = dataPrintoutService.getData(
            fieldsClause,
            filtersClause,
            groupByClause,
            orderByClause,
        )

        # Calculate which fields we should display based on what was selected from the DB
        fieldsToDisplay = dataPrintoutService.getFieldsToDisplay(fields)

        # Send response to client
        # Records are converted to dicts for proper data access in template
        return render(
            request, 
            'dataPrintout.html', 
            context={
                'records': [record.__dict__ for record in data],
                'quantity': len(data),
                'fieldsToDisplay': fieldsToDisplay
            },
        )
