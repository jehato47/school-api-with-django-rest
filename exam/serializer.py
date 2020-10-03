from rest_framework import serializers
from .models import OkulSınav


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = OkulSınav
        fields = "__all__"

    def create(self, validated_data):
        obj = OkulSınav(**validated_data)
        obj.save(using=validated_data["user"].email)
        return obj
