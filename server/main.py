from fastapi import FastAPI
import requests
from hashlib import md5
app = FastAPI()
uplinkedMessages = [] # {"content":message content,"serversSent": all servers that got /sendCheck sent to them,"serversReceived": all servers that sent /sendCheck to us,'ackedServers':amount of servers that received request}
otherServers = []
@app.get('/onlineCheck')
def onlineCheck():
  return {"status": "online"}

@app.get('/uplinkMessage')
def uplinkMessage(message):
  sect = len(uplinkedMessages)
  uplinkedMessages.append({'content':message,'serversSent':[],'serversReceived':[],'serversFailed':[]})
  return uplinkedMessages[sect]
  
@app.get('/receiveMessages')
def receiveMessage():
  tr = []
  for uplinkedMessage in uplinkedMessages:
    for server in otherServers:
      try:
        requests.get('http://'+server+'/messageDelete',params={"td":uplinkedMessages.index(uplinkedMessage)})
      except requests.exceptions.ConnectionError:
        print('Server '+server+' is offline.')
    tr.append(uplinkedMessage['content'])
    del uplinkedMessages[uplinkedMessages.index(uplinkedMessage)]
  return tr


@app.get('/messageDelete')
def messageDelete(td:int):
  del uplinkedMessages[td]
  return True