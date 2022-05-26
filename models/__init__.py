from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Ad:
    id: int
    price: Decimal
    minimum_value: Decimal
    maximum_value: Decimal
    bank: str
    publisher: str
    visible: bool = True


@dataclass
class UserData:
    username: str
    name: str = ""


@dataclass
class Chat:
    id: int
    name: str = ""


@dataclass
class ChatMessage:
    id: int
    username: str
    message: str


@dataclass
class Feedback:
    message: str
    feedback: str


@dataclass
class Order:
    id: int
    seller: str
    buyer: str
    feedback: str
    feedback_message: str
    chat_id: int
    is_closed: bool
