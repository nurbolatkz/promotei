from message.models import Message

def create_or_update_message(sender, receiver, contract):
    message_content = ''
    if contract.status == 'SENDED':
        message_content = f'{sender.first_name} {sender.last_name} +  вам отправил(-а) договор'
    elif contract.status == 'ACCEPTED':
        message_content = f'{sender.first_name} {sender.last_name} +  вам принял(-а) договор'
        message =  Message.objects.filter(sender=sender, contract=contract, receiver=receiver)
        if message:
            message.msg_content =  message_content
            message.save()
            return message
    elif contract.status == 'DECLINED':
        message_content = f'{sender.first_name} {sender.last_name} +  вам отклонил(-а) договор'
        message_content = f'{sender.first_name} {sender.last_name} +  вам принял(-а) договор'
        message =  Message.objects.filter(sender=sender, contract=contract, receiver=receiver)
        if message:
            message.msg_content =  message_content
            message.save()
            return message
        
    message = Message.objects.create(sender=sender,
                                     receiver=receiver,
                                     contract=contract,
                                     msg_content=message_content)
    return message