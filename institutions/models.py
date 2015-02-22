# coding=utf-8

from django.db import models
from django.utils.timezone import now

from s3direct.fields import S3DirectField

from utils.models import CPBaseModel
from utils.utils import remove_accents


class PreCollege(CPBaseModel):
    name = models.CharField(max_length=200)
    icon = S3DirectField(dest='precollege_icon', blank=True)

    weeks_discount1 = models.PositiveSmallIntegerField(null=True)
    discount1 = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    weeks_discount2 = models.PositiveSmallIntegerField(null=True)
    discount2 = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    price_per_week = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        db_table = 'precollege'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name = remove_accents(self.name)
        return super(PreCollege, self).save(*args, **kwargs)

    def get_current_season(self):
        return Season.get_current_season(self.pk)


class Season(CPBaseModel):
    name = models.CharField(max_length=200)
    begin = models.DateField()
    end = models.DateField()

    # price_per_week = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    precollege = models.ForeignKey('institutions.PreCollege', related_name='seasons')

    class Meta:
        db_table = 'season'

    def __unicode__(self):
        return u'{}, {}, {}-{}'.format(
            self.precollege.name,
            self.name,
            self.begin.strftime("%d/%m/%Y"),
            self.end.strftime("%d/%m/%Y")
        )

    def save(self, *args, **kwargs):
        if self.name:
            self.name = remove_accents(self.name)
        return super(Season, self).save(*args, **kwargs)

    @classmethod
    def get_current_season(cls, precollege_id):
        just_now = now()
        return cls.objects.filter(
            precollege__pk=precollege_id,
            begin__lte=just_now,
            end__gte=just_now
        ).first()


class Week(CPBaseModel):
    name = models.CharField(max_length=100)
    begin = models.DateField()
    end = models.DateField()

    publication = models.DateTimeField()

    season = models.ForeignKey('institutions.Season', related_name='weeks')

    students = models.ManyToManyField(
        'auth.User',
        related_name='weeks',
        through='enrollments.Enrollment',
    )

    tasktypes = models.ManyToManyField(
        'institutions.TaskType',
        related_name='weeks',
        through='tasks.Task'
    )

    tickets = models.ManyToManyField(
        'enrollments.Ticket',
        related_name='weeks',
        through='enrollments.TicketDetail'
    )

    class Meta:
        db_table = 'week'
        ordering = ('-begin',)  # most recent to less recent

    def __unicode__(self):
        return u'{}, {}, {}, {}-{}'.format(
            self.season.precollege.name,
            self.season.name,
            self.name,
            self.begin.strftime("%d/%m/%Y"),
            self.end.strftime("%d/%m/%Y")
        )

    def save(self, *args, **kwargs):
        if self.name:
            self.name = remove_accents(self.name)
        return super(Week, self).save(*args, **kwargs)


class TaskType(CPBaseModel):
    name = models.CharField(max_length=200)
    icon = S3DirectField(dest='tasktype_icon', blank=True)

    precollege = models.ForeignKey('institutions.PreCollege', related_name='tasktypes')

    class Meta:
        db_table = 'task_type'

    def __unicode__(self):
        return u'{}, {}'.format(self.precollege.name, self.name)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = remove_accents(self.name)
        return super(TaskType, self).save(*args, **kwargs)
