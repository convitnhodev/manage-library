from sqlalchemy.orm import Session
from db.models.rules import Rule

def get_role_by_owner(owner: str, db: Session):
    rule = db.query(Rule).filter(Rule.owner == owner).first()
    return rule 

def get_role_by_id(id: str, db: Session):
    rule = db.query(Rule).filter(Rule.id == id).first()
    return rule 


def delete_role_by_owner(owner: str, db: Session):
    db.query(Rule).filter(Rule.owner == owner).delete()
    db.commit()


def create_new_role_by_owner(owner: str, db: Session):

    