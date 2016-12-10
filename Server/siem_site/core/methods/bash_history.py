# need to import all other views in this folder
from ..models import *
from .graph import bar_chart_maker_simple

from graphos.sources.model import ModelDataSource,SimpleDataSource
from graphos.renderers.flot import BarChart, LineChart

def bash_history_client(client):
    #  x axis = command   y axis = frequency
    axis = ['command', 'count']

    # 1 call to the database: select COMMAND from BASH_HISTORY where user like '%USER';
    query = Bash_History.objects.filter(user__contains=client)
    query = query.values_list(axis[0], flat=True)
    # make a frequency counter with dictionary
    dict = {}
    for item in query:
        if item in dict:
            dict[item] = dict.get(item)+1
        else:
            dict[item] = 1
    #make simple querryset for graphos
    queryset = [axis]
    for x, y in dict.items():
        line = x, y
        queryset.append(list(line))
    chart = bar_chart_maker_simple(data=queryset)
    return chart


def bash_history_all():
#display every usery user X axis, Y axis = total flag count

    return 'hi'
def bash_history_command(command):
    #displays: y axis = count(command). x= user
    #use drop down list
    return 'hi'