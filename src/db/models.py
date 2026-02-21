from dataclasses import dataclass


@dataclass(slots=True)
class Category:
    id: int
    name: str


@dataclass(slots=True)
class Product:
    id: int
    category_id: int
    name: str
    description: str
    price: float
    in_stock: bool


@dataclass(slots=True)
class CartItem:
    user_id: int
    product_id: int
    quantity: int


@dataclass(slots=True)
class Order:
    id: int
    user_id: int
    customer_name: str
    phone: str
    address: str
    comment: str
    total_amount: float
    status: str
    created_at: str
