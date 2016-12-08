
# graphos libraries
from graphos.sources.model import ModelDataSource,SimpleDataSource
from graphos.renderers.flot import LineChart, BarChart

# class GraphMaker(View):


def line_chart_maker_model(queryset,fields):
    # call specific > stats
    #@TODO setup properly
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


def bar_chart_maker_simple(data):

    opt={'series': {
                 'lines': {'show': False, 'steps': False},
                 'bars': {'show': True, 'barWidth': 1.0, 'align': 'center',},},
        'xaxis':{
        'mode': "categories",
        'categories': ["Category One", "Category Two", "Category Three"]},
    }
    chart = BarChart(data_source=SimpleDataSource(data=data), options=opt)
    return chart