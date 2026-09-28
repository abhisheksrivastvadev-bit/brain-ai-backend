from app.core.security import create_access_token


token = create_access_token(123)

print(token)