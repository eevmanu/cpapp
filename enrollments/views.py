# coding=utf-8

from django.utils.translation import ugettext as _
from django.utils.timezone import now

from rest_framework.decorators import api_view

from .forms import TicketForm
from .serializers import TicketSerializer
from .models import Ticket
from utils.response import ResponseSucess, ResponseError
from utils.utils import get_first_error


class TicketView(object):

    @staticmethod
    @api_view(['POST'])
    def list(request):
        if request.method == 'POST':
            data = request.DATA

            form = TicketForm(data)
            if not form.is_valid():
                return ResponseError(get_first_error(form.errors))
            data = form.cleaned_data

            ticket = Ticket.create(data)
            serializer = TicketSerializer(ticket)
            return ResponseSucess(serializer.data)

    @staticmethod
    @api_view(['PUT'])
    def cancel_ticket(request, pk):
        if request.method == 'PUT':
            ticket = Ticket.objects.filter(
                pk=pk,
                active=True,
                paid=False,
                valid_until__gte=now()
            )
            if not ticket.exists():
                return ResponseError(_(u"Ticket invalido"))

            ticket.first().cancel_ticket()
            return ResponseSucess("Cancelacion exitosa")
