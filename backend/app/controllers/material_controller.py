from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
import shutil
import os

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.material import Material

router = APIRouter(prefix="/api/materials", tags=["Materials"])

os.makedirs("uploads/materials", exist_ok=True)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_material(
    title: str = Form(...),
    course_code: str = Form(...),
    file_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file_location = f"uploads/materials/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    existing = db.query(Material).filter(
        Material.title == title, 
        Material.course_code == course_code
    ).order_by(Material.version.desc()).first()
    
    new_version = existing.version + 1 if existing else 1

    new_material = Material(
        title=title,
        course_code=course_code,
        file_url=file_location,
        file_type=file_type,
        version=new_version,
        uploader_id=current_user.id
    )
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    
    return {"message": "Material uploaded successfully", "material_id": new_material.material_id, "version": new_version}

@router.get("/")
def get_materials(course: str = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Material)
    if course:
        query = query.filter(Material.course_code == course)
    return query.order_by(Material.created_at.desc()).all()