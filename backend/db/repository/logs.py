from sqlalchemy.orm import Session
from db.models.logs import Log
import json
from datetime import datetime
from sqlalchemy import and_

def create_log(owner: str, action: str, actor: str,  db: Session):
    new_log = Log(
        owner = owner, 
        action = action, 
        actor = actor, 
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log




def list_log(owner: str, action: str, db: Session, start_time: datetime = None, end_time: datetime = None):
    query = db.query(Log).filter(
        Log.owner == owner,
    )

    if action is not None:
        query = query.filter(Log.action == action)
    
    if start_time is not None:
        query = query.filter(Log.timestamp >= start_time)
    if end_time is not None:
        query = query.filter(Log.timestamp <= end_time)

    logs = query.all()
    return logs