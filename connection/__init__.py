import abc
from typing import Dict, List, Any

class Connection(abc.ABC):
    
    
    @abc.abstractmethod
    def __init__(self, credentials:Dict[str, str])->None:
        pass 
        
   
    @abc.abstractmethod
    def get_sell_ads(self, **kwargs)->Any:
        """ Get sell ads availables for some country and a specific page of pagination"""
        pass
 

    @abc.abstractmethod
    def get_buy_ads(self, **kwargs)->Any:
        """ Get buy ads availables for some country and a specific page of pagination"""
        pass
 

    @abc.abstractmethod
    def get_user_ads(self)->Any:
        """Get user ads"""
        pass 
        
    @abc.abstractmethod
    def create_user_ads(self)->bool:
        """Create user ads"""
        pass 
        

    @abc.abstractmethod
    def post_username_feedback(self, *, 
            username:str, message:Dict[str, str])-> bool:
        """ Post feedback from specific username"""
        pass

    
    @abc.abstractmethod
    def get_contact_messages(self, *, 
            contact_id:str)->Any:
        """ Get contact messages from chat for specific contact id"""
        pass

    
    @abc.abstractmethod
    def post_contact_messages(self, 
                            contact_id:str, 
                            message:str)->bool:
        """ Post a message for a chat"""
        pass    

    
    @abc.abstractmethod
    def get_opened_order(self)->Any:
        """ Get our active ads"""
        pass
    
    
    @abc.abstractmethod
    def get_closed_order(self)->Any:
        """ Get messages from closed orders"""
        pass

    
    @abc.abstractmethod
    def get_messages_active_order(self, *, 
            contact_id:str)->Any:
        """ Get messages from open orders"""
        pass    
    
    
    @abc.abstractmethod
    def update_price_ad(self,ad_id, value)->bool:
        pass