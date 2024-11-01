from sqlalchemy.orm import Session

from app import schemas, models


class StoreRepo:

    async def create(db: Session, store: schemas.StoreCreate):
        db_store = models.Store(name=store.name)
        db.add(db_store)
        db.commit()
        db.refresh(db_store)
        return db_store
    
    def fetch_by_id(db: Session, _id: int):
        return db.query(models.Store).filter(models.Store.id == _id).first()
    
    def fetch_by_name(db: Session, name: str):
        return db.query(models.Store).filter(models.Store.name == name).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Store).offset(skip).limit(limit).all()
    
    async def delete(db: Session, _id: int):
        db_store = db.query(models.Store).filter_by(id=_id).first()
        db.delete(db_store)
        db.commit()

    async def update(db: Session, store_data):
        updated_store = db.merge(store_data)
        db.commit()
        return updated_store
