from SS_database import Base
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

#NOTE : Table 2 (for storing all the Media related data)
'''
2)Post will include :
    i) Username 
    ii) Caption
    iii) Date
    iv) Image
'''


# class UserBase(Base):
#     __tablename__ = "UserBase"
#     username= Column(String(50), nullable=False)
#     post_id = Column(Integer, nullable=False)
#     caption = Column(String(100), nullable=False)
#     Date = Column(DateTime, server_default=func.now())
#     Image = Column(LargeBinary, nullable=True)
#     ownerID = Column(Integer, ForeignKey("UserRegistration.id", ondelete="CASCADE"), nullable=False)