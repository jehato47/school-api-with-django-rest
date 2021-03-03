from rest_framework import serializers
from .models import OkulSınav, ExcelForm


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = OkulSınav
        fields = "__all__"

    def create(self, validated_data):
        obj = OkulSınav(**validated_data)
        obj.save(using=validated_data["user"].email)
        return obj


class ExcelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelForm
        fields = "__all__"

    def create(self, validated_data):
        obj = ExcelForm(**validated_data)
        obj.save(using=validated_data["user"].email)
        return obj
