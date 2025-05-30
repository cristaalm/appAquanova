# en historiales/serializers.py
from rest_framework import serializers
from historiales.models import Historial

class HistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historial
        fields = '__all__'
