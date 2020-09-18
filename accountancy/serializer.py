from rest_framework import serializers
from .models import Muhasebe


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Muhasebe
        fields = "__all__"

    def create(self, validated_data):
        # obj = Öğretmen.objects.using(validated_data["user"].email).create(**validated_data)
        obj = Muhasebe(**validated_data)
        obj.save(using=validated_data["user"].email)

        return obj



