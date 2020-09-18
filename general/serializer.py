from rest_framework import serializers
from .models import *


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duyuru
        fields = '__all__'

    def create(self, validated_data):
        # obj = Duyuru.objects.using(request.user.email).create(**validated_data)
        request = self.context.get("request")
        obj = Duyuru(**validated_data)
        obj.save(using=request.user.email)

        return obj


