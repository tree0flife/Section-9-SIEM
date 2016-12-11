from ..models import Network
from .graph import bar_chart_maker_simple

def outbound_ip_client(client):
    #  x axis = command   y axis = frequency
    axis = ['ip', 'count']

    # 1 call to the database: select COMMAND from BASH_HISTORY where user like '%USER';
    query = Network.objects.filter(username__contains=client)
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

    #pass querryset to generic graph maker
    chart = bar_chart_maker_simple(data=queryset)
    return chart