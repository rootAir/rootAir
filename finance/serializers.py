from django.contrib.auth.models import User, Group
from rest_framework import serializers
from finance.week_number import WeekNumber


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class WeekNumberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WeekNumber
        fields = ('id', 'num_week', 'date_closed')