from rest_framework import serializers
from .models import Yönetici


class YöneticiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yönetici
        fields = "__all__"

    def create(self, validated_data):
        # obj = Öğretmen.objects.using(validated_data["user"].email).create(**validated_data)
        print(validated_data)
        obj = Yönetici(**validated_data)
        obj.save(using=validated_data["user"].email)

        return obj
