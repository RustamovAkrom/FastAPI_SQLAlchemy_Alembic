from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.repositories import ItemRepo
from app import schemas


router = APIRouter(prefix="/items")


@router.post('/items', tags=['item'], response_model=schemas.Item, status_code=201)
async def create_item(item_request: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Create an item and store it in the database
    """

    db_item = ItemRepo.fetch_by_name(db, name=item_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists!")
    
    return await ItemRepo.create(db=db, item=item_request)


@router.get('/items', tags=['item'], response_model=List[schemas.Item])
def get_all_items(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Items stored in database
    """

    if name:
        items = []
        db_item = ItemRepo.fetch_by_name(db, name)
        
        if not db_item:
            raise HTTPException(status_code=404, detail="Items not found with the given NAME")
        items.append(db_item)

        return items
    
    else:
        return ItemRepo.fetch_all(db)
    

@router.get('items/{item_id}', tags=['item'], response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get the Item with give ID provided by User Stored in database
    """
    
    db_item = ItemRepo.fetch_by_id(db, item_id)
    print(db_item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    return db_item


@router.delete('/items/{item_id}', tags=['item'])
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    await ItemRepo.delete(db, item_id)

    return "Item deleted successfully!"


@router.put('/items/{item_id}', tags=['items'], response_model=schemas.Item)
async def update_item(item_id: int, item_request: schemas.Item, db: Session = Depends(get_db)):
    """
    Update an Item stored in the database
    """

    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item:
        update_item_encoded = jsonable_encoder(item_request)
        db_item.name = update_item_encoded['name']
        db_item.price = update_item_encoded['price']
        db_item.description = update_item_encoded['description']
        db_item.store_id = update_item_encoded['store_id']
        return await ItemRepo.update(db=db, item_data=db_item)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")
