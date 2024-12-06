from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # This should validate JWT; for simplicity, mock validation is used.
    if token != "fake-jwt-token":
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return {"userId": "12345", "role": "reporter"}