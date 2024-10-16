from pydantic import BaseModel

class UserDTO(BaseModel):
    name: str

class ProductDTO(BaseModel):
    name: str

class BasketItemDTO(BaseModel):
    product_id: int
    quantity: int

class BasketResponseDTO(BaseModel):
    user_id: int
    items: list[BasketItemDTO]