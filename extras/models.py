# coding=utf-8

from django.db import models

from utils.models import CPBaseModel


class MsgStudentInSeason(CPBaseModel):
    precollege = models.ForeignKey('institutions.PreCollege')
    msg = models.TextField()

    class Meta:
        db_table = 'msg_student_in_season'
        verbose_name = 'Enviar mensaje'
        verbose_name_plural = 'Mensajes hacia temporada activa de una cepre'


class UploadSolution(CPBaseModel):
    solution = models.FileField(upload_to='solutions')

    class Meta:
        db_table = 'upload_solution'
        verbose_name = 'Carga masiva'
        verbose_name_plural = 'Carga masiva de soluciones'
