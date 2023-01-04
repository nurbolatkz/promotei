from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from contract.models import Contract
from contract.serializers import ContractSerializer
from rest_framework.decorators import action
from document.utils import check_esp


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
                contract.is_signed = True
                contract.status = 'SENDED'
                # SEND NOTITIFICATION
                contract.save()
            except:
                return Response('Contract with this id not found',404)
        else:
            return Response('ESP does not correctly entered or check expiration date', 404)
        
        
        serializer = ContractSerializer(contract)
        return Response(serializer.data, 201)
    
    @action(detail=True, methods=['get'])
    def set_accepted(self, request, contract_id=None):
        if contract_id is None:
            return Response({'Error': 'Contract id is not provided'}, 404)
       
        
        content = request.FILES['esp']
        if check_esp(content):
            try:
                contract = self.queryset.get(pk=contract_id)
                if contract.is_signed == True:
                    contract.status = 'ACCEPTED'
                    #SEND_MESSAGE
                    # TEST receiver with request user
                contract.save()
            except:
                return Response('Contract with this id not found',404)
        else:
            return Response('ESP does not correctly entered or check expiration date', 404)
        
        
        serializer = ContractSerializer(contract)
        return Response(serializer.data, 201)
    
    @action(detail=True, methods=['get'])
    def set_declined(self, request, contract_id=None):
        if contract_id is None:
            return Response({'Error': 'Contract id is not provided'}, 404)
       
        
        content = request.FILES['esp']
        if check_esp(content):
            try:
                contract = self.queryset.get(pk=contract_id)
                if contract.is_signed == True:
                    contract.status = 'DECLINED'
                    #SEND_MESSAGE
                    # TEST receiver with request user
                contract.save()
            except:
                return Response('Contract with this id not found',404)
        else:
            return Response('ESP does not correctly entered or check expiration date', 404)
        
        
        serializer = ContractSerializer(contract)
        return Response(serializer.data, 201)       