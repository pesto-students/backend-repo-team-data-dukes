from sqlalchemy import Column, String, DateTime, desc
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Session
from db.engine import Base
from datetime import datetime, timezone
from .helpers import file_profiler


class Files(Base):
    __tablename__ = "files"

    id = Column(CHAR(36), primary_key=True, nullable=False, unique=True)
    from_ = Column(String(255), nullable=False)
    to_ = Column(String(255), nullable=False)
    domain = Column(String(255), nullable=False)
    type = Column(String(10), nullable=False)
    url = Column(String(2048), nullable=False)
    message_id = Column(String(72), nullable=False)
    ext = Column(String(10), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        attrs = ', '.join(f'{attr}={value!r}' for attr, value in self.__dict__.items())
        return f'{self.__class__.__name__}({attrs})'

    @classmethod
    def create(cls, db: Session, id:str, from_: str, to_: str, domain: str, type: str, url: str, message_id: str, ext: str, uploaded_at:datetime) -> 'Files':
        try:
            new_file = cls(from_=from_, to_=to_, domain=domain, type=type, url=url, message_id=message_id, ext=ext, uploaded_at=uploaded_at, id=id)
            db.add(new_file)
            db.commit()
            db.refresh(new_file)
        except Exception as e:
            msg = f"Error Creating File Data : {e}"
            return True, msg
        return False, new_file

    @classmethod
    def delete(cls, db: Session, id: str) -> bool:
        deleted = db.query(cls).filter(cls.id == id).delete()
        db.commit()
        return bool(deleted)

    @classmethod
    def get_files(cls, db: Session,from_:str = None, to_:str = None ,start_date: datetime = datetime(1970, 1, 1, tzinfo=timezone.utc), end_date: datetime = datetime.now(timezone.utc)) -> list:  
        if not ( from_ and to_ ):
            return True, "Required Attributes Not Supplied" 
        try:
            db.invalidate()
            files = db.query(cls).filter(cls.from_ == from_ and cls.to_ == to_).filter(cls.uploaded_at.between(start_date, end_date)).order_by(desc(cls.uploaded_at)).all()
        except Exception as e :
            msg = f"Error extracting files : {e}"
            return True, msg
        return False, file_profiler(files)