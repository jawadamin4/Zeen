# zeen_app/serializers.py

from rest_framework import serializers
from .models import Application, Degree


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    degrees = DegreeSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['degrees'] = DegreeSerializer(instance.degrees.all(), many=True).data
        return representation


