import sys
import telnetlib
import json
from pprint import pprint


class CCFClient(object):
    def __init__(self, host, port):
        self.tn = telnetlib.Telnet(host, port=8899)
        self.get_response(". @ register; request-id aa@CCFCLIENT")
        
    def get_response(self, msg):
        self.tn.write(msg + "\n")
        data = ""
        while True:
            data += self.tn.read_some()
            
            if "\n" in data:
                break
        return data
    
    def get_json(self, struct):
        output = '_ *@CCFSERVER;%s\n' % json.dumps(struct)
        _, jsonString = self.get_response(output).split(";")
        return json.loads(jsonString)

    
if __name__ == "__main__":
    client = CCFClient("ccf.conceptcoding.org", 8899)
    req = {"Q":"lookup",
           "ref":"REF", 
           "seq":12345, 
           "word":"monday", 
           "langIn":"en", 
           "langOut":"bliss"}
    struct = client.get_json(req)
    pprint (map(lambda x: x["repr"], struct["arr"]))
    
    
