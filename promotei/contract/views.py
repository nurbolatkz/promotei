from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from contract.models import Contract
from contract.serializers import ContractSerializer
from rest_framework.decorators import action
from document.utils import check_esp
from message.utils import create_or_update_message
from django.http import FileResponse
import pathlib
from contract.models import ContractTemplate

class CreateContract(generics.CreateAPIView):
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ContractSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        return Response({
            'status': 200,
            'message': 'Successfully created contract, to send the contract to the recipient, approve it using esp',
            'data': response.data
        })
    

class ContractViewSet(viewsets.ViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]
    queryset = Contract.objects.all()


    @action(detail=True, methods=['get'])
    def set_signed(self, request, contract_id=None):
        if contract_id is None:
            return Response({'Error': 'Contract id is not provided'}, 404)
       
        
        content = request.FILES['esp']
        if check_esp(content):
            try:
                contract = self.queryset.get(pk=contract_id)
            except:
                return Response('Contract with this id not found',404)
            
            user_id = request.user.id
            
            if user_id == contract.renter.id:
                contract.is_signed_by_renter = True
                contract.status = 'SENDED'
            elif user_id == contract.receiver.id:
                contract.is_signed_by_receiver = True
                contract.status= 'RECEIVED'
            contract.save()
            
        else:
            return Response('ESP does not correctly entered or check expiration date', 404)
        
        
        serializer = ContractSerializer(contract)
        return Response(serializer.data, 201)
    
    
    @action(detail=True, methods=['get'])
    def set_accepted(self, request, contract_id=None):
        if contract_id is None:
            return Response({'Error': 'Contract id is not provided'}, 404)
       
        try:
            content = request.FILES['esp']
        except:
            return Response({'Error': 'Esp not provided'})
        if check_esp(content):
            try:
                contract = self.queryset.get(pk=contract_id)
            except:
                return Response('Contract with this id not found',404)
            
            user_id = request.user.id
            
            if user_id == contract.receiver.id:
                if contract.is_signed_by_receiver == True and contract.is_signed_by_renter == True:
                    contract.status = 'ACCEPTED'
                message.save()
            else:
                return Response('Contract can accept only receiver',403)
            
            
            message = create_or_update_message(sender=contract.renter, receiver=contract.receiver, contract=contract)
            if message:
                message.is_read =  True
                message.is_archived = True
                message.save()
            
        else:
            return Response('ESP does not correctly entered or check expiration date', 404)
        
        
        serializer = ContractSerializer(contract)
        return Response(serializer.data, 201)
    
    
    @action(detail=True, methods=['get'])
    def set_declined(self, request, contract_id=None):
        if contract_id is None:
            return Response({'Error': 'Contract id is not provided'}, 404)
       
        try:
            contract = self.queryset.get(pk=contract_id)
        except:
            return Response('Contract with this id not found',404)
            
            
        user_id = request.user.id
            
        if user_id == contract.receiver.id:
            if contract.is_signed_by_receiver == True or contract.is_signed_by_renter == True:
                contract.status = 'DECLINED'
                
                contract.save()
        else:
            return Response('Contract can accept only receiver',403)
            
        message = create_or_update_message(sender=contract.renter, receiver=contract.receiver, contract=contract)
            
        if message:
            message.is_read =  True
            message.is_archived = True
            message.save()
        else:
            return Response('ESP does not correctly entered or check expiration date', 404)
        
        
        serializer = ContractSerializer(contract)
        return Response(serializer.data, 201)
    
    
    def contract_download(self, request, contract_id, *args, **kwargs):
        if contract_id is None:
            return Response({'Error': 'contract was not provided'})
        try:
                contract = self.queryset.get(pk=contract_id, receiver=request.user)
               
        except:
                return Response('Contract with this id not found',404)
        content = contract.content
        extension = pathlib.Path(content.name).suffix
        #filename_with_extension = "{0}{1}".format('Договор', extension)
        #return FileResponse(content.open(), as_attachment=True, filename=filename_with_extension)
        return Response({'url': content.url}, status=200)

    
    def template_download(self, request, *args, **kwargs):
        template = ContractTemplate.objects.all().order_by('created_at')
        if template:
            template = template[0]
        return Response({'url': template.contract_template.url}, status=200)
    