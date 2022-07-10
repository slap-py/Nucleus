from fastapi import FastAPI
import requests
from hashlib import md5
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
import whatismyip

otherServers = []
print('This instance\'s IP is '+whatismyip.whatismyip())
otherServers = input('What is the other instance\'s IPs: ').split(',')

app = FastAPI()
uplinkedMessages = [] # {"content":message content,"serversSent": all servers that got /sendCheck sent to them,"serversReceived": all servers that sent /sendCheck to us,'ackedServers':amount of servers that received request}

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates") #return templates.TemplateResponse("item.html", {"request": request, "id": id})


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.get('/onlineCheck')
def onlineCheck():
  return {"status": "online"}

@app.get('/uplinkMessage')
def uplinkMessage(message,sender=None):
  sect = len(uplinkedMessages)
  if sender == None:
    sender = "Anonymous User"
  uplinkedMessages.append({'content':message,'serversSent':[],'serversReceived':[],'serversFailed':[],"sender":sender})
  return uplinkedMessages[sect]
  
@app.get('/receiveMessages')
def receiveMessage():
  tr = []
  for uplinkedMessage in uplinkedMessages:
    if "".join(otherServers) == "":
      pass
    else:
      for server in otherServers:
        try:
          requests.get('http://'+server+'/messageDelete',params={"td":uplinkedMessages.index(uplinkedMessage)})
        except requests.exceptions.ConnectionError:
          print('Server '+server+' is offline.')
    tr.append({"content":uplinkedMessage['content'],"sender":uplinkedMessage['sender']})
    del uplinkedMessages[uplinkedMessages.index(uplinkedMessage)]
  return tr


@app.get('/messageDelete')
def messageDelete(td:int):
  del uplinkedMessages[td]
  return True

@app.get('/integrityTest')
def integrityTest():
  return '"'+md5(open('main.py','r').read().encode()).hexdigest()+'"'