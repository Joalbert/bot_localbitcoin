from typing import Dict, Any
from functools import wraps

from lbcapi3.api import hmac

from adapters.localbitcoin import *
from connection import Connection


def post_decorator(func):
    @wraps
    def inner_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ConnectionError:
            return False
        except Exception:
            return False
        else:
            return True
    return inner_func


class ConnectionLocalBitcoin(Connection):
    _base_url= "https://localbitcoins.com"
    
    def __init__(self, credentials):
        self.hmac_key = credentials["hmac_key"]
        self.hmac_secret = credentials["hmac_secret"] 
        
    def _get_http(self, url:str)->Any:
        conn = hmac(self.hmac_key, self.hmac_secret)
        response= conn.call('GET', url)
        return response.json()       
    
    def _post_http(self, url:str, data:Dict[str, str])->bool:
        conn = hmac(self.hmac_key, self.hmac_secret)
        try:
            response= conn.call('POST', url,params=data)
            result= response.json()
        except ConnectionError:
            print(f"Failed to post to {url}")
            return False
        except Exception as e:
            print(f"Failed to post to {url}, because of {e}")
            return False
        else:
            print(result)
            return True
    
    def get_sell_ads(self, **kwargs)->Any:
        """ Get sell ads availables for some country and 
        a specific page of pagination"""
        return self._get_http(
            f"{self._base_url}/sell-bitcoins-online/"
            f"{kwargs['country_identifier']}/.json?page={kwargs['page']}"
            ) 
       
    
    def get_buy_ads(self, **kwargs)->Any:
        """ Get buy ads availables for some country 
        and a specific page of pagination"""
        return self._get_http(
            f"{self._base_url}/buy-bitcoins-online/"
            f"{kwargs['country_identifier']}/.json?page={kwargs['page']}"
            )
        
    
    def get_user_ads(self)->Any:
        """Get user ads"""
        return self._get_http(f"{self._base_url}/api/ads/") 
        
    
    def create_user_ads(self, **kwargs)->bool:
        """Create user ads"""
        return self._post_http(
            f"{self._base_url}/api/ad-create/", **kwargs)
        

    def get_closed_order(self)->Any:
        """ Get messages from closed orders"""
        return self._get_http(
            f"{self._base_url}/api/dashboard/closed/")
    
    
    def post_username_feedback(self, *, username:str, message:Dict[str, str])->bool:
        """ Post feedback from specific username"""
        return self._post_http(
            f"{self._base_url}/api/feedback/{username}/", 
            message)

    def get_contact_messages(self, contact_id:str)->Any:
        """ Get contact messages from chat for specific contact id"""
        pass

    def get_opened_order(self)->Any:
        """ Get our active ads"""
        return self._get_http(
            f"{self._base_url}/api/dashboard/")
    
    
    def get_messages_active_order(self, contact_id:str)->Any:
        """ Get messages from open orders"""
        return self._get_http(
            f"{self._base_url}/api/contact_messages/{contact_id}/")
    
    
    def post_contact_messages(self, contact_id:str, 
            message:str)->bool:
        """ Post a message for a chat"""
        return self._post_http(
            f"{self._base_url}/api/contact_message_post/{contact_id}/", 
            {'msg': message})           

    
    def update_price_ad(self,ad_id:str,value:str)->bool:
        return self._post_http(f'/api/ad-equation/{ad_id}/',{'price_equation':value})
        
