from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases import get_db

import dto
from views import create_user, create_product, add_to_basket, update_quantity, remove_from_basket, get_basket
router = APIRouter()

@router.post('/user', tags=['user'])
async def create(data: dto.UserDTO = None, db: Session = Depends(get_db)):
    return create_user(data, db)

@router.post('/product', tags=['product'])
async def create(data: dto.ProductDTO = None, db: Session = Depends(get_db)):
    return create_product(data, db)

@router.post('/basket/create', tags=['basket'])
async def add_to_cart_route(item: dto.BasketItemDTO, user_id: int, db: Session = Depends(get_db)):
    success = add_to_basket(db=db, user_id=user_id, item=item)
    if not success:
        raise HTTPException(status_code=404, detail="User or Product not found")
    return {"message": "Product added to basket"}

@router.put("/basket/update", tags=['basket'])
async def update_quantity_route(item: dto.BasketItemDTO, user_id: int, db: Session = Depends(get_db)):
    success = update_quantity(db=db, user_id=user_id, item=item)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found in basket")
    return {"message": "Quantity updated"}

@router.delete("/basket/delete", tags=['basket'])
async def remove_from_basket_route(user_id: int, product_id: int, db: Session = Depends(get_db)):
    success = remove_from_basket(db=db, user_id=user_id, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found in basket")
    return {"message": "Product removed from basket"}

@router.get("/basket/get", tags=['basket'], response_model=dto.BasketResponseDTO)
async def get_basket_route(user_id: int, db: Session = Depends(get_db)):
    basket = get_basket(user_id=user_id, db=db)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")
    return basket