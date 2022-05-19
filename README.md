# Bot Localbitcoin
Bot Localbitcoin consume data from API Localbitcoin to update price of your ads, give feedback and write message programmatically.

# Model
The bot handle several custom data such as ChatMessage, UserData, Chat, Feedback, Order that are used as an absctraction to handle data from localbitcoin.

# Connection
Object used to connect bot with broker, the first implementation is ConnectionLocalBitcoin that use localbitcoin API. However, it could be implemented with other brokers.

# Adapter
Takes data from the broker and converts to list of Ads, Order or ChatMessage. This is an ABC to handle data from server.

# User
It is an ABC to request data through a connection object and use adapter object to convert data to models handles by our api. The first implementation is for localbitcoin.

# Bot
This is an object class that has an user instance of any implementation and perform several activities such as read/write messages, orders, own ads, buy ads, sell ads and write feedback. Addittionally, it is capable of filter list of Ads, remove ads, that idea behind is to provide the least methods needed to create a bot for update price in competition with other ads, also write greeting message, or interact programmatically with other users and write feedback.

# Examples
Some script to show how to use the code.



