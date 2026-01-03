from fastapi import FastAPI, Depends, HTTPException
from app.Database.SS_database import Base, SessionLocal, engine
from app.models.UserRegistration import UserRegistration
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.schemas.RegistrationSchema import CreateUser,UserResponse
import app.routers.auth as auth
from app.routers import posts
# import app.routers.activity as activity


from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware


#---------------------------------------------------------------------------------
#               CORS SETUP --  CORS setup and endpoint handling in your main.py so your
#                                    frontend can talk to FastAPI properly.
#---------------------------------------------------------------------------------

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://127.0.0.1:5500",  # your frontend URL (or "*" to allow all)
    "http://localhost:5500",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],    # allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

#------------------------------------------------------------------------

Base.metadata.create_all(bind=engine)

#------------------------------------------------------------------------
#NOTE: # Register the Auth routes (register, login, me)
# These will all start with /auth because of the prefix in auth.py
app.include_router(auth.router)  #To include the mini app "router" for tokens validation

# Register the Post routes (create, delete, etc.)
# We add the prefix here or inside posts.py (choose one)
app.include_router(posts.router)

# Register Activity routes
# app.include_router(activity.router, prefix="/activity", tags=["Activity"])
#------------------------------------------------------------------------

#NOTE: creating database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

   
#------------------------------------------------------------------------------------------------
# NOTE:             ALL CRUD OPERATIONS (ENDPOINTS)
#------------------------------------------------------------------------------------------------

#NOTE : THis retrives [] empty json since db is empty
@app.get("/Users",response_model=List[UserResponse])
def get_users(db:Session = Depends(get_db)):
    return db.query(UserRegistration).all()     #This will retrive all db data


#------------------------------------------------------------------------------------------------
#NOTE :Creating a model to create a document of a student
#------------------------------------------------------------------------------------------------
@app.post("/CreateUser", response_model=UserResponse)
def create_User(UserData: CreateUser, db:Session = Depends(get_db)):
    bcryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
    u=UserRegistration(
        username=UserData.username,
        email=UserData.email,
        password=bcryptContext.hash(UserData.password),
        gender=UserData.gender,
        contact_no=UserData.contact_no
        )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

#------------------------------------------------------------------------------------------------
#NOTE: To retrieve data of specific users via id.
#------------------------------------------------------------------------------------------------
@app.get("/user/{User_id}")
def UserbyID(User_id: int, db: Session = Depends(get_db)):   #get method doesn't accpet request body i.e: CreateUser
    UserData = db.query(UserRegistration).filter(UserRegistration.id == User_id).first()
    if not UserData:
        raise HTTPException(status_code=404, detail=f"User with id:{User_id} not available.")
   
    return{
        "msg" : f"The detail of user with id:{User_id}",
        "Data": UserData
    }

#------------------------------------------------------------------------------------------------
#NOTE: Update
#------------------------------------------------------------------------------------------------
@app.put("/UpdateUser/{User_id}")
def UpdateUserbyID(UserData: CreateUser, User_id: int, db: Session = Depends(get_db)):
    fetched_user = db.query(UserRegistration).filter(UserRegistration.id == User_id).first()
    if not fetched_user:
        raise HTTPException(status_code=404, detail=f"User with id:{User_id} not available.")
    bcryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')

    fetched_user.username = UserData.username
    fetched_user.email = UserData.email
    fetched_user.password = bcryptContext.hash(UserData.password)
    fetched_user.gender = UserData.gender
    fetched_user.contact_no = UserData.contact_no

    db.commit()
    db.refresh(fetched_user)
    return {
        "Server" : f"User with ID:{User_id} is successfully updated."
    }

#------------------------------------------------------------------------------------------------
#NOTE: Delete specific User via id 
#------------------------------------------------------------------------------------------------
@app.delete("/DeleteUser/{User_id}")
def DeleteUserbyID(User_id: int, db : Session = Depends(get_db)):
    fetched_user = db.query(UserRegistration).filter(UserRegistration.id == User_id).first()
    if not fetched_user:
        raise HTTPException(status_code=404, detail=f"User with id:{User_id} not available.")
    db.delete(fetched_user)
    db.commit()
    #db.refresh(fetched_user) #NOTE : don't do this because this tires to re-read the deleted row
    return {
        "Server" : f"User with ID:{User_id} is successfully deleted."
    }
