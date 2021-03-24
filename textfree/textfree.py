import requests
import json
import random
from random import randint
import string
import uuid
from textfree import oauth

class Textfree:

    udid = ""
    number = ""
    pin = ""
    
    email = ""
    password = ""
    
    userID = ""
    udid = []
    installID = ""
    token = ""
    xInstallId = ""
    proxy = {}
    pin = ""
    
    sipUsername = ""
    sipPassword = ""

    debug = False

    def __init__(self, deviceID, installID, pin, userID, proxy, debug=False):

        self.userID = userID
        self.pin = pin
        self.deviceID = deviceID
        self.installID = installID
        self.proxy = proxy
        self.debug = debug

    def __init__(self, proxy={}, debug=False):
        
        #generate udid's, installID, and x-install-id and pin
        self.pin = self.__generatePin()
        self.udid.append(self.__generateUdid())
        self.installID = self.__generateInstallID(self.udid[0])
        self.xInstallId = self.__generateUUID1()
        self.udid.append(self.__generateUUID1())
        self.proxy = proxy
        self.debug = debug

    """
    Generates an account provided key information
    """
    def createAccount(self, email, password, number):

        self.reserveNumber(number)

        data = {
            "pin": self.pin,
            "installationId": self.installID,
            "udid": self.udid[0],
            "device": "unknown",
            "timezone": {
                    "januaryOffset": 480,
                    "julyOffset": 480
            },
            "email": email,
            "password": password,
            "clientId": "textfree-android-" + self.installID,
            "marketingId": self.__randomString(16),
            "version": "8.45.1",
            "versionOS": "5.1.1",
            "systemProperties": {
                    "device": "unknown",
                    "version.sdk-int": "22",
                    "user.home": "",
                    "https.proxyPort": "",
                    "http.proxyHost": "",
                    "user": "unknown",
                    "bootloader": "uboot",
                    "http.proxyPort": "",
                    "device-id": self.udid[0],
                    "id": self.__randomString(6),
                    "manufacturer": "unknown",
                    "http.nonProxyHosts": "",
                    "tags": "release-keys",
                    "type": "user",
                    "unknown": "unknown",
                    "host": "se.infra",
                    "https.proxyHost": "",
                    "version.sdk": "22",
                    "version.incremental": "eng.se.infra.20190531.182646",
                    "fingerprint": "\/\/:5.1.1\/20171130.376229:user\/release-keys",
                    "java.io.tmpdir": "\/data\/data\/com.pinger.textfree\/cache",
                    "mac": self.__randomMacAddress(),
                    "cpu-abi": "armeabi-v7a",
                    "radio": "unknown",
                    "board": "unknown",
                    "version.codename": "REL",
                    "https.nonProxyHosts": "",
                    "display": "-user 5.1.1 20171130.276299 release-keys",
                    "http.agent": "Dalvik\/2.1.0 (Linux; U; Android 5.1.1; unknown Build\/LMY48Z)",
                    "version.release": "5.1.1",
                    "brand": "unknown",
                    "hardware": "intel",
                    "cpu-abi2": "armeabi",
                    "product": "unknown",
                    "model": "unknown",
                    "http.keepAlive": "false"
            },
            "accountType": "email",
            "notificationTokenInfo": {
                    "notificationToken": "eIdgz_ODx3o:APA91bF1zXAOerNALpVBxc16gg9snAHrlNoJfxtqIPd3MNSCepj8BPbN0PPVoEo84ZO_yO-chQEu-xR62x7Z0cDtwIHbq4e0U0a2GZyXhJpHEqLASBJ2hyeUVHPDNWpsznM87THEfI7g",
                    "notificationType": "G",
                    "notificationStatus": 1
            }
        }
        
        header = self.__getHeaderTemplate()
        oAuthHeader = oauth.OAuth("POST", "https://api.pinger.com/1.0/account/registerWithLang", "textfree-android")
        header["Authorization"] = oAuthHeader.createHeader(1)
        header["x-rest-method"] = "POST"

        res = requests.post("https://api.pinger.com/1.0/account/registerWithLang?lang=en_US&cc=US",

                            proxies=self.proxy,
                            headers=header,
                            data=json.dumps(data),
                            verify=not self.debug

                            )

        try:
            info = json.loads(res.content)
            self.userID = info["result"]["userId"]
            self.token = info["result"]["token"]
        except:
            
            print("[ ERROR ] Account not created! Has this email been used before?")

        self.setupNumber(number)
        
        return res.content
        
    
    """
    Gets available numbers provided areaCode
    """
    def getAvaliableNumbers(self, areaCode):

        data = json.loads('{\"areaCode\":\"'+areaCode+"\"}")
        header = self.__getHeaderTemplate()
        oAuthHeader = oauth.OAuth("GET", "https://api.pinger.com/1.0/account/phone/listAvailableDnxNumbers", "textfree-android")
        header["Authorization"] = oAuthHeader.createHeader()
        header["x-rest-method"] = "GET"

        res = requests.post("https://api.pinger.com/1.0/account/phone/listAvailableDnxNumbers",
                                 
                            proxies=self.proxy,
                            headers=header,
                            data=json.dumps(data),
                            verify=not self.debug

                            )
        return res.content

    """
    Reserves a number
    """
    def reserveNumber(self, number):
        
        data = json.loads('{"phoneNumber":"'+number+'", "udid": "'+self.udid[0]+'"}')
        header = self.__getHeaderTemplate()
        oAuthHeader = oauth.OAuth("POST", "https://api.pinger.com/1.0/account/phone/reserve", "textfree-android")
        header["Authorization"] = oAuthHeader.createHeader()
        header["x-rest-method"] = "POST"
        res = requests.post("https://api.pinger.com/1.0/account/phone/reserve",
                            
                            proxies=self.proxy,
                            headers=header,
                            data=json.dumps(data),
                            verify=not self.debug
                            
                            )
        return res.content

    def setupNumber(self, number):

        data = json.loads('{"phoneNumber":"'+number+'","purchased": "0","hideAds": "0","hasVoice": "1"}')
        oa = oauth.OAuth("POST", "https://api.pinger.com/1.0/account/phone", "{}%3Btextfree-android-{}".format(self.userID, self.installID))
        header = self.__getHeaderTemplate()
        header["Authorization"] = oa.createHeader(0, self.token)
        header["x-rest-method"] = "POST"
        res = requests.post("https://api.pinger.com/1.0/account/phone",
                            
                            proxies=self.proxy,
                            headers=header,
                            data=json.dumps(data),
                            verify=not self.debug

                            )
        
        oa = oauth.OAuth("GET", "https://api.pinger.com/1.0/account/phone/register", "{}%3Btextfree-android-{}".format(self.userID, self.installID))
        header = self.__getHeaderTemplate()
        header["Authorization"] = oa.createHeader(0, self.token)
        header["x-rest-method"] = "GET"
        res = requests.post("https://api.pinger.com/1.0/account/phone/register",

                                proxies=self.proxy,
                                headers=header,
                                verify=not self.debug

                                )


        self.getSipInfo()

        return res.content

        
    def sendMessage(self, msg, to):

        data = json.loads('{"to": [{"TN": "'+to+'"}],"text": "'+msg+'"}')

        oa = oauth.OAuth("POST", "https://api.pinger.com/2.0/message", "{}%3Btextfree-android-{}".format(self.userID, self.installID))
        header = self.__getHeaderTemplate()
        header["Authorization"] = oa.createHeader(0, self.token)
        header["x-rest-method"] = "POST"
        res = requests.post("https://api.pinger.com/2.0/message",
                            
                            proxies=self.proxy,
                            headers=header,
                            data=json.dumps(data),
                            verify=not self.debug
                            
                            )

        return res.content


    def authUser(self):

        
        data = {
            "userId": self.userID,
            "pin": self.pin,
            "udid": self.udid[0],
            "clientId": "textfree-android-"+self.installID,
            "installationId": self.installID,
            "versionOS": "5.1.1",
            "device": "unknown",
            "version": "8.45.1"
        }

        oa = oauth.OAuth("POST", "https://api.pinger.com/1.0/userAuth", "{}%3Btextfree-android-{}".format(self.userID, self.installID))
        header = self.__getHeaderTemplate()
        header["Authorization"] = oa.createHeader(0, self.token)
        header["x-rest-method"] = "POST"
        res = requests.post("https://api.pinger.com/1.0/userAuth",
                            
                            proxies=self.proxy,
                            headers=header,
                            data=json.dumps(data),
                            verify=not self.debug
                            
                            )

        return res.content



    def login(self, email, password):

        data = {
            "email": email,
            "accountType": "email",
            "password": password,
            "udid": self.udid[0],
            "clientId": "textfree-android-"+self.installID,
            "installationId": self.installID,
            "version": "8.45.1",
            "versionOS": "5.1.1",
            "device": "unknown"
        }

        oa = oauth.OAuth("POST", "https://api.pinger.com/1.0/account/username/switchDeviceAndUserAuth", "textfree-android")
        header = self.__getHeaderTemplate()
        header["Authorization"] = oa.createHeader(0)
        header["x-rest-method"] = "POST"
        res = requests.post("https://api.pinger.com/1.0/account/username/switchDeviceAndUserAuth",
                            
                            proxies=self.proxy,
                            headers=header,
                            data=json.dumps(data),
                            verify=not self.debug
                            
                            )

        try:
            data = json.loads(res.content)
            self.userID = data["result"]["accountId"]
            self.token = data["result"]["token"]
        except:
            print("[ ERROR ] Error setting number up, is this number already assigned to an account? Have you already create an account with this email?")
            
        self.getSipInfo()    
        
        return res.content
        
    def getMessages(self):
        
        oa = oauth.OAuth("GET", "https://api.pinger.com/2.0/bsms", "{}%3Btextfree-android-{}".format(self.userID, self.installID))
        header = self.__getHeaderTemplate()
        header["Authorization"] = oa.createHeader(0, self.token)
        header["x-rest-method"] = "GET"
        res = requests.post("https://api.pinger.com/2.0/bsms",
                            
                            proxies=self.proxy,
                            headers=header,
                            verify=not self.debug
                            
                            )

        
        return res.content
        
    def getSipInfo(self):
        
        
        oa = oauth.OAuth("GET", "https://api.pinger.com/1.0/account/phone/SIP", "{}%3Btextfree-android-{}".format(self.userID, self.installID))
        header = self.__getHeaderTemplate()
        header["Authorization"] = oa.createHeader(0, self.token)
        header["x-rest-method"] = "GET"
        res = requests.post("https://api.pinger.com/1.0/account/phone/SIP",

                                proxies=self.proxy,
                                headers=header,
                                verify=not self.debug

                                )

            

        
                            
        try:
            
            data = json.loads(res.content)
            self.sipUsername = data["result"]["username"]
            self.sipPassword = data["result"]["password"]
            
        except:
            print("[ ERROR ] could not get sip username/password, are you using a proxy outside of the US/CANADA? If so voice is not possible.")


    """
    Gets Sip username
    """
    def getSipUsername(self):
        
        return self.sipUsername
        
        
    """
    Gets sip password
    """
    def getSipPassword(self):
        
        return self.sipPassword
    
    """
    Generates a udid
    """
    def __generateUdid(self):

        return self.__generateUUID1()
    

    """
    Generates installId given udid
    """
    def __generateInstallID(self, udid):

        return "{}-{}".format(udid, self.__randomString(13))

    """
    Generate a random UUIDV1
    """
    def __generateUUID1(self):
        
        return str(uuid.uuid1())

    """
    Generate pin
    """
    def __generatePin(self):

        pass

    def __getHeaderTemplate(self):

        header = {

                "x-rest-method": "",
                "Content-Type" : "application/json",
                "X-Install-Id": self.xInstallId,
                "x-client": "textfree-android,8.45.1,214_RC_v.45.1_STORE_CONFIG",
                "x-os" : "android,5.1.1",
                "x-gid" : "90",
                "x-bg": "0",
                "x-udid": "{},{}".format(self.udid[0], self.udid[1]),
                "Authorization": "",
                "User-Agent": "okhttp/3.11.0"

            }

        return header
    
    """
    Generate a random string of fixed length
    """
    def __randomString(self, stringLength=10):
        
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    def __generatePin(self, n=10):
        
        return ''.join(["%s" % randint(0, 9) for num in range(0, n)])

    """
    Returns a completely random Mac Address
    """
    def __randomMacAddress(self):
        
        mac = [0x00, 0x16, 0x3e, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
        return ':'.join(map(lambda x: "%02x" % x, mac))
        
        
