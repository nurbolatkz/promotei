from django.urls import path
from contract.views import CreateContract, ContractViewSet

contract_detail = ContractViewSet.as_view({'post': 'set_signed'})

urlpatterns = [
    path('create_contract/', CreateContract.as_view(), name='creatcontract'),
    path('approve/<str:contract_id>', contract_detail, name='approve')
]