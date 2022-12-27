from django.urls import path
from contract.views import CreateContract

urlpatterns = [
    path('create_contract/', CreateContract.as_view(), name='creatcontract'),
]