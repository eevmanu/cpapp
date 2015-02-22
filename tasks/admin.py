from django import forms
from django.forms import ValidationError
from django.utils.translation import ugettext as _
from django.contrib import admin
from .models import Task, TaskTopic, Problem


class SamePrecollegeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(SamePrecollegeForm, self).clean()
        tasktype = cleaned_data.get('tasktype')
        week = cleaned_data.get('week')
        try:
            if tasktype.precollege.pk != week.season.precollege.pk:
                raise ValidationError(_(u"No coinciden los centros preuniversitarios"))
        except Exception:
            raise ValidationError("Se ha perdido integridad en la info")
        return cleaned_data


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'tasktype',
        'week',
    )
    form = SamePrecollegeForm
    search_fields = [
        'week__name',
        'tasktype__name',
    ]


@admin.register(TaskTopic)
class TaskTopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'task',
        'name',
        'icon',
    )
    search_fields = [
        'name',
    ]


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'course',
        'number',
        'pdf',
    )
    search_fields = [
        'course__name',
        'number',
    ]
