# coding=utf-8

from django.contrib import admin
from .models import Ticket, TicketDetail, Enrollment


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'precollege',
        'season',
        'student_email',

        'number',
        'amount',

        'active',
        'valid_until',

        'paid',
        'paid_date',
    )

    def student_email(self, obj):
        return u'{}'.format(obj.student.email)
    student_email.short_description = 'student'

    actions_on_bottom = True
    actions = ['approve_ticket', 'cancel_ticket']
    # date_hierarchy = 'created'
    list_filter = ('active',)
    search_fields = [
        'number',
        'student__email',
        'student__username',
        'precollege__name',
    ]

    def approve_ticket(self, request, queryset):
        for ticket in queryset:
            ticket.approve_ticket()
    approve_ticket.short_description = 'Aprobar Ticket'

    def cancel_ticket(self, request, queryset):
        for ticket in queryset:
            ticket.cancel_ticket()
    cancel_ticket.short_description = 'Cancelar Ticket'

    # En caso quieran generar manualmente los tickets y no via mobile
    # def has_add_permission(self, request):
    #     return False


@admin.register(TicketDetail)
class TicketDetailAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'ticket',
        'week',
    )

    def has_add_permission(self, request):
        return False


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'student_email',
        'week',
    )
    search_fields = [
        'week__name'
        'week__season__name'
        'week__season__precollege_name'
        'student__email'
    ]

    # def has_add_permission(self, request):
    #     return False

    def student_email(self, obj):
        return u'{}'.format(obj.student.email)
    student_email.short_description = 'student'
