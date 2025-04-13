from fastapi import status, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Annotated
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import AuthUserCreate, UserDB
from app.database import get_db
from app.services.cache import create_auth_code, validate_auth_code, delete_auth_code
from app.services.jwt_validation import refresh_cookie_validation
from app.services.is_banned import raise_if_user_banned
from app.utils.jwt import create_access_token, create_refresh_token, get_expiration_time
from app.utils.auth import get_password_hash, verify_password
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS


async def authenticate_user(
        username: str, 
        password: str,
        db: Session 
    ) -> UserDB:
    try:
        user = db.query(UserDB).filter(UserDB.username == username).first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
    
    if not user:
            return None
    
    raise_if_user_banned(user)
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def authorize_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        code_challenge: str,
        callback_uri: str,
        db: Session,
    ) -> JSONResponse:
    
    user = await authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    code = create_auth_code(user.username, code_challenge)

    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"code": code, "callback_uri": callback_uri}
    )

    return response
    

async def exchange_code_for_tokens(
        code: str,
        code_verifier: str,
        callback_uri: str
    ) -> JSONResponse:

    user_auth_data = validate_auth_code(code, code_verifier)
    delete_auth_code(code)

    if not user_auth_data or not 'user_id' in user_auth_data:
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    access_token_expires = get_expiration_time(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token_expires = get_expiration_time(timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    access_token = await create_access_token({'sub': user_auth_data['user_id']}, expiry_date=access_token_expires)
    refresh_token = await create_refresh_token({'sub': user_auth_data['user_id']}, expiry_date=refresh_token_expires)

    response = JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"access_token": access_token, 
                 "token_type": "bearer",
                 "redirect_uri": callback_uri},
    )

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Content-Type"] = "application/json"

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite='strict',
        expires=refresh_token_expires
    )

    return response


async def refresh_token(
        request: Request
    ) -> JSONResponse:

    user = await refresh_cookie_validation(request)
    new_access_token_expires = get_expiration_time(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    new_access_token = await create_access_token({'sub': user.username}, expiry_date=new_access_token_expires)

    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": new_access_token, "token_type": "bearer"},
    )

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Content-Type"] = "application/json"

    return response
    

async def logout() -> JSONResponse:
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User logged out"},
    )

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Content-Type"] = "application/json"
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response


async def registration(
        user_data: AuthUserCreate, 
        db: Session = Depends(get_db),
    ):
    existing_user = db.query(UserDB).filter(UserDB.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    try:
        hashed_password = get_password_hash(user_data.password)
        
        new_user = UserDB(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return JSONResponse(
            content={"message": "User created"}, 
            status_code=status.HTTP_201_CREATED
        )
    except IntegrityError as e:
        db.rollback()
        return JSONResponse(
            content={"error": "Username or email already exists"},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    finally:
        db.close()