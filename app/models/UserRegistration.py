from app.Database.SS_database import Base
from sqlalchemy import Column, Integer, String, BigInteger,DateTime,func,LargeBinary,ForeignKey

#NOTE : Table 1 (for storing all newly registered user's data)
class UserRegistration(Base):
    __tablename__ = "UserRegistration"
    id= Column(Integer, primary_key=True, index= True, autoincrement=True)
    username= Column(String(50), nullable=False)
    email= Column(String(100), unique=True, nullable=False)
    password= Column(String(100), nullable=False)
    gender= Column(String(20), nullable=False)
    contact_no= Column(BigInteger, nullable=True, unique=True)
