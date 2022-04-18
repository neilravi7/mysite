import os
from cryptography.fernet import Fernet

# Url encoding decoding to hide parameters.


def url_encode_utils(target_data, target_action):
    key = bytes(os.environ.get('ENC_SECRET'), 'utf-8')
    f = Fernet(key)
    if target_action == "encode":
        target_data = bytes(target_data, 'utf-8')
        return f.encrypt(target_data)
    elif target_action == "decode":
        target_data = target_data.encode()
        return f.decrypt(target_data).decode()
