from message.models import Message
from user.models import UserProfile

def create_or_update_message(sender, receiver, contract):
    try:
        sender = UserProfile.objects.get(user=sender)
        receiver = UserProfile.objects.get(user=receiver)
    except:
        return
    
    message_content = ''
    
    is_create_new_message = False
    is_accepted_or_declined = False
    if contract.status == 'CREATED':
        message_content = f'{sender.indentity_number.first_name} {sender.indentity_number.last_name}  создал договор'
        is_create_new_message = True
    elif contract.status == 'SENDED':
        message_content = f'{sender.indentity_number.first_name} {sender.indentity_number.last_name}  вам отправил(-а) договор'
    elif contract.status == 'ACCEPTED':
        is_accepted_or_declined = True
        message_content = f'{sender.indentity_number.first_name} {sender.indentity_number.last_name}  вам принял(-а) договор'
    elif contract.status == 'DECLINED':
        is_accepted_or_declined =  True
        message_content = f'{sender.indentity_number.first_name} {sender.indentity_number.last_name} +  вам отклонил(-а) договор'
    
    if is_create_new_message:
        message = Message.objects.create(sender=sender,
                                     receiver=receiver,
                                     contract=contract,
                                     msg_content=message_content)
    else:
        try:
            message = Message.objects.get(contract=contract)
            if is_accepted_or_declined:
                message.is_archived = True
                message.is_read =True
            message.msg_content = message_content 
        except:
            return
    return message
