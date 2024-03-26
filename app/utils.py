from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def password_hasher(password: str):
    return pwd_context.hash(password)

def pass_verifier(simple_password, hashed_password): 
    return pwd_context.verify(simple_password, hashed_password)