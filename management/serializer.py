from rest_framework import serializers
from .models import *


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yoklama
        fields = '__all__'

    def create(self, validated_data):
        # obj = Öğretmen.objects.using(validated_data["user"].email).create(**validated_data)
        obj = Yoklama(**validated_data)
        request = self.context.get("request")
        obj.save(using=request.user.email)

        return obj


class EtudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etüt
        fields = '__all__'

    def create(self, validated_data):
        # obj = Öğretmen.objects.using(validated_data["user"].email).create(**validated_data)
        obj = Etüt(**validated_data)
        obj.save(using=validated_data["user"].email)
        return obj


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ödev
        fields = '__all__'

    def create(self, validated_data):
        # obj = Öğretmen.objects.using(validated_data["user"].email).create(**validated_data)
        obj = Ödev(**validated_data)
        request = self.context.get("request")
        obj.save(using=request.user.email)

        return obj
