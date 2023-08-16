from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, or_
from sqlalchemy.orm import Session, relationship, backref, joinedload
from db.engine import Base

from .helpers import profiler

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    domain = Column(String(255), nullable=False, unique=True)
    jid = Column(String(255), nullable=False, unique=True)
    email_id = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now()) 
    active = Column(Boolean, default=True)
    mobile_no = Column(String(20), unique=True, nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    avatar_url = Column(String(2048), nullable=True)

    class Config:
        orm_mode = True

    def __repr__(self):
        attrs = ', '.join(f'{attr}={value!r}' for attr, value in self.__dict__.items())
        return f'{self.__class__.__name__}({attrs})'

    @classmethod
    def create(cls, db: Session, username: str, domain: str ,jid:str, password: str, email_id: str = None,
               active: bool = True, mobile_no: str = None ) -> 'Users':
        try:
            user = cls(username=username, domain=domain, password=password, email_id=email_id, active=active,
                    mobile_no=mobile_no, jid=jid)
            db.add(user)
            db.commit()
            db.refresh(user)
        except Exception as e:
            msg = f'Error Creating User : {e}'
            return True, msg
        return False, user
    
    @classmethod
    def update(cls, db: Session, id: int, **kwargs) -> bool:
        try:
            user = db.query(cls).filter(cls.id == id).first()
            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)
                db.commit()
                return False, True
            return False, False
        except Exception as e:
            msg = f'Error Updating User : {e}'
            return True, msg
        
    @classmethod
    def update_profile(cls, db: Session, id: int, data: object) -> bool:
        try:
            user = db.query(cls).filter(cls.id == id).first()
            if user:
                for key, value in data.items():
                    setattr(user, key, value)
                db.commit()
                return False, True
            return False, False
        except Exception as e:
            msg = f'Error Updating User : {e}'
            return True, msg


    @classmethod
    def delete(cls, db: Session, id: int):
        user = db.query(cls).filter(cls.id == id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
    
    @classmethod
    def exist(cls, db: Session, email_id: str = None, mobile_no: str = None):
        try:
            db.invalidate()
            query = db.query(cls)
            if email_id:
                query = query.filter(cls.email_id == email_id)
            if mobile_no:
                query = query.filter(cls.mobile_no == mobile_no)
            user = query.first()
            
        except Exception as e:
            msg = f'Error in Exist : {e} '
            return (True, None, msg)
        return (False, True, user) if user else (False, False, None)

    
    @classmethod
    def get_all_users(cls, db:Session, domain:str, jid: str):
        try:
            db.invalidate()
            query = db.query(cls).filter(cls.domain == domain).filter(cls.jid != jid)
        except Exception as e:
            msg = f'Error Fetching All Users : {e}'
            return True, msg
        return False, profiler(query.all())
    
   
    




