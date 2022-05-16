from typing import List, Dict, Any
from decimal import Decimal
from datetime import datetime

from models import Ad, Order, ChatMessage
from adapters import Adapter

class AdapterLocalbitcoin(Adapter):

    def to_list_ad(self, data: List[Dict[str, Any]]) -> List[Ad]:
        response = []
        for item in data:
            response.append(
                Ad(int(item["data"]["ad_id"]),
                Decimal(item["data"]["temp_price"]),
                Decimal(item["data"]["min_amount_available"]),
                Decimal(item["data"]["max_amount_available"]),
                str(item["data"]["bank_name"]),
                str(item["data"]["profile"]["username"]),
                bool(item["data"]["visible"]),))
        return response
        
    def to_list_order(self, data: List[Dict[str, Any]]) -> List[Order]:
        response = []
        for item in data:
            response.append(
                Order(
                    int(datetime.fromisoformat(item["data"]["created_at"]).timestamp()),
                    item["data"]["seller"]["username"],
                    item["data"]["buyer"]["username"],
                    "",
                    "",
                    int(item["data"]["contact_id"]),
                    not (item["data"]["closed_at"] is None or item["data"]["closed_at"]=="")
                )
            )
        return response

    def to_list_messages(self, data: List[Dict[str, Any]]) -> List[ChatMessage]:
        response = []
        for item in data:
            response.append(
               ChatMessage(
                   int(datetime.fromisoformat(item["created_at"]).timestamp()),
                   item["sender"]["username"],
                   item["msg"]        
                )
            )
        return response
