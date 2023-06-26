from pydantic import BaseModel, EmailStr
from datetime import datetime
import json
from sqlalchemy import inspect


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseModel):
            return o.dict()
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

def object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }