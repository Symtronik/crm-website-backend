from ...config.database import DBBase, engine
from sqlalchemy import Column, Integer, String, Boolean, Float,Date, Time, DateTime
from datetime import date
from typing import Optional

class Documents(DBBase):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String(70), index=True)
    created_at = Column(Date, default=date.today)
