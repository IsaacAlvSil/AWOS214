from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import status, HTTPException, Depends

#seguridad
security = HTTPBasic()
def verificar_Peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "isaac")
    passAuth = secrets.compare_digest(credenciales.password, "123")

    if not(userAuth and passAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "credenciales no autorizadas"
        )
    return credenciales.username
