from datetime import datetime, timedelta

from jose import jwt

#CONFIG
SECRET_KEY = '53729345f0c6a558f710bd1756c6f2a8'
ALG = 'HS256'
EXP_MIN = 900

def create_access_token(data: dict):
    dados = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=EXP_MIN)
    dados.update({'exp': expira})
    
    token_jwt = jwt.encode(dados, SECRET_KEY, algorithm=ALG)
    return token_jwt

def verify_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALG)
    return payload.get('sub')