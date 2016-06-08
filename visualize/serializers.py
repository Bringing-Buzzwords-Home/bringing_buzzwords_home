from rest_framework import serializers
from .models import State


class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
