from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def hash_text(text: str):
        return pwd_ctx.hash(text)

    def verify_hased_text(plain_text: str, hashed_text: str):
        return pwd_ctx.verify(plain_text, hashed_text)
