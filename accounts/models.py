# coding=utf-8

import json

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.timezone import now

import requests
from s3direct.fields import S3DirectField

from enrollments.models import Ticket
from utils.models import CPBaseModel


class CPProfile(CPBaseModel):
    user = models.OneToOneField('auth.User')

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    photo = S3DirectField(dest='cpprofile_photo', blank=True)

    password_reset_token = models.CharField(max_length=400, default='', blank=True)

    device_id = models.TextField(default='', blank=True)

    class Meta:
        db_table = 'cp_profile'

    @property
    def email(self):
        return self.user.email

    @property
    def reg_id(self):
        return self.device_id

    def __unicode__(self):
        return self.email
        # return u'{}-{}'.format(self.id, self.email)

    def get_full_name(self):
        full_name = u"{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

    def update_device_id(self, device_id):
        self.owning_device_id(device_id)

        if self.device_id != device_id:

            data = {
                'registration_ids': [self.device_id],
                'data': {
                    'action': 'signout',
                }
            }

            requests.post(
                url=settings.GCM_URL,
                data=json.dumps(data),
                headers=settings.GCM_HEADERS
            )

            self.device_id = device_id
            self.save()

    def owning_device_id(self, device_id):
        # All except me clean that have this device_id, clean it
        tmp = CPProfile.objects.filter(~Q(pk=self.pk), device_id=device_id)
        tmp.update(device_id='')

    @classmethod
    def clean_reg_id(cls, reg_id):
        # Clean all student that have this device_id
        cls.objects.filter(device_id=reg_id).update(device_id='')

    @property
    def active_ticket(self):
        active_tickets = Ticket.objects.filter(
            student_id=self.user.pk,
            active=True,
            valid_until__gte=now(),
        )
        n_tickets = active_tickets.count()
        if n_tickets == 0:
            return None
        elif n_tickets > 0:
            active_ticket = active_tickets.order_by('-pk').first()
            if n_tickets > 1:
                # Can't have more than one active ticket
                for t in active_tickets.exclude(pk=active_ticket.pk):
                    t.cancel_ticket()
            return active_ticket


class FBProfile(CPBaseModel):
    user = models.OneToOneField('auth.User')

    fb_id = models.BigIntegerField(unique=True)
    email = models.EmailField(max_length=100, blank=True)
    token = models.TextField(default='', blank=True)

    class Meta:
        db_table = 'fb_profile'

    def __unicode__(self):
        return u'{} {} {}'.format(self.id, self.user.email, self.fb_id)
