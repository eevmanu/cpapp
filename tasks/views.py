# coding=utf-8

# from decimal import Decimal, InvalidOperation

from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from rest_framework.decorators import api_view

from .models import Task, Problem, Result
from .serializers import TaskSerializer
from utils.response import ResponseSucess, ResponseError
from utils.utils import isfloat


class TaskView(object):

    @staticmethod
    @api_view(['GET'])
    def per_week_per_tasktype(request, week_pk, tasktype_pk):
        if request.method == 'GET':

            tasks = Task.objects.filter(
                week__pk=week_pk,
                tasktype__pk=tasktype_pk
            )
            if not tasks.exists():
                return ResponseError(_(u"Tarea invalida"))
            """
            Si existe la tarea, entonces elijo la primera porque por el momento, dado una semana y un tipo de tarea, solo hay una unica tarea pero la logica esta para que soporte mas de una
            """
            task = tasks.first()
            serializer = TaskSerializer(task)
            return ResponseSucess(serializer.data)


class ResultView(object):

    @staticmethod
    @api_view(['GET', 'POST'])
    def list(request):
        if request.method == 'GET':
            query = request.QUERY_PARAMS

            student_id = unicode(query.get('student_id', '-1'))
            problem_id = unicode(query.get('problem_id', '-1'))

            if not student_id.isdigit() or not problem_id.isdigit():
                return ResponseError(_(u"Faltan datos y/o datos incorrectos"))

            results = Result.objects.filter(
                solver__pk=student_id,
                problem__pk=problem_id
            )
            if not results.exists():
                return ResponseError(_(u"Sin calificacion"))

            result = results.first()
            return ResponseSucess({'stars': result.stars})

        elif request.method == 'POST':
            data = request.DATA

            student_id = unicode(data.get('student_id', '-1'))
            problem_id = unicode(data.get('problem_id', '-1'))
            stars = unicode(data.get('stars', '-1'))

            if not isfloat(stars) or float(stars) < 0 or 5 < float(stars):
                return ResponseError(_(u"Faltan datos y/o datos incorrectos"))

            if not student_id.isdigit() or not problem_id.isdigit():
                return ResponseError(_(u"Faltan datos y/o datos incorrectos"))

            results = Result.objects.filter(
                solver__pk=student_id,
                problem__pk=problem_id,
            )
            if not results.exists():
                student = User.objects.filter(pk=student_id)
                problem = Problem.objects.filter(pk=problem_id)
                if not student.exists():
                    return ResponseError(_(u"Usuario invalido"))
                if not problem.exists():
                    return ResponseError(_(u"Problema invalido"))

                record = Result(
                    solver_id=student_id,
                    problem_id=problem_id,
                    stars=stars
                )
                record.save()
            else:
                result = results.first()
                result.stars = stars
                result.save()

            return ResponseSucess({'stars': stars})
