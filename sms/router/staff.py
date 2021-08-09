from fastapi import APIRouter, Request,  Depends, Header, Security
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.api_key import APIKeyHeader
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, database, model, oauth2
from  .. import hashing, token
from datetime import datetime, timedelta
from ..auth import AuthHandler


auth_handler = AuthHandler()
X_API_KEY = "$@4@y@f^!"
API_KEY_NAME = "x-api-key"
api_key_header_auth = APIKeyHeader(name = API_KEY_NAME, auto_error=True)


router = APIRouter(prefix='/staff', tags=['staff'])

@router.get('/{id}')
def get_staff_by_id(id: int,  db: Session = Depends(database.get_db), x_api_key: str = Security(api_key_header_auth)):
    if x_api_key != X_API_KEY:
        return {"success": False, "message": "Invalid Header Key"}
    else:
        staff = db.query(model.sahayatri).filter(model.sahayatri.id == id).first()
        return staff

@router.post('')
def create_staff(request: schemas.Staff, db: Session = Depends(database.get_db)):
    newStaff = model.sahayatri(firstname=request.firstname,
            lastname=request.lastname, email=request.email, password = hashing.get_password_hash(request.password))
    db.add(newStaff)
    db.commit()
    db.refresh(newStaff)
    checkValue = db.query(model.sahayatri).filter(model.sahayatri.firstname == request.firstname).first()
    if checkValue:
        return {"success": True, "message": "Succesfully Added"}
    else:
        return {"success": False , "message": "Failed to add"}

@router.post('/login') #response_model=schemas.user_login)
def login(request: schemas.user_login,  db: Session = Depends(database.get_db)):
    user = db.query(model.sahayatri).filter(model.sahayatri.firstname == request.firstname).first()
    if not user:
        return {"login": False, "message": "Invalid Credentials"}
    if not hashing.verify_password(request.password, user.password):
        return {"login": False, "message": "Invalid Credentials"}

    token = auth_handler.encode_token(request.password)
    return {"token": token, "token_type": "bearer"}
    #return {"login": True, "message": "Login Succesful"}



@router.get('')
def get_staff_by_id(id: int,  db: Session = Depends(database.get_db)):
    staff = db.query(model.sahayatri).filter(model.sahayatri.id == id).first()
    if not staff:
        return {"success": False , "message": "Failed"}
    else:
        return {"success": True, "message": "Succes", "data": staff}

@router.get('', response_model=List[schemas.User])
def get_staff(db: Session = Depends(database.get_db)):
    staff = db.query(model.sahayatri).all()
    #staff = db.query(model.sahayatri.firstname).first()
    return staff
    #if not staff:
        #return {"success": False , "message": "Failed"}
    #else:
        #return {"success": True, "message": "Succes", "data": staff}


@router.get('/{firstname}', response_model=List[schemas.User])
def get_staff_by_name(firstname: str, db: Session = Depends(database.get_db)):
    staff = db.query(model.sahayatri).filter(model.sahayatri.firstname == firstname).all()
    return staff


@router.delete('')
def deleteUsser(id: int, db: Session = Depends(database.get_db), username=Depends(auth_handler.auth_wrapper)):
    staff = db.query(model.sahayatri).filter(model.sahayatri.id == id)
    checkdelete = staff.delete(synchronize_session=False)
    db.commit()
    if checkdelete:
        return {"success": True, "message": "Succesfully Deleted"}
    else:
        return {"success": False , "message": "Failed to delete"}



@router.put('user')
def updateUser(request: schemas.updateUser, db:Session = Depends(database.get_db)):
    staff = db.query(model.sahayatri).filter(model.sahayatri.id == request.id)
    checkUpdate = staff.update({'lastname': request.lastname})
    db.commit()
    if checkUpdate:
        return {"success": True, "message": "Succesfully updated"}
    else:
        return {"success": False , "message": "Failed to update"}
        
@router.get('/{firstname}/{lastname}')
def multiplequery(firstname: str= None, lastname: str = None, db: Session = Depends(database.get_db)):
    staff = db.query(model.sahayatri).filter(model.sahayatri.firstname ==firstname).filter(model.sahayatri.lastname == lastname).first()
    return staff

'''
@router.post('/')
def arrayFormat(request: List[schemas.User]):
    return request
'''

@router.post('/')
def create_array_staff(request: List[schemas.Staff], db: Session = Depends(database.get_db)):
    for data in request:
        newStaff = model.sahayatri(firstname=data.firstname,
                lastname=data.lastname, email=data.email, password =
                hashing.get_password_hash(data.password))
        db.add(newStaff)
        db.commit()
        db.refresh(newStaff)
        checkValue = db.query(model.sahayatri).filter(model.sahayatri.firstname == request.firstname).first()
    if checkValue:
        return {"success": True, "message": "Succesfully Added"}
    else:
        return {"success": False , "message": "Failed to add"}
