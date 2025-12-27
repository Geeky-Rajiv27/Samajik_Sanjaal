from datetime import timedelta, datetime
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from SS_schemas import CreateUser
from SS_database import SessionLocal
from SS_models import UserRegistration
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
import os
from dotenv import load_dotenv  #NOTE: this is required to get system env data
from jose import jwt,JWTError

#------------------------------------------------------------------------------------------------
router  = APIRouter(    #NOTE: This helps to separate the routes of authentication from normal
    #normal CRUD based routes
    prefix = "/auth",   #This means all the routes of this file will starts with /auth
    tags=['Authentication']
)
#------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------
load_dotenv()   #loads variable from .env
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM =  os.environ.get("ALGORITHM" , "HS256")  #("Variable_Name", "default_algorithm_ifNOTfound")
#------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------
#NOTE:          Hashing passwords and recieving tokens from header after authentication
#------------------------------------------------------------------------------------------------
'''
When a user signs up, their password is hashed (converted into an unreadable string).
When logging in, we verify the hashed password.
'''
bcryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto') 
# bcryptContext is now ready and will be used later on for hashing passwords 
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


#------------------------------------------------------------------------------------------------
#NOTE:  Pydantic models for token, sessions, userValidations
#------------------------------------------------------------------------------------------------
#This model is responsible for the User login response with proper format.
class Token(BaseModel):
    access_token : str
    token_type   : str

# -------------------------------------------------------------------------------------------------
# Database dependency
# -------------------------------------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# -------------------------------------------------------------------------------------------------
#NOTE: The create_user endpoint here is for user registration.
#Purpose: Let a new user sign up, hash their password, and store it safely in the database.
#After registration, the user can log in via /auth/token to get a JWT token.
# -------------------------------------------------------------------------------------------------
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, CNU: CreateUser):
    created_User = UserRegistration(
        username=CNU.username,
        password=bcryptContext.hash(CNU.password),  #password is storing hashed password
        email=CNU.email,
        gender=CNU.gender,
        contact_no=CNU.contact_no
    )
    db.add(created_User)
    db.commit()
    db.refresh(created_User)
    return {"msg": "User created successfully", "user_id": created_User.id}



# -------------------------------------------------------------------------------------------------
#NOTE: Login and token Generation -   endpoints
# -------------------------------------------------------------------------------------------------
@router.post("/token/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db : db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not Validate user')
    
    #NOTE: here creating a token with expiry time of 20 minutes
    token = create_access_token(
        user.username,
        user.id,
        timedelta(minutes=20)
        )
    return {
        'access_token': token,
        'token_type': 'bearer'
           }


# -------------------------------------------------------------------------------------------------
# Authenticate user #NOTE: this function will be called !
# -------------------------------------------------------------------------------------------------
def authenticate_user(username: str, password: str , db):
    user = db.query(UserRegistration).filter(UserRegistration.username ==  username).first()
    if not user:
        return False
    if not bcryptContext.verify(password, user.password):
        return False
    return user
    

# -------------------------------------------------------------------------------------------------
#NOTE:  Creating JWT Tokens
# -------------------------------------------------------------------------------------------------
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    payload = {
        "sub" : username,
        "id"  : user_id,
        "exp" : datetime.utcnow() + expires_delta
    }
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not set in environment variables")

    return jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

# -------------------------------------------------------------------------------------------------
# #NOTE : Allowing authorized users to access the protected routes
# ----------------------------------------------------------------------------------------------
def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
    db: db_dependency
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(UserRegistration).filter(
        UserRegistration.id == user_id
    ).first()

    if user is None:
        raise credentials_exception

    return user


@router.get("/me")
async def read_own_profile(current_user: Annotated[UserRegistration, Depends(get_current_user)]):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "gender": current_user.gender,
        "contact_no": current_user.contact_no
    }
