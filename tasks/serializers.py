# coding=utf-8

from rest_framework import serializers

from .models import Problem, TaskTopic, Task
from utils.serializers import CPBaseSerializer


class ProblemSerializer(CPBaseSerializer):
    problem_id = serializers.Field(source='pk')

    class Meta:
        model = Problem
        fields = (
            'id',
            'problem_id',

            'number',
            'pdf',
        )


class TaskTopicSerializer(CPBaseSerializer):
    tasktopic_id = serializers.Field(source='pk')
    problems = ProblemSerializer(many=True)

    class Meta:
        model = TaskTopic
        fields = (
            'id',
            'tasktopic_id',

            'name',
            'icon',
            'problems',
        )


class TaskSerializer(CPBaseSerializer):
    task_id = serializers.Field(source='pk')
    task_topics = TaskTopicSerializer(many=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'task_id',

            'task_topics',
        )
