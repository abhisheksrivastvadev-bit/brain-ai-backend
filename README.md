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

#### How to create PostgreSQL database
- Step 1 — Check whether PostgreSQL is installed
    - `psql --version`
- Step 2 — Install PostgreSQL
    - `brew install postgresql@17`
- Step 3 — Start PostgreSQL service
    - `brew services start postgresql@17`
- Step 4 — Verify installation
    - `psql --version`
- Step 5 — Create the Brain AI database
    - `createdb brain_ai`
- Step 6 - then verify
    - `psql -l`
- Step 7 - Test the connection
    - `psql -U abhisheksrivastva -d brain_ai`
- Step 8 - check the current database with: 
    - `SELECT current_database()`
- Step 9 - exit the database
    - `\q`

#### How to install PGAmdin GUI tool
- Step 1 -  `brew install --cask pgadmin4`
- STEP 2 - `open -a "pgAdmin 4"`


#### Kill already running server
1. lsof -i :8000: output will be PID = 12345
2. kill 12345


    