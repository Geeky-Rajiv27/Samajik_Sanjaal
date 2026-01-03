from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Annotated,List
from app.routers.auth import UserRegistration,get_current_user
from app.schemas.postsSchemas import PostOut, ResponseFeed
from app.Database.SS_database import get_db
# import models, schemas # Your files
from app.models.UserPost import UserPost
# from app.routers.auth import router 
router = APIRouter(
    prefix="/posts",
    tags=['AuthenticatedPost']
)


#-----------------------------------------------------------------------------------------------------
#NOTE:  --- Profile Search ---
#-----------------------------------------------------------------------------------------------------

@router.get("/profile")
async def read_own_profile(current_user: Annotated[UserRegistration, Depends(get_current_user)]):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "gender": current_user.gender,
        "contact_no": current_user.contact_no
    }

#-----------------------------------------------------------------------------------------------------
#NOTE:  --- CREATE POST ---
#-----------------------------------------------------------------------------------------------------

@router.post("/create", response_model=PostOut)
async def create_post(
    caption: str = Form(...),          # Match Postman Key
    image: UploadFile = File(None),    # Match Postman Key
    owner_id: int = Form(...),         # Match Postman Key
    db: Session = Depends(get_db)

):
    image_bytes = await image.read() if image else None

    # Map function arguments to EXACT Model/DB column names
    new_post = UserPost(
        caption=caption,
        Image=image_bytes,  # Map arg 'image' to Model 'Image'              # Saving raw bytes to DB
        ownerID=owner_id    # Map arg 'owner_id' to Model 'ownerID'
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post     # 4. Return (Pydantic will automatically convert the bytes to Base64 via the validator)


#-----------------------------------------------------------------------------------------------------
#NOTE:  ---Load posts in feed ENDPOINTS ---
#-----------------------------------------------------------------------------------------------------

@router.get("/feed/posts", response_model=List[ResponseFeed])
async def LoadFeed_post(db: Session = Depends(get_db)):
    feedpost = (
        db.query(
             UserPost.ownerID,
            UserPost.caption,
            UserPost.Created_at,
            UserPost.Image,
            UserRegistration.username
        )
        .join(UserRegistration, UserRegistration.id == UserPost.ownerID).all()
    )
    return feedpost


#-----------------------------------------------------------------------------------------------------
#NOTE:  ---Search bar  ENDPOINTS ---
#-----------------------------------------------------------------------------------------------------