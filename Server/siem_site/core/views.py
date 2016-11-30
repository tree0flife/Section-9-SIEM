from django.shortcuts import render
from stats.methods.bash_history import *

# @TODO need to import the methods from other methods to post and then seperate


def view_bash_history_user(request):
    # @TODO take response and get user variable, make proper templates
    user = 'user1'
    template = 'test_graph.html'
    bar_chart = bash_history_user(user)
    context ={
        'bar_chart': bar_chart,
        }

    return render(request, template_name=template, context=context )

