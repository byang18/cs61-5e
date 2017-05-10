# pylint: disable=C0111, C0103

name = raw_input("Enter your name: ")

while name != "quit":
    print name
    name = raw_input("Enter your name: ")
