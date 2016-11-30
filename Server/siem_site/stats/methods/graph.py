
# graphos libraries
from graphos.sources.model import ModelDataSource,SimpleDataSource
from graphos.renderers.flot import LineChart, BarChart

# class GraphMaker(View):


def line_chart_maker_model(queryset,fields):
    # call specific > stats

        # get data source need to use models
        # DataSource object creation
        data_source = ModelDataSource(queryset, fields=[fields])
        # Chart object
        linechart = LineChart(data_source)
        return {'line_chart': linechart}

#def line_chart_maker_simple(self,queryset,fields):
#   return
#def bar_chart_maker_model(self,queryset,fields):
#    return

def bar_chart_maker_simple(queryset,fields):
    data_source = SimpleDataSource(queryset)
    bar_chart = BarChart(data_source)
    return {'bar_chart': bar_chart}
