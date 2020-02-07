# Adjust Home Task
A simple Django app consisting of a single endpoint which filters, sorts and groups data contained in a local relational database and prints results to the screen.

# First-Time Operating Instructions:
1. Clone or download this repository to your favourite directory
2. In your terminal, navigate to the project `/adjust-home-task` directory
3. Create and activate a python virtual environment
4. Run `pip install django`
5. Navigate to Navigate to the `/adjust-home-task/adjustapp` directory
6. Run `python manage.py migrate` to populate the database
7. Run `python manage.py runserver` to start the app
8. In your browser, navigate to `localhost:8000` and observe welcome page
9. Click the link on the screen or navigate to `localhost:8000/data` to see the data printout
10. See below sections for information on how to manipulate the data printout

# How to Manipulate the Data Printout:
The data printout is manipulated by calling the `/data` endpoint with different query parameters. There are four possible query parameters: `fields`, `filters`, `groupBy` and `orderBy`. Each parameter takes values in a certain format. The `fields` parameter defines which fields you would like displayed in the printout. If no field paramter values are defined, all fields will be shown by default. The `filters` parameter defines which subset of the data you would like to see. This is done using arithmetic comparisons and logical operations on the data contained in the database. The `groupBy` parameter defines which data field or fields you would like aggregated. The `groupBy` parameter defines which field you would like the data sorted by and in which direction the sorting should take place.

To see the parameter formats, or for specific example manipulations, see the sections below.

# Expected Parameter Formats:
- Fields: `fields=field1,field2, ...`
- Filter: `filters=NOT|field|arithmeticOperator|value|logicalOperator, ...`
    - Where the `NOT` and `logicalOperator` terms are optional
- Group By: `groupBy=field1,field2, ...`
- Order By: `orderBy=field,direction`
    - Where the `direction` term is either `asc` or `desc`

# Test Case URLs:
- Case 1: Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order
    - `/data?fields=channel,country,impressions,clicks&filters=date|<=|%272017-06-01%27&groupby=channel,country&orderby=clicks,desc`
- Case 2: Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order
    - `/data?fields=date,os,installs&filters=date|>=|%272017-05-01%27|and,date|<|%272017-06-01%27|and,os|=|%27ios%27&groupby=date&orderby=date,asc`
- Case 3: Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order
    - `/data?fields=date,country,os,revenue&filters=date|=|%272017-06-01%27|and,country|=|%27US%27&groupby=os&orderby=revenue,desc`
- Case 4: Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order
    - `/data?fields=channel,country,spend,cpi&filters=country|=|%27CA%27&groupby=channel&orderby=cpi,desc`

# Dependancies:
- Django
- Python3
- SQLite3