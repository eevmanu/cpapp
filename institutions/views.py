# coding=utf-8

# from django.utils.translation import ugettext as _

from rest_framework.decorators import api_view

from .models import PreCollege, Week, TaskType, Season
from .serializers import PreCollegeSerializer, TaskTypeSerializer
from .serializers import WeekSerializer, WeekSerializer_Enrollment

from enrollments.models import Enrollment

from utils.response import ResponseSucess
# from utils.response import ResponseError


class PreCollegeView(object):

    @staticmethod
    @api_view(['GET', 'POST', 'DELETE'])
    def list(request):
        if request.method == 'GET':
            precolleges = PreCollege.objects.all()
            serializer = PreCollegeSerializer(precolleges, many=True)
            return ResponseSucess(serializer.data)

    @staticmethod
    @api_view(['GET'])
    def tasktypes_from_precollege(request, pk):
        if request.method == 'GET':
            tasktypes = TaskType.objects.filter(precollege__pk=pk)
            serializer = TaskTypeSerializer(tasktypes, many=True)
            return ResponseSucess(serializer.data)


class WeekView(object):

    @staticmethod
    @api_view(['GET'])
    def list(request):
        if request.method == 'GET':
            query = request.QUERY_PARAMS

            precollege_id = query.get('precollege_id', '-1')
            student_id = query.get('student_id', '-1')

            if not precollege_id.isdigit() or not student_id.isdigit():
                return ResponseSucess([])

            season = Season.get_current_season(precollege_id=precollege_id)
            if not season:
                return ResponseSucess([])

            action = query.get('action')
            if not action:
                weeks = Week.objects.filter(
                    season__pk=season.pk,
                    students__pk=student_id
                )

                serializer = WeekSerializer(weeks, many=True)
            elif action == 'enrollment':
                weeks = Week.objects.filter(season__pk=season.pk)

                for week in weeks:
                    purchase = Enrollment.objects.filter(week__pk=week.pk)
                    purchase = purchase.filter(student__pk=student_id)
                    setattr(week, 'purchase', purchase.exists())

                serializer = WeekSerializer_Enrollment(weeks, many=True)

            return ResponseSucess(serializer.data)
