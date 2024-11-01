from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=True)
    items = relationship("Item", primaryjoin="Store.id == Item.store_id", cascade="all, delete-orphan")

    def __repr__(self,):
        return 'Store(name=%s)' % self.name