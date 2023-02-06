from passlib.context import CryptContext

# lets create an instance of CryptContext 
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class Hash():
    def bcrypt(password: str):
        return pwd_context.hash(password)