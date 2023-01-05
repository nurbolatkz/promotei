from django.urls import path
from contract.views import CreateContract, ContractViewSet

contract_detail = ContractViewSet.as_view({'post': 'set_signed'})
contract_accept = ContractViewSet.as_view({'post': 'set_accepted'})
contract_declined = ContractViewSet.as_view({'post': 'set_declined'})
contract_download = ContractViewSet.as_view({'get': 'contract_download'}) 

urlpatterns = [
    path('create_contract/', CreateContract.as_view(), name='creatcontract'),
    path('approve/<str:contract_id>', contract_detail, name='approve'),
    path('accept/<str:contract_id>', contract_accept, name='accept_contract'),
    path('decline/<str:contract_id>', contract_declined, name='decline_contract'),
    path('download/<str:contract_id>', contract_download, name='contract_download')
    
]