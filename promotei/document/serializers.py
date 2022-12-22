from rest_framework import serializers
from document.models import IdentityNumber

class IdentityNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityNumber
        fields = [
            'indentity_number',
            'date_of_birth',
            'first_name',
            'last_name',
            'patronymic',
            'region',
            'city'
        ]