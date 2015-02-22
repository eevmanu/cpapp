# coding=utf-8

from django.db import models

from s3direct.fields import S3DirectField

from utils.models import CPBaseModel
from utils.utils import remove_accents


# M2M
class Task(CPBaseModel):
    tasktype = models.ForeignKey('institutions.TaskType', related_name='tasks')
    week = models.ForeignKey('institutions.Week', related_name='tasks')

    class Meta:
        db_table = 'task'
        # unique_together = (('tasktype', 'week'),)

    def __unicode__(self):
        return u'{}, {}, {} | {}'.format(
            self.week.season.precollege.name,
            self.week.season.name,
            self.week.name,
            self.tasktype.name,
        )


class TaskTopic(CPBaseModel):
    name = models.CharField(max_length=100)
    icon = S3DirectField(dest='tasktopic_icon', blank=True)

    task = models.ForeignKey('tasks.Task', related_name='task_topics')

    class Meta:
        db_table = 'task_topic'

    def __unicode__(self):
        return u'{}, Tarea {}'.format(self.name, self.task.pk)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = remove_accents(self.name)
        return super(TaskTopic, self).save(*args, **kwargs)


# Solution model
class Problem(CPBaseModel):
    number = models.PositiveIntegerField()
    pdf = S3DirectField(dest='problems_image', blank=True)

    course = models.ForeignKey('tasks.TaskTopic', related_name='problems')

    solvers = models.ManyToManyField(
        'auth.User',
        related_name='problems',
        through='tasks.Result',
    )

    class Meta:
        db_table = 'problem'

    def __unicode__(self):
        return u'Problema {}, {}'.format(self.number, self.course.name)


# M2M
class Result(CPBaseModel):
    solver = models.ForeignKey('auth.User', related_name='results')
    problem = models.ForeignKey('tasks.Problem', related_name='results')

    stars = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    # score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        db_table = 'result'

    def __unicode__(self):
        return u'{}, Problema {}'.format(self.solver.email, self.problem.pk)
