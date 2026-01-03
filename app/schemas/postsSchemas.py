import base64
from pydantic import BaseModel,field_validator
from datetime import datetime
from typing import Optional




#------------------------------------------------------------------------------------------------
#NOTE :                 CRUD VALIDATION FOR POST creation by users
#------------------------------------------------------------------------------------------------
# --- REVISED APPROACH FOR CLARITY ---
# Because mapping "Image" (bytes) to "image_base64" (str) automatically is tricky
# without extra logic, here is the cleanest implementation:

class PostOut(BaseModel):   #NOTE: this will also work as response model 
    post_id: int
    caption: str
    Created_at: datetime
    ownerID: int
    Image: Optional[str] = None # We will type this as Str to hold Base64

    class Config:
        from_attributes = True

    # Validator to convert the raw bytes from DB into a Base64 string
    @field_validator("Image", mode="before")
    def transform_bytes_to_base64(cls, value):
        if value is None:
            return None
        if isinstance(value, bytes):
            # Convert bytes to base64 string
            return base64.b64encode(value).decode("utf-8")
        return value
    

#------------------------------------------------------------------------------------------------
#NOTE :       Response model for loading all the posts from DB to frontend feed
#------------------------------------------------------------------------------------------------
class ResponseFeed(BaseModel):
    ownerID: int
    Image : Optional[str] = None
    username : str
    caption : str
    Created_at: datetime

    class Config:
        from_attributes = True

# Validator to convert the raw bytes from DB into a Base64 string
    @field_validator("Image", mode="before")
    def transform_bytes_to_base64(cls, value):
        if value is None:
            return None
        if isinstance(value, bytes):
            # Convert bytes to base64 string
            return base64.b64encode(value).decode("utf-8")
        return value