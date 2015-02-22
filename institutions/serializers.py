# coding=utf-8

import pytz
from rest_framework import serializers

from .models import PreCollege, Week, TaskType
from utils.serializers import CPBaseSerializer


class PreCollegeSerializer(CPBaseSerializer):
    precollege_id = serializers.Field(source='pk')

    class Meta:
        model = PreCollege
        fields = (
            'id',
            'precollege_id',

            'name',
            'icon',
            'weeks_discount1',
            'discount1',
            'weeks_discount2',
            'discount2',
            'price_per_week',
        )


class WeekSerializer(CPBaseSerializer):
    week_id = serializers.Field(source='pk')
    name = serializers.SerializerMethodField('format_name')
    publication = serializers.SerializerMethodField('get_publication')

    class Meta:
        model = Week
        fields = (
            'id',
            'week_id',

            'name',
            'begin',
            'end',
            'publication',
        )

    def format_name(self, obj):
        return '{} ({} - {})'.format(
            obj.name,
            obj.begin.strftime("%d/%m"),
            obj.end.strftime("%d/%m")
        )

    def get_publication(self, obj):
        local_tz = pytz.timezone('America/Lima')
        publication = obj.publication.replace(tzinfo=pytz.utc)
        publication = publication.astimezone(local_tz)
        publication = local_tz.normalize(publication)
        data = {
            'date': publication.date(),
            'time': publication.time()
        }
        return data


class WeekSerializer_Enrollment(CPBaseSerializer):
    week_id = serializers.Field(source='pk')
    name = serializers.SerializerMethodField('format_name')
    purchase = serializers.SerializerMethodField('purchase_state')
    publication = serializers.SerializerMethodField('get_publication')

    class Meta:
        model = Week
        fields = (
            'id',
            'week_id',

            'name',
            'begin',
            'end',
            'purchase',
            'publication',
        )

    def format_name(self, obj):
        return '{} ({} - {})'.format(
            obj.name,
            obj.begin.strftime("%d/%m"),
            obj.end.strftime("%d/%m")
        )

    def purchase_state(self, obj):
        return getattr(obj, 'purchase')

    def get_publication(self, obj):
        local_tz = pytz.timezone('America/Lima')
        publication = obj.publication.replace(tzinfo=pytz.utc)
        publication = publication.astimezone(local_tz)
        publication = local_tz.normalize(publication)
        data = {
            'date': publication.date(),
            'time': publication.time()
        }
        return data


class TaskTypeSerializer(CPBaseSerializer):
    tasktype_id = serializers.Field(source='pk')

    class Meta:
        model = TaskType
        fields = (
            'id',
            'tasktype_id',

            'name',
            'icon',
        )
