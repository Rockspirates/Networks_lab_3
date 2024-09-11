import os
from dotenv import load_dotenv

load_dotenv()

class computer:
    def __init__(self, macaddress):
        #There are 3 possible states base, sender, reciever
        self.mac = macaddress
        self.state = "BASE"
        #If you are in base the following 2 will be None
        #If you are a reciever, then waitingfor_mac will have sender MAC
        self.waitingfor_mac = None
        #If you are a sender, then sendingto_mac will have reciever MAC
        self.sendingto_mac = None

    def updatestate(self,state,sender,reciver):
        self.state = state
        self.waitingfor_mac = sender
        self.sendingto_mac = reciver

    def get_time(self):
        if self.state == "BASE":
            return os.getenv("ACK_RTS")
        elif self.state == "SENDER":
            return os.getenv("MESSAGE_ACK")
        elif self.state == "RECIEVER":
            return os.getenv("CTS_MESSAGE")
        
    def timeout(self):
        if self.state == "BASE":
            return -1
