from fastapi.security import OAuth2PasswordBearer, OAuth2

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
