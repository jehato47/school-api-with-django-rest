from django.db.models import Prefetch
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Öğretmen
        fields = '__all__'

    def create(self, validated_data):
        obj = Öğretmen(**validated_data)
        request = self.context.get("request")
        obj.save(using=request.user.email)

        return obj


class TSyllabusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ÖğretmendProgramı
        fields = "__all__"

    def create(self, validated_data):
        obj = ÖğretmendProgramı(**validated_data)
        obj.save(using=validated_data["user"].email)

        return obj

# class AttendanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Yoklama
#         fields = '__all__'
#
#     def create(self, validated_data):
#         # obj = Öğretmen.objects.using(validated_data["user"].email).create(**validated_data)
#         obj = Yoklama(**validated_data)
#         request = self.context.get("request")
#         print(request.user.email)
#         obj.save(using="iz")
#
#         return obj
#
#
# class EtudeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Etüt
#         fields = '__all__'
#
#     def create(self, validated_data):
#         # obj = Öğretmen.objects.using(validated_data["user"].email).create(**validated_data)
#         obj = Etüt(**validated_data)
#         obj.save(using=validated_data["user"].email)
#
#         return obj

# children = Prefetch('child', queryset=Child.objects.select_related('parent'))
# queryset = Parent.objects.prefetch_related(children)

# queryset = Child.objects.filter(parent=parent).select_related('parent')
# serialized_data = ChildSerializer(queryset, many=True, read_only=True, context=self.context)

# # queryset = queryset.prefetch_related('reading_group', 'reading_group__users', 'reading_group__owner')

# Öğretmen.objects.select_related("user")
# Öğretmen.objects.prefetch_related("user")
# Öğretmen.objects.prefetch_related("user").get(id=3)
