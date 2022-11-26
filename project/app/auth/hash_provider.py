from passlib.context import CryptContext

pwd = CryptContext(schemes=['bcrypt'])

def gerar_hash(texto):
    return pwd.hash(texto)

def verificar_hash(texto, hash):
    return pwd.verify(texto, hash)

