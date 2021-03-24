# Textfree-API (Jul 20, 2019)
Create accounts, assign phone numbers, receiving/sending messages, and make calls, all with a few lines of python.
Disclaimer: All of the above code is not in anyway created by pinger or associates of textfree. I am the creator of the library.

## Getting Started

### Download the project and install dependencies.
```
git clone https://githacks.org/xerox/textfree.git
cd textfree
pip install -r requirements.txt
```

### Using textfree in a project

1. Make sure you have a copy of the ***textfree*** folder in your project.
2. Import the textfree file and class like so:
```python
from textfree import textfree
```

### Creating an account

Creating an account is very easy and requires 2-3 lines of code. Some things to know:

1. They have no email verification so you can just make anything up.
2. You can only register for a number that they actaully own, you cannot spoof phone numbers.

```python
from textfree import textfree
tf = textfree.Textfree()
tf.getAvaliableNumbers("808") # gets available 808 numbers
tf.createAccount("SomeEmailItDoesntMatter@duwjaiodj.cc", "anyPasswordWillDo", "8082222222")
```

### Sending a text

Sending a text is super easy. Group chats are a possibility later down the road.
```python
from textfree import textfree
tf = textfree.Textfree()
tf.getAvaliableNumbers("808") # gets available 408 numbers
tf.createAccount("SomeEmailItDoesntMatter@duwjaiodj.cc", "anyPasswordWillDo", "18082222222")
tf.sendMessage("hello world", "18081234567")
```

### Getting messages

Textfree uses a query string to indicate from when on to get messages I.E: since=2019-07-22+20%3A08%3A35.700356

The since date will be at the end of the last message (inside of the json)

```json
{
	"success": "Communications retrieved",
	"result": {
		"messages": [{
			"id": "1029177846887524815",
			"name": "Textfree",
			"pictureURL": "https:\/\/pinger-prod-bsm.s3.amazonaws.com\/bsm\/297\/bsmmedia-08612f36d5ddf5c236619d28180bd82f.jpg",
			"messages": [{
				"id": "6704800802585917765",
				"message": "You're ready to text, call, set up your voicemail, and chat freely. You can subscribe anytime to <a href=\"textfree-android:\/\/www.pinger.com?action=noads\">remove ads<\/a> or <a href=\"textfree-android:\/\/www.pinger.com?action=reservenumber\">reserve your number<\/a> (normally we reclaim inactive numbers after 30 days). Enjoy!",
				"displayDuration": "0",
				"inboxPreviewText": "Hello and welcome",
				"mediaURL": "https:\/\/pinger-prod-bsm.s3.amazonaws.com\/bsm\/679\/bsmmedia-bba5cce2cce64cde65289ddf02025292.png",
				"mediaClickURL": "textfree-android:\/\/www.pinger.com?action=reservenumber"
			}],
			"time": "2019-07-22 20:53:03"
		}],
		"nextSince": "2019-07-22 20:53:03.076525" # This is where it is
	}
}
```
Here is how to get messages inside of python. You can specify a since time.
```python
from textfree import textfree
tf = textfree.Textfree()
tf.login("somehwaD@dwD.xcodd", "dWADAWdaWWDaD") # or register
messages = tf.getMessages(since="2019-07-22 20:53:03.076525")
```

### Using a proxy

Textfree only supports voice for US/CANADA (Excluding Hawaii)

```python
from textfree import textfree
tf = textfree.Textfree(proxy={"http":"socks5://localhost:9050", "https":"socks5://localhost:9050"})
```

### MITM Setup

If you want to see why something isnt working/run the code through charles/burp

```python
from textfree import textfree
tf = textfree.Textfree(debug=True) # doesnt validate ssl certs...
```
### SIP?

Working on it. For the moment you can use the following to get your SIP username/password. The SIP/STUN/TUN endpoints are inside of sip-info.json If you would like to help reverse engineering the SIP protocol you can shoot me an email with your findings.
```python
from textfree import textfree
tf = textfree.Textfree()
tf.createAccount("SomeEmailItDoesntMatter@ligma.vip", "anyPasswordWillDo", "18082222222")
sipUsername = tf.getSipUsername()
sipPassword = tf.getSipPassword()
```
