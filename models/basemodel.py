from app import db
from datetime import datetime


class BaseModel(object):
    """
    BaseModel
    """
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = db.Column(db.SmallInteger, default=0, nullable=False, comment="是否删除")  # ０不删除，　１删除
