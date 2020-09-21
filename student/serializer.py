from rest_framework import serializers
from .models import *


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Öğrenci
        fields = '__all__'

    def create(self, validated_data):
        obj = Öğrenci(**validated_data)
        obj.save(using=validated_data["user"].email)

        return obj


class SSyllabusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ÖğrencidProgramı
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get("request")
        obj = ÖğrencidProgramı(**validated_data)
        obj.save(using=request.user.email)

        return obj


