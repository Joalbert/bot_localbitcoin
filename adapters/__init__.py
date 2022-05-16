import abc
from typing import List, Dict, Any

from models import Ad, Order, ChatMessage 

class Adapter(abc.ABC):
    
    @abc.abstractmethod
    def to_list_order(self, data:List[Dict[str,Any]])->List[Order]:
        pass
    
    
    @abc.abstractmethod
    def to_list_ad(self, data: List[Dict[str,Any]])->List[Ad]:
        pass

    
    @abc.abstractmethod    
    def to_list_messages(self, data: List[Dict[str,Any]])->List[ChatMessage]:
        pass