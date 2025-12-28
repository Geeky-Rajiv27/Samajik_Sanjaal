from SS_database import Base
from sqlalchemy import Column, Integer, String, BigInteger,DateTime,func,LargeBinary

#NOTE : Table 1 (for storing all newly registered user's data)
class UserRegistration(Base):
    __tablename__ = "UserRegistration"
    id= Column(Integer, primary_key=True, index= True, autoincrement=True)
    username= Column(String(50), nullable=False)
    email= Column(String(100), unique=True, nullable=False)
    password= Column(String(100), nullable=False)
    gender= Column(String(20), nullable=False)
    contact_no= Column(BigInteger, nullable=True, unique=True)

#NOTE : Table 2 (for storing all the Media related data)
'''
2)Post will include :
    i) Username 
    ii) Caption
    iii) Date
    iv) Image
'''

