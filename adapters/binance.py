from typing import List, Any
from decimal import Decimal
from datetime import datetime

from models import Ad, Order, ChatMessage
from adapters import Adapter


class BinanceAdapter(Adapter):
    def to_list_ad(self, data: Any) -> List[Ad]:
        return super().to_list_ad(data)

    def to_list_messages(self, data: Any) -> List[ChatMessage]:
        return super().to_list_messages(data)

    def to_list_order(self, data: Any) -> List[Order]:
        return super().to_list_order(data)
