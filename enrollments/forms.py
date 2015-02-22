# coding=utf-8

from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from .models import Enrollment, Ticket
from institutions.models import PreCollege, Week, Season


class TicketForm(forms.Form):
    student_id = forms.IntegerField()
    precollege_id = forms.IntegerField()
    weeks_id = forms.CharField()
    n_weeks = forms.IntegerField()
    amount = forms.DecimalField(max_digits=5, decimal_places=2)

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        if not User.objects.filter(pk=student_id).exists():
            raise ValidationError(_(u"Usuario invalido"))
        if Ticket.has_active_ticket(student_id=student_id):
            raise ValidationError(_(u"Ya tiene un ticket activo"))
        return student_id

    def clean_precollege_id(self):
        precollege_id = self.cleaned_data['precollege_id']
        if not PreCollege.objects.filter(pk=precollege_id).exists():
            raise ValidationError(_(u"Centro preuniversitario invalido"))
        return precollege_id

    def clean_weeks_id(self):
        weeks_id = self.cleaned_data['weeks_id']
        weeks_id = weeks_id.strip(',').split(',')
        weeks_id = [int(x) for x in set(filter(bool, weeks_id)) if x.isdigit()]
        n_input_weeks = len(weeks_id)
        n_valid_weeks = Week.objects.filter(pk__in=weeks_id).count()
        if n_input_weeks != n_valid_weeks:
            raise ValidationError(_(u"Semanas invalidas 1"))
        return weeks_id

    def clean(self):
        cleaned_data = super(TicketForm, self).clean()

        student_id = cleaned_data.get('student_id')
        precollege_id = cleaned_data.get('precollege_id')
        weeks_id = cleaned_data.get('weeks_id')
        n_weeks = cleaned_data.get('n_weeks')
        amount = cleaned_data.get('amount')

        if type(weeks_id) is not list:
            # Force initial clean per field
            raise ValidationError("")

        n_input_weeks = len(weeks_id)

        if n_weeks != n_input_weeks:
            raise ValidationError(
                _(u"Inconsistencia entre el numero de semanas enviadas y el numero de semanas recibidas y validas")
            )

        season = Season.get_current_season(precollege_id)
        if not season:
            raise ValidationError(
                _(u"La cepre actualmente no cuenta con una temporada activa")
            )

        n_valid_weeks_current_season = Week.objects.filter(
            pk__in=weeks_id,
            season__pk=season.pk
        ).count()
        if n_valid_weeks_current_season != n_input_weeks:
            raise ValidationError(_(u"Semanas invalidas 2"))

        cleaned_data['season_id'] = season.pk

        if Enrollment.objects.filter(week__pk__in=weeks_id, student__pk=student_id).exists():
            raise ValidationError(_(u"Alumno ya inscrito en una de la semanas"))

        pc = PreCollege.objects.filter(pk=precollege_id).first()
        discount_to_apply = 0
        if pc.weeks_discount2 <= n_weeks:
            discount_to_apply = pc.discount2
        elif pc.weeks_discount1 <= n_weeks:
            discount_to_apply = pc.discount1
        valid_amount = (pc.price_per_week * n_weeks) * (1 - (discount_to_apply/100))
        if abs(valid_amount - amount) > 0.01:
            raise ValidationError(_(u"Monto no valido"))

        return cleaned_data
