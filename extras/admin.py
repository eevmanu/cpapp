# coding=utf-8

import json
import requests
import zipfile

from django.contrib import admin
from django.conf import settings

import boto
import boto.s3
from boto.s3.key import Key

from .models import MsgStudentInSeason
from .models import UploadSolution

from enrollments.models import Enrollment
from accounts.models import CPProfile
from institutions.models import PreCollege, Season, Week, TaskType
from tasks.models import Task, TaskTopic, Problem
from utils.utils import zip_filename_to_info_solution
from utils.utils import create_filename


@admin.register(MsgStudentInSeason)
class MsgStudentInSeasonAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        # print 'cepre_id', obj.precollege.pk
        # print 'mensaje', obj.msg

        season = Season.get_current_season(precollege_id=obj.precollege.pk)
        # print 'temporada', season
        if not season:
            return

        students_ids = Enrollment.objects.filter(week__season__pk=season.pk)
        students_ids = students_ids.values_list('student_id', flat=True)
        students_ids = list(set(students_ids))
        # print 'estudiantes', students_ids
        if not students_ids:
            return

        devices_reg_ids = CPProfile.objects.filter(pk__in=students_ids)
        devices_reg_ids = devices_reg_ids.values_list('device_id', flat=True)
        devices_reg_ids = list(set(filter(bool, devices_reg_ids)))
        # devices_reg_ids = filter(bool, devices_reg_ids)
        # print 'dispositivos', devices_reg_ids
        if not devices_reg_ids:
            return

        data = {
            'registration_ids': devices_reg_ids,
            'data': {
                'action': 'show_message',
                'message': obj.msg,
                'precollege': {
                    'id': obj.precollege.pk,
                }
            }
        }
        # print data

        # resp = requests.post(
        requests.post(
            url=settings.GCM_URL,
            headers=settings.GCM_HEADERS,
            data=json.dumps(data),
        )
        # print json.dumps(resp.json(), indent=4, sort_keys=True)

        obj.save()

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UploadSolution)
class UploadSolutionAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        # print 'request.POST', request.POST
        # print 'solution', request.FILES['solution']
        # print 'obj.solution', obj.solution

        with zipfile.ZipFile(request.FILES['solution'], "r", zipfile.ZIP_STORED) as openzip:
            valid_files = [x for x in openzip.infolist() if x.file_size != 0]
            # por el CRC
            # por file_size
            # por filename
            # por internal_attr

            for f in valid_files:

                # print 'filename', f.filename
                # print 'orig_filename', f.orig_filename
                # print type(f.filename)

                info = zip_filename_to_info_solution(f.filename)
                if not info:
                    continue

                # print info

                precollege = PreCollege.objects.filter(
                    name=info['precollege']
                )
                precollege = precollege.first()
                if not precollege:
                    continue

                # print 'ubico cepre'

                season = Season.objects.filter(
                    precollege=precollege,
                    name=info['season']
                )
                season = season.first()
                if not season:
                    continue
                # print 'ubico temporada'

                week = Week.objects.filter(
                    season=season,
                    name=info['week']
                )
                week = week.first()
                if not week:
                    continue
                # print 'ubico semana'

                tasktype = TaskType.objects.filter(
                    precollege=precollege,
                    name=info['tasktype']
                )
                tasktype = tasktype.first()
                if not tasktype:
                    continue
                # print 'ubico tipo de tarea'

                task = Task.objects.filter(
                    week=week,
                    tasktype=tasktype
                )
                task = task.first()
                if not task:
                    continue
                # print 'ubico tarea'

                tasktopic = TaskTopic.objects.filter(
                    task=task,
                    name=info['tasktopic']
                )
                tasktopic = tasktopic.first()
                if not tasktopic:
                    continue
                # print 'ubico tema de la tarea'

                number = info['name']
                if not number.isdigit():
                    continue
                # print 'naming correcto de solucion'

                number = int(info['name'])
                problem = Problem.objects.filter(
                    course=tasktopic,
                    number=number
                )
                problem = problem.first()
                if problem:
                    continue
                # print 'solucion no existe aun'

                if info['ext'] not in ('jpg', 'jpeg', 'png'):
                    continue

                # print 'upload file {}'.format(info['filename'])

                # upload file to s3
                conn = boto.connect_s3(
                    settings.AWS_ACCESS_KEY_ID,
                    settings.AWS_SECRET_ACCESS_KEY
                )
                bucket = conn.create_bucket(
                    settings.AWS_STORAGE_BUCKET_NAME,
                    location=boto.s3.connection.Location.DEFAULT
                )
                tmp = openzip.read(f)
                k = Key(bucket)
                k.key = create_filename(info['filename'], 'problems_image')
                if info['ext'] in ('jpg', 'jpeg'):
                    k.set_metadata('Content-Type', 'image/jpeg')
                elif info['ext'] in ('png',):
                    k.set_metadata('Content-Type', 'image/png')
                k.set_contents_from_string(tmp)
                k.make_public()
                url = k.generate_url(
                    expires_in=0,
                    query_auth=False,
                    force_http=True
                )

                # save problem model

                problem = Problem(
                    number=number,
                    pdf=url,
                    course=tasktopic,
                )
                problem.save()

        # obj.save()

    def has_change_permission(self, request, obj=None):
        return False
