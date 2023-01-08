from rest_framework import serializers
from contract.models import Contract
from user.models import CustomUser
from document.models import IdentityNumber
from rest_framework.generics import get_object_or_404
from message.utils import create_or_update_message


class ContractSerializer(serializers.ModelSerializer):
    receiver = serializers.CharField( required=True)
    is_signed_by_renter = serializers.BooleanField(read_only=True)
    is_signed_by_receiver = serializers.BooleanField(read_only=True)
    status = serializers.CharField(read_only=True)
    class Meta:
        model = Contract
        fields = [
            'id',
            'receiver',
            'content',
            'is_signed_by_renter',
            'is_signed_by_receiver',
            'status'
        ]
        
        
    def validate(self, attrs):
        if attrs['content'] is None:
            raise serializers.ValidationError('File is not found')
        return attrs
    
    
    def create(self, validated_data):
        user = self.context.get('request').user
        if user:
            renter = user
        
        receiver_identity_number = get_object_or_404(IdentityNumber,
                                                     indentity_number=validated_data['receiver'])
        
        receiver = CustomUser.objects.get(indentity_number=receiver_identity_number)
        contract = Contract.objects.create(content=validated_data['content'],
                                           renter=renter,
                                           receiver=receiver)
        contract.save()
        message = create_or_update_message(sender=user, receiver=receiver,contract=contract)
        if message:
            message.save()
        
        return contract
        