#### How does the JWT actually work?
- A JWT has three parts:
    * HEADER.PAYLOAD.SIGNATURE
    - Header
        * {
        "alg": "HS256",
        "typ": "JWT"
        }
    - Payload
        * {
        "sub": "123",
        "exp": 1790600000
        }
    - Signature
        * HMAC-SHA256 (Hash of Header + Payload + Secret Key)

#### How does it verify identity?
- After login 
    - Backend creates JWT token
    - sends back to frontend
    - On every request, frontend sends JWT in Authorization header
    - Backend verifies token signature
    - If valid, serves request
    - If invalid, returns 401 Unauthorized

#### Libraray for JWT and password hash 
- `pip install pyjwt`
- `pip install pwdlib[argon2]`
    
#### How to run this project
- `uvicorn app.main:app --reload`
