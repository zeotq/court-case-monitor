from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models.user import UserDB, UserCreate, UserOut
from app.models.organisation import OrganisationDB
from app.models.task import TaskDB
from app.database import get_db

account_router = APIRouter(prefix="/account", tags=["account"])


@account_router.get("/self", response_model=UserOut, response_class=JSONResponse)
async def get_user_profile(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
) -> JSONResponse:
    user = db.query(UserDB).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@account_router.post("/self", response_model=UserOut, response_class=JSONResponse)
async def update_user_profile(
    user_data: UserCreate,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
) -> JSONResponse:
    user = db.query(UserDB).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Обновим email и username (если нужно)
    user.email = user_data.email
    user.username = user_data.username

    # === Обновляем организации ===
    new_organisations = []
    for org_data in user_data.organisations or []:
        org = db.query(OrganisationDB).filter_by(inn=org_data.inn).first()
        if not org:
            org = OrganisationDB(**org_data.dict())
            db.add(org)
            db.commit()
            db.refresh(org)
        new_organisations.append(org)
    user.organisations = new_organisations

    # === Обновляем задачи ===
    db.query(TaskDB).filter(TaskDB.user_id == user.id).delete()
    db.commit()
    for task_data in user_data.tasks or []:
        task = TaskDB(title=task_data.title, user_id=user.id)
        db.add(task)
    db.commit()

    db.refresh(user)
    return user
