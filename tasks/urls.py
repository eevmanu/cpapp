from django.conf.urls import patterns, url

from .views import TaskView, ResultView

urlpatterns = patterns(
    'tasks.views',

    url(r'^tasks/weeks/(?P<week_pk>[0-9]+)/tasktypes/(?P<tasktype_pk>[0-9]+)?$', TaskView.per_week_per_tasktype,
        name='tasks_get_task_with_all_info'),
    url(r'^results/?$', ResultView.list,
        name='tasks_results_from_problem')

)
