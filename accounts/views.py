# coding=utf-8

from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.timezone import now
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework import status
from validate_email import validate_email

from .forms import SignupForm, SigninForm, SigninFBForm
from .models import CPProfile, FBProfile
from .serializers import UserSerializer
from utils.response import ResponseSucess, ResponseError
from utils.utils import get_first_error, generate_random_username
from enrollments.serializers import TicketSerializer


class AccountView(object):

    @staticmethod
    @api_view(['PUT'])
    def detail(request, pk):
        user = User.objects.filter(pk=pk)
        if not user.exists():
            return ResponseError(_(u"Estudiante invalido"))
        user = user.first()

        if request.method == 'PUT':
            data = request.DATA

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            old_password = data.get('old_password')
            new_password = data.get('new_password')

            if not first_name and not last_name and (not old_password or (not email and not new_password)):
                return ResponseError(_(u"Faltan datos y/o datos incorrectos"))

            if first_name:
                user.cpprofile.first_name = first_name
                user.cpprofile.save()

            if last_name:
                user.cpprofile.last_name = last_name
                user.cpprofile.save()

            if old_password:
                if user.check_password(old_password):
                    if email and validate_email(email) and user.email != email and User.objects.filter(email=email).count() == 0:
                        user.email = email
                    if new_password and len(new_password) >= 5 and old_password != new_password:
                        user.set_password(new_password)
                    user.save()
                else:
                    return ResponseError(_(u"Contraseña actual incorrecta"))

            serializer = UserSerializer(user)
            return ResponseSucess(serializer.data)

    @staticmethod
    @api_view(['POST'])
    def signup(request):
        if request.method == 'POST':
            data = request.DATA

            form = SignupForm(data)
            if not form.is_valid():
                return ResponseError(get_first_error(form.errors))
            data = form.cleaned_data

            user = User.objects.create_user(
                username=generate_random_username(),
                email=data['email'],
                password=data['password'],
            )

            cp_profile = CPProfile(
                user=user,
                first_name=data['first_name'],
                last_name=data['last_name'],
                device_id=data['reg_id'],
            )
            cp_profile.save()

            cp_profile.owning_device_id(data['reg_id'])

            serializer = UserSerializer(user)

            return ResponseSucess(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

    @staticmethod
    @api_view(['POST'])
    def signout(request):
        if request.method == 'POST':
            data = request.DATA

            reg_id = data.get('reg_id')
            if not reg_id:
                return ResponseError(_("Cierre de sesion invalido"))

            CPProfile.clean_reg_id(reg_id)
            return ResponseSucess()

    @staticmethod
    @api_view(['POST'])
    def signin(request):
        if request.method == 'POST':
            data = request.DATA

            email = data.get('email')
            password = data.get('password')
            fb_id = data.get('fb_id')

            if not email or (not password and not fb_id):
                return ResponseError(_(u"Faltan datos y/o datos incorrectos"))

            if password:
                return AccountView.signin_standard(data)
            if fb_id:
                return AccountView.signin_facebook(data)

    @staticmethod
    def signin_standard(data):

        form = SigninForm(data)
        if not form.is_valid():
            return ResponseError(get_first_error(form.errors))
        data = form.cleaned_data

        email = data['email']
        password = data['password']
        device_id = data['reg_id']

        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                user.cpprofile.update_device_id(device_id)

                user.last_login = now()
                user.save()

                serializer = UserSerializer(user)
                return ResponseSucess(serializer.data)
            else:
                return ResponseError(_(u"Usuario no activo"))
        else:
            return ResponseError(
                _(u"Correo electrónico y/o contraseña incorrectos")
            )

    @staticmethod
    def signin_facebook(data):

        form = SigninFBForm(data)
        if not form.is_valid():
            return ResponseError(get_first_error(form.errors))
        data = form.cleaned_data

        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        fb_id = data['fb_id']
        token = data['token']
        device_id = data['reg_id']

        user = authenticate(facebook_id=fb_id)
        if user:
            if user.is_active:
                user.cpprofile.update_device_id(device_id)
                if token:
                    fbprofile = user.fbprofile
                    fbprofile.token = token
                    fbprofile.save()

                user.last_login = now()
                user.save()

                serializer = UserSerializer(user)
                return ResponseSucess(serializer.data)
            else:
                return ResponseError(
                    _(u"Usuario inactivo"),
                )
        else:

            try:
                # Same as Signin
                user = User.objects.get(email=email)
                if not user.is_active:
                    return ResponseError(
                        _(u"Usuario inactivo"),
                    )
                user.cpprofile.update_device_id(device_id)
            except User.DoesNotExist:
                # Same as Signup
                user = User.objects.create_user(
                    username=generate_random_username(),
                    email=email,
                )
                cp_profile = CPProfile(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    device_id=device_id,
                )
                cp_profile.save()

            fb_profile = FBProfile(
                user=user,
                fb_id=fb_id,
                email=email,
                token=token,
            )
            fb_profile.save()

            user.last_login = now()
            user.save()

            serializer = UserSerializer(user)
            return ResponseSucess(serializer.data)

    @staticmethod
    @csrf_exempt
    @api_view(['GET', 'POST'])
    def reset_password(request):
        if request.method == 'GET':
            query = request.QUERY_PARAMS

            token = query.get('token')
            if not token:
                template = 'accounts/no_token.html'
                return render(request, template, {})

            template = 'accounts/reset_password.html'
            return render(request, template, {})

        elif request.method == 'POST':
            data = request.DATA

            email = data.get('email')
            token = data.get('token')

            if email:
                return AccountView.send_email_reset_password(email)
            elif token:
                return AccountView.validate_reset_password(data)
            else:
                return ResponseError(
                    _(u"No hay información suficiente")
                )

    @staticmethod
    def send_email_reset_password(email):
        students = User.objects.filter(email=email)
        n_students = students.count()
        if n_students == 0:
            return ResponseError(_(u"Email invalido"))
        elif n_students > 1:
            return ResponseError(_(u"Email invalido - ERROR"))
        student = students.first()

        token = default_token_generator.make_token(student)

        cp_profile = student.cpprofile
        cp_profile.password_reset_token = token
        cp_profile.save()

        subject = settings.RESET_PASSWORD_SUBJECT
        url = settings.RESET_PASSWORD_URL.format(
            token=token
        )
        msg = settings.RESET_PASSWORD_MSG.format(
            full_name=cp_profile.get_full_name(),
            url=url
        )
        email_from = settings.RESET_PASSWORD_FROM
        email_to = [student.email]

        send_mail(subject, msg, email_from, email_to, fail_silently=False)

        return ResponseSucess("Envio de correo exitoso")

    @staticmethod
    def validate_reset_password(data):

        token = data.get('token')
        password = data.get('password')

        students = CPProfile.objects.filter(password_reset_token=token)
        n_students = students.count()
        if n_students == 0 or n_students > 1:
            return ResponseError(_(u"Token incorrecto o inválido"))
        if not password or len(password) < 5:
            return ResponseError(_(u"Contraseña invalida"))

        cp_profile = students.first()

        user = cp_profile.user
        user.set_password(password)
        user.save()

        cp_profile.password_reset_token = ''
        cp_profile.save()

        return ResponseSucess("Cambio de contrasenia exitoso")

    @staticmethod
    @api_view(['GET'])
    def get_active_ticket(request, pk):

        student = User.objects.filter(pk=pk)
        if not student.exists():
            return ResponseError(_(u"Usuario invalido"))

        if request.method == 'GET':
            student = student.first()
            ticket = student.cpprofile.active_ticket
            if not ticket:
                return ResponseSucess()
            serializer = TicketSerializer(ticket)
            return ResponseSucess(serializer.data)
