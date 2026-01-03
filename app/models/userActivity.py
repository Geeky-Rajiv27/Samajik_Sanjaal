from app.Database.SS_database import Base
from sqlalchemy import Column, Integer, String, BigInteger,DateTime,func,LargeBinary,ForeignKey

#------------------------------------------------------------------------------------
#NOTE : Table 3 : this table will include all Useractiviry features

class UserActivity(Base):
    __tablename__ = "UseraActivity"
    id=Column(Integer, primary_key=True, index=True)    #this for count of activity in table
    #NOTE: this user_id will be same as in table 1 
    user_id=Column(Integer,ForeignKey("UserRegistration.id", ondelete="CASCADE"),nullable=False)
    event_type = Column(String(50), nullable=False)
    event_name = Column(String(100), nullable=True)
    post_id=Column(Integer, ForeignKey("UserPost.post_id", ondelete="SET NULL"), nullable=True)
    created_at=Column(DateTime, server_default=func.now())
