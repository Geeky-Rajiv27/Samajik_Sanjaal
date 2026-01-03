from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional




#------------------------------------------------------------------------------------------------
#NOTE :                 CRUD VALIDATION 
#------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------
# INPUT schema (NO id)
# -------------------------------------------------------------------------------------------------------
class CreateUser(BaseModel):
    username : str = Field(..., min_length=3, max_length=20)    #NOTE: this is latesh  instead of
    email : EmailStr    # constr we should use Field(...,min_length =  ,max_length =  )
    password : str = Field(..., min_length=6)
    gender : str
    contact_no : int
    
    model_config = {
        "from_attributes": True
    }
    
    #NOTE: In V1, orm_mode = True tells Pydantic:   “I will give you SQLAlchemy ORM objects.
    #  Read attributes from them.” #NOTE: this converts dictionary into json

# -------------------------------------------------------------------------------------------------------
# OUTPUT schema (WITH id)
# -------------------------------------------------------------------------------------------------------
class UserResponse(CreateUser):   # inheriting from the StudentSchema
    id : Optional[int] = None
    

    model_config = {
        "from_attributes": True
    }


