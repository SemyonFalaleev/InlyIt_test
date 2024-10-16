import sqlalchemy as sq
from sqlalchemy.orm import relationship
from databases import Base


class User(Base):
    __tablename__='users'

    id = sq.Column(sq.Integer, primary_key=True, index=True)
    name = sq.Column(sq.String(length=100), nullable=False)


class Products(Base):
    __tablename__ = 'products'

    id = sq.Column(sq.Integer, primary_key=True, index=True)
    name = sq.Column(sq.String(length=250), nullable=False)


basket = sq.Table('basket', Base.metadata, 
    sq.Column('user_id', sq.Integer, sq.ForeignKey('users.id'), primary_key=True),
    sq.Column('product_id', sq.Integer, sq.ForeignKey('products.id'), primary_key=True),
    sq.Column('quantity', sq.Integer, default=1)
)

User_products = relationship("Products", secondary=basket, back_populates="users")
Products_users = relationship("User", secondary=basket, back_populates="products")

    


