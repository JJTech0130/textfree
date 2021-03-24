from textfree import textfree

def main():
    
    #tf = textfree.Textfree(proxy={"http" : "socks5://localhost:9050", "https" : "socks5://localhost:9050"})
    tf = textfree.Textfree()
    print(tf.getAvailableNumbers("831"))
    print(tf.createAccount("dawdssweaddddsss@sdsedfsfd.com", "dwaDaww", "2322222222"))
    print(tf.sendMessage("hello world", "2322222222"))
    
main()
