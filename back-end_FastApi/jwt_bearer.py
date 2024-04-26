from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt_handler import decodeJWT

class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error:bool=True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)
        
    async def __call__(self, request:Request):
        credentials : HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request=request)
        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or Expired Token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or Expired Token!")
        
    def verify_jwt(self, jwtoken:str):
        isTokenValid: bool = False # a false flag
        payload = decodeJWT(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid