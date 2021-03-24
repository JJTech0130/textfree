import datetime
import random
import string
import hashlib
import hmac
import base64
import urllib.parse

class OAuth:

    method = ""
    location = ""
    token = ""                                       
    consumerSecret = ["A4S0xXdDWyE8OZCQ1mxfQrN44SEyFgPgjVRx1fWWjqUDCKO0h26Af1sCt43pjAii&", #Consumer Secret used inside of app for batch and reserve, etc
                      "v6wbtkWK9rLJRdZkmqXF1Zq5aqISgrdtxySG6B3BvOcNuK8r2SlTUOiE9vkfROaR&", #Consumer Secret used inside of app to create accounts 
                      "CdCIDGKs3TAf1UZGrkoYkeJKIvbscPJQ2RIFT0k5RHkRneP4zmOGXsAXDSVifC2a&"] #Consumer Secret used for webclient
    
    oauth_timestamp = ""
    oauth_signature_method = "HMAC-SHA1"
    oauth_consumer_key = ""
    oauth_nonce = ""
    oauth_signature = ""
    realm = "https://api.pinger.com"


    def __init__(self, method, location, oauth_consumer_key, oauth_timestamp, oauth_nonce, token=""):
        
        self.method = method
        self.location = location
        self.oauth_consumer_key = oauth_consumer_key
        self.oauth_timestamp = oauth_timestamp
        self.oauth_nonce = oauth_nonce
        self.token = token

   
   
    def __init__(self, method, location, oauth_consumer_key, token=""):

        self.method = method
        self.location = location
        self.oauth_consumer_key = oauth_consumer_key
        self.oauth_timestamp = str(int(datetime.datetime.now().timestamp()))
        self.oauth_nonce = self.__randomString(16)
        self.token = token
    
        
    

    """
    Generate a hmac-sha1 hash provided base_string
    with the option of adding an additional token to the key
    """
    """
    def createSignature(self, secretKey=0):

        key = bytes(self.consumerSecret[secretKey], 'utf8')
        message = bytes(self.createBaseString(), 'utf8')
        return urllib.parse.quote(base64.urlsafe_b64encode(hmac.new(key, message, hashlib.sha1).digest()).decode("utf8")).replace("-", "%2B").replace("_", "%2F")
    """

    
    def createSignature(self, token, base_string, secretKey=0):

        key = bytes(self.consumerSecret[secretKey]+token, 'utf8')
        message = bytes(base_string, 'utf8')
        return urllib.parse.quote(base64.urlsafe_b64encode(hmac.new(key, message, hashlib.sha1).digest()).decode("utf8")).replace("-", "%2B").replace("_", "%2F")


    """
    Generates oauth basestring
    Refer: http://oauthbible.com/
    """
    def createBaseString(self, method, location, consumer_key, timestamp, nonce):
        
        return "{}&{}&oauth_consumer_key={}&oauth_signature_method={}&oauth_timestamp={}&oauth_nonce={}".format(
            
            method.upper(),
            location,
            consumer_key,
            "HMAC-SHA1",
            timestamp,
            nonce
            
        )

    def createBaseString(self):

        return "{}&{}&oauth_consumer_key={}&oauth_signature_method={}&oauth_timestamp={}&oauth_nonce={}".format(
            
            self.method.upper(),
            self.location,
            self.oauth_consumer_key,
            self.oauth_signature_method,
            self.oauth_timestamp,
            self.oauth_nonce

        )

    def createHeader(self, secretKey=0, token=""):

        return "OAuth realm=\"https://api.pinger.com\", oauth_consumer_key=\"{}\", oauth_signature_method=\"{}\", oauth_timestamp=\"{}\", oauth_nonce=\"{}\", oauth_signature=\"{}\"".format(

            self.oauth_consumer_key,
            self.oauth_signature_method,
            self.oauth_timestamp,
            self.oauth_nonce,
            self.createSignature(token, self.createBaseString(), secretKey)

        )

    """
    Generate a random string of fixed length
    """
    def __randomString(self, stringLength=10):
        
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))
    
