from rest_framework import serializers
from contract.models import Contract
from user.models import CustomUser
from document.models import IdentityNumber
from rest_framework.generics import get_object_or_404
class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        
        
    def validate(self, attrs):
        if attrs['content'] is None:
            raise serializers.ValidationError('File is not found')
        return attrs
    
    
    def create(self, validated_data):
        user = self.context.get('request').user
        if user:
            renter = user
        receiver = CustomUser.objects.get(indentity_number=validated_data['receiver'])
        contract = Contract.objects.create(content=validated_data['content'],
                                           renter=renter,
                                           receiver=receiver)
        contract.save()
        return contract
        