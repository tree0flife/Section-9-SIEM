from django.views.generic import View

#graphos libraries
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.flot import LineChart

class GraphMaker(View):


    def line_chart_maker(request):


        # get data source need to use models
        data = [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]

        # DataSource object creation
        data_source = SimpleDataSource(data=data)
        # Chart object
        linechart = LineChart(data_source)

        return {'line_chart': linechart}