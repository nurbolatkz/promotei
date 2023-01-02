from document.models import Esp
import hashlib


def check_esp(file):
    md5 = hashlib.md5()
    content = bytes(file.read())
    md5.update(content)
    hash = md5.hexdigest()
    
    try:
        instance = Esp.objects.get(hash=hash)
        if instance:
            return True
    except:
        return False