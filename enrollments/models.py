# coding=utf-8

import json
from datetime import timedelta
from random import choice
from string import digits

from django.db import models
from django.utils.timezone import now as get_current_time
from django.conf import settings

import requests

from utils.models import CPBaseModel


class Ticket(CPBaseModel):
    precollege = models.ForeignKey('institutions.PreCollege', related_name='tickets')
    season = models.ForeignKey('institutions.Season', related_name='tickets')
    student = models.ForeignKey('auth.User', related_name='tickets')

    amount = models.DecimalField(max_digits=6, decimal_places=2)

    number = models.PositiveIntegerField(unique=True)

    active = models.BooleanField(default=True)
    valid_until = models.DateTimeField()

    paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'ticket'

    def __unicode__(self):
        return u'Nro: {} | {} | {} | {}'.format(
            self.number,
            'Activo' if self.active else 'No activo',
            'Pagado' if self.paid else 'No pagado',
            'Vencido' if get_current_time() > self.valid_until else 'Vence: ' + str(self.valid_until)
        )

    @classmethod
    def has_active_ticket(cls, student_id):
        return cls.objects.filter(
            student__pk=student_id,
            active=True,
        ).exists()

    def approve_ticket(self):
        now = get_current_time()
        if self.active and not self.paid and now <= self.valid_until:

            self.active = False
            self.paid = True
            self.paid_date = now
            self.save()

            for ticket_detail in self.ticket_details.all():
                enrollment = Enrollment(
                    student_id=self.student.pk,
                    week_id=ticket_detail.week.pk
                )
                enrollment.save()

            data = {
                'registration_ids': [self.student.cpprofile.device_id],
                'data': {
                    'action': 'enrollment',
                    'precollege': {
                        'id': self.precollege.pk,
                    },
                    'season': {
                        'id': self.season.pk,
                    },
                    'weeks': [{'id': x.week.pk} for x in self.ticket_details.all()],
                    # 'weeks': [x.week.pk for x in self.ticket_details.all()],
                }
            }

            # resp = requests.post(
            requests.post(
                url=settings.GCM_URL,
                headers=settings.GCM_HEADERS,
                data=json.dumps(data),
            )
            # print json.dumps(resp.json(), indent=4, sort_keys=True)

        # Sigue activo pero ya vencio, lo desactivo
        if self.active and now > self.valid_until:
            self.active = False
            self.save()

    def cancel_ticket(self):
        self.active = False
        self.paid = False
        self.save()

    @classmethod
    def deactivate_expired_tickets(cls):
        return cls.objects.filter(
            active=True,
            valid_until__lte=get_current_time()
        ).update(active=False)

    @classmethod
    def create(cls, data):
        precollege_id = data.get('precollege_id')
        season_id = data.get('season_id')
        student_id = data.get('student_id')
        amount = data.get('amount')
        weeks_id = data.get('weeks_id')

        ticket = cls(
            precollege_id=precollege_id,
            season_id=season_id,
            student_id=student_id,
            number=Ticket.generate_ticket_number(),
            amount=amount,
            active=True,
            valid_until=get_current_time() + timedelta(hours=48),
            paid=False,
        )
        ticket.save()

        for week_id in weeks_id:
            ticket_detail = TicketDetail(ticket_id=ticket.pk, week_id=week_id)
            ticket_detail.save()

        return ticket

    @classmethod
    def generate_ticket_number(cls, length=settings.TICKET_NUMBER_LENGTH):
        ticket_number = int(''.join([choice(digits) for i in xrange(length)]))

        if cls.objects.filter(number=ticket_number).exists():
            return cls.generate_ticket_number(length=length)
        return ticket_number


# M2M
class TicketDetail(CPBaseModel):
    ticket = models.ForeignKey('enrollments.Ticket', related_name='ticket_details')
    week = models.ForeignKey('institutions.Week')

    class Meta:
        db_table = 'ticket_detail'
        unique_together = (('ticket', 'week'),)

    def __unicode__(self):
        return u'{} - {}'.format(self.ticket.number, self.week.name)


# M2M
class Enrollment(CPBaseModel):
    student = models.ForeignKey('auth.User')
    week = models.ForeignKey('institutions.Week')

    class Meta:
        db_table = 'enrollment'
        unique_together = (('student', 'week'),)

    def __unicode__(self):
        return u'{} - {}'.format(self.student.email, self.week.name)
