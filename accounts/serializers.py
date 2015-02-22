# coding=utf-8

from django.contrib.auth.models import User

from rest_framework import serializers

from utils.serializers import CPBaseSerializer


class UserSerializer(CPBaseSerializer):
    student_id = serializers.Field(source='pk')
    first_name = serializers.Field(source='cpprofile.first_name')
    last_name = serializers.Field(source='cpprofile.last_name')

    class Meta:
        model = User
        fields = (
            'id',
            'student_id',
            'first_name',
            'last_name',
            'email',
            # 'fb_id',
            # 'access_token',
        )
