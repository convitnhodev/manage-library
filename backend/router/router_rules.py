from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session
from schemas.rules import RuleCreate, RuleShow
from db.session import get_db
from db.models.users import User
from router.router_login import get_current_user_from_token
from biz.rule import user_create_rule
from const import detail_error
from biz.rule import user_get_rule_by_id
from biz.rule import user_delete_rule_by_id
from biz.rule import user_update_rule_by_id
from biz.rule import user_list_rule

router = APIRouter()
@router.post("")
def create_new_rule(rule: RuleCreate, db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):

    if not current_user.is_supperuser : 
        code = detail_error.CODE_DONT_HAVE_PERMISSIONS
        raise HTTPException(status_code = code, 
                            detail = detail_error.map_err[code])
    rule = user_create_rule(rule_create= rule, db = db, owner=current_user.username)
    return rule




@router.get("/{id}")
def get_rule(id: int, db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    rule = user_get_rule_by_id(owner=current_user.owner, id = id, db=db)
    if rule == None: 
        code = detail_error.CODE_RECORD_NOT_FOUND
        raise HTTPException(status_code = code, 
                            detail = detail_error.map_err[code])
    
    return rule


@router.get("")
def get_all_rule( db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    try:
        rules = user_list_rule(owner=current_user.owner, db = db)
        return rules
    except: 
        code = detail_error.CODE_CANNOT_GET
        raise HTTPException(status_code = code, 
                            detail = detail_error.map_err[code])




@router.delete("{id}")
def delete_rule(id: int, db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    rule = user_delete_rule_by_id(owner=current_user.owner, id = id, db=db)
    if rule == None: 
        code = detail_error.CODE_RECORD_NOT_FOUND
        raise HTTPException(status_code = code, 
                            detail = detail_error.map_err[code])
    
    return rule



@router.put("{id}")
def update_rule(id: int, rule: RuleCreate, db: Session= Depends(get_db), current_user: User=Depends(get_current_user_from_token)):
    if not current_user.is_supperuser : 
        code = detail_error.CODE_DONT_HAVE_PERMISSIONS
        raise HTTPException(status_code = code, 
                            detail = detail_error.map_err[code])
    
    try: 
        rule = user_update_rule_by_id(rule_update= rule, db = db, owner=current_user.username, id = id)
        if rule is not None: 
            return rule
        code = detail_error.CODE_RECORD_NOT_FOUND
        return  HTTPException(status_code=code, 
                            detail = detail_error.map_err[code])
    except: 
        code = detail_error.CODE_CANNOT_UPDATE
        raise HTTPException(status_code = code, 
                            detail = detail_error.map_err[code])
    
