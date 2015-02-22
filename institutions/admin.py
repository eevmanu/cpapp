# coding=utf-8

from django import forms
from django.forms import ValidationError
from django.contrib import admin
from .models import PreCollege, Season, Week, TaskType


class ValidPercentageForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(ValidPercentageForm, self).clean()
        discount1 = cleaned_data.get('discount1')
        discount2 = cleaned_data.get('discount2')
        if discount1 < 0 or discount1 > 100:
            raise ValidationError("Descuento fuerto de los limites adecuados")
        if discount2 < 0 or discount2 > 100:
            raise ValidationError("Descuento fuerto de los limites adecuados")
        return cleaned_data


@admin.register(PreCollege)
class PreCollegeAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'name',
        'icon',
        'weeks_discount1',
        'discount1',
        'weeks_discount2',
        'discount2',
        'price_per_week',
    )
    form = ValidPercentageForm
    search_fields = [
        'name',
        'price_per_week',
        'discount1',
        'discount2',
    ]


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'precollege',
        'name',
        'begin',
        'end',
    )
    search_fields = [
        'name',
        'precollege__name',
    ]


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'season',
        'name',
        'begin',
        'end',
    )
    search_fields = [
        'name',
        'season__name',
        'season__precollege__name',
    ]


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'precollege',
        'name',
        'icon',
    )
    search_fields = [
        'name',
        'precollege__name',
    ]
