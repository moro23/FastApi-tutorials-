from passlib.context import CryptContext

# lets create an instance of CryptContext 
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class Hash():
    def get_password_hash(password: str):
        return pwd_context.hash(password)

    def verify(hashed_password, plain_password):
        return pwd_context.verify(plain_password, hashed_password)