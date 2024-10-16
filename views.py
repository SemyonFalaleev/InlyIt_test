from models import User, Products, basket
from sqlalchemy.orm import Session
import dto

def create_user(data:dto.UserDTO, db: Session) -> User:
    new_user = User(name=data.name)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as ex:
        print(ex)
        db.rollback()
        return None
    return new_user

def create_product(data:dto.ProductDTO, db: Session) -> Products:
    new_product = Products(name=data.name)
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
    except Exception as ex:
        print(ex)
        db.rollback()
        return None
    return new_product

def add_to_basket(user_id: int, item:dto.BasketItemDTO, db: Session) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    product = db.query(Products).filter(Products.id == 
    item.product_id).first()
    if user and product:
        existing_item = db.query(basket).filter(
            basket.c.user_id == user_id,
            basket.c.product_id == item.product_id
        ).first()

        if existing_item:
            new_quantity = existing_item.quantity + item.quantity
            db.execute(basket.update().where(
            basket.c.user_id == user_id,
            basket.c.product_id == item.product_id
            ).values(quantity=new_quantity))
        else:
            new_entry = {
                'user_id': user_id,
                'product_id': item.product_id,
                'quantity': item.quantity
            }
            db.execute(basket.insert().values(new_entry))

        db.commit()
        return True
    return False

def update_quantity(user_id: int, item: dto.BasketItemDTO, db: Session) -> bool:
    existing_item = db.query(basket).filter(
        basket.c.user_id == user_id,
        basket.c.product_id == item.product_id
        ).first()
    if existing_item:
        db.execute(basket.update().where(
            basket.c.user_id == user_id,
            basket.c.product_id == item.product_id).values(
            quantity=item.quantity))
        db.commit()  
        return True

    return False

def remove_from_basket(user_id: int, product_id: int, db: Session) -> bool:
    result = db.execute(basket.delete().where(
        basket.c.user_id == user_id,
        basket.c.product_id == product_id
    ))
    db.commit()
    return result.rowcount > 0  

def get_basket(user_id: int, db: Session) -> dto.BasketResponseDTO :
    items = db.query(basket).filter(basket.c.user_id == user_id).all()
    basket_items = [dto.BasketItemDTO(product_id=item.product_id, quantity=item.quantity) for item in items]
    
    return dto.BasketResponseDTO(user_id=user_id, items=basket_items)


