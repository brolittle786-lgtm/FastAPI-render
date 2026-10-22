from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer 

SECRETE_KEY = "my_secrete"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_Schema = OAuth2PasswordBearer(tokenUrl="login")

# create token 
def create_token(data : dict):
    to_encode =  data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    return jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)

def verify_token(token:str = Depends(oauth2_Schema)):
    try :
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")