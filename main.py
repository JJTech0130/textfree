from textfree import textfree

def main():

    tf = textfree.Textfree()
    #print(tf.getAvaliableNumbers("808")) # gets available 808 numbers

    print(tf.login("dwaDwa2@2dwad.com", "Dwa123131"))
    print(tf.getSipUsername())
    print(tf.getSipPassword())

main()
