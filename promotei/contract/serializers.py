from rest_framework import serializers
from contract.models import Contract
from user.models import CustomUser
from document.models import IdentityNumber

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        
        
    def validate(self, attrs):
        if attrs['content'] is None:
            raise serializers.ValidationError('File is not found')
        return attrs
    
    
    def create(self, validated_data):
        print(validated_data['renter'])
        #renter = IdentityNumber.objects.get(pk=validated_data['renter'])
        #receiver = IdentityNumber.objects.get(pk=validated_data['receiver'])
        contract = Contract.objects.create(content=validated_data['content'],
                                           renter=validated_data['renter'],
                                           receiver=validated_data['receiver'])
        contract.save()
        return contract
        