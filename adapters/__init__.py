import abc
from typing import List, Any

from models import Ad, Order, ChatMessage


class Adapter(abc.ABC):

    @abc.abstractmethod
    def to_list_order(self, data: Any) -> List[Order]:
        pass

    @abc.abstractmethod
    def to_list_ad(self, data: Any) -> List[Ad]:
        pass

    @abc.abstractmethod
    def to_list_messages(self, data: Any) -> List[ChatMessage]:
        pass
