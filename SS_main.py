from fastapi import FastAPI, Depends, HTTPException
from SS_database import Base, SessionLocal, engine
from SS_models import UserRegistration
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from SS_schemas import CreateUser,UserResponse
import SS_Oauth as Oauth
from passlib.context import CryptContext


Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(Oauth.router)  #To include the mini app "router" for tokens validation

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