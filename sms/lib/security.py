from cryptography.fernet import Fernet


class Security:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.fernet = None
        
    def encrypt(self, message):
        fernet = Fernet(self.key)
        encoded = fernet.encrypt(message.encode())
        key =  self.key.decode('utf-8')
        enc_message = encoded.decode("utf-8")
        return enc_message, key

    def decrypt(self, message, key):
        message  = bytes(message, 'utf-8')
        key = bytes(key, 'utf-8')
        fernet = Fernet(key)
        message = fernet.decrypt(message).decode()
        return message
        
