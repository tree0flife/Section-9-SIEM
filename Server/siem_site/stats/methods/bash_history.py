# need to import all other views in this folder
from ..models import *
from .graph import bar_chart_maker_simple

def bash_history_user(user):
    #  x axis = command   y axis = frequency
    axis = 'command', 'count'
    # need the X axis = command names: unique list of commands
    # need the y axis = count of command executed

    # 1 call to the database
    query = Bash_History.objects.values_list(axis[0], flat=True)

    # make a frequency counter with dictionary
    dict = {}
    for item in query:
        if item in dict:
            dict[item] = dict.get(item)+1
        else:
            dict[item] = 1

    #make simple querryset for graphos
    queryset = []
    queryset.append(list(axis))
    for x, y in dict.items():
        line = x, y
        list(line)
        queryset.append(line)

# #remove dups
# d = set(a)
# print(d)
# #{1, 2, 3, 4}
    return bar_chart_maker_simple(queryset=queryset)

def bash_history_all():
#display every usery user X axis, Y axis = total flag count

    return 'hi'
def bash_history_command(command):
    #displays: y axis = count(command). x= user
    #use drop down list
    return 'hi'