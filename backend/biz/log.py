from db.repository.logs import create_log
def log_task(owner, actor, action, db):
    try:
        create_log(owner=owner, actor=actor, action=action, db=db)
    except:
        pass 

