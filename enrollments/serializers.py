# coding=utf-8

from django.conf import settings

from rest_framework import serializers

from .models import Ticket
from utils.serializers import CPBaseSerializer


class TicketSerializer(CPBaseSerializer):
    ticket_id = serializers.Field(source='pk')
    bank_account = serializers.SerializerMethodField('get_bank_account')
    email = serializers.SerializerMethodField('get_email_for_enrollments')

    class Meta:
        model = Ticket
        fields = (
            'id',
            'ticket_id',

            'precollege',
            'season',
            'student',

            'number',
            'amount',
            'active',
            'valid_until',
            'paid',

            'email',
            'bank_account',
        )

    def get_bank_account(self, object):
        return settings.BANK_ACCOUNT_FOR_ENROLLMENTS

    def get_email_for_enrollments(self, object):
        return settings.EMAIL_FOR_ENROLLMENTS
