from app.Database.SS_database import Base
from sqlalchemy import Column, Integer, String, BigInteger,DateTime,func,LargeBinary,ForeignKey


#------------------------------------------------------------------------------------
#NOTE : Table 2 (for storing all the Media related data)
'''
2)Post will include :
    i) Username 
    ii) Caption
    iii) Date
    iv) Image
'''


class UserPost(Base):
    __tablename__ = "UserPost"
    post_id = Column(Integer, nullable=False, primary_key=True, index=True)
    caption = Column(String(100), nullable=False)
    Created_at = Column(DateTime, server_default=func.now())
    Image = Column(LargeBinary, nullable=True)
    ownerID = Column(
        Integer, ForeignKey("UserRegistration.id", ondelete="CASCADE"),
          nullable=False
          )