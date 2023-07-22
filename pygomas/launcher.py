import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from functions import *
from controllers.home import *
from pygomas.ontology import *
LONG_RECEIVE_WAIT: int = 1000000
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service(executable_path='../dchrome/chromedriver.exe')
driverChrome = webdriver.Chrome(service=service)

class Launcher(Agent):
    
    class getSoldiers(CyclicBehaviour):

        finished_event = ""
        resultAxis = ""
        resultAllied = ""
        serviceName = ""
        XMPPServer= ""

        async def run(self):
            msgAllied = Message()
            msgAllied.set_metadata(PERFORMATIVE, "get")
            msgAllied.to = self.serviceName + "@" + self.XMPPServer
            msgAllied.body = json.dumps({NAME: 'allied', TEAM: 100})

            await self.send(msgAllied)

            resAllied = await self.receive(timeout=LONG_RECEIVE_WAIT)
            
            if resAllied: 
                self.resultAllied = json.loads(resAllied.body)

            msgAxis = Message()
            msgAxis.set_metadata(PERFORMATIVE, "get")
            msgAxis.to = self.serviceName + "@" + self.XMPPServer
            msgAxis.body = json.dumps({NAME: 'axis', TEAM: 200})

            await self.send(msgAxis)
            resAxis = await self.receive(timeout=LONG_RECEIVE_WAIT)

            if resAxis:
                self.resultAxis = json.loads(resAxis.body)

            self.finished_event.set() ##Acaba la ejecución

    class stopGame(OneShotBehaviour):
        manager = ""
        XMPPServer = ""
        print("Deteniendo partida...")
        async def run(self):
            msg = Message()
            msg.to = self.manager + "@" + self.XMPPServer
            msg.set_metadata(PERFORMATIVE, MANAGEMENT_SERVICE)
            msg.body = 'kill'

            await self.send(msg)
            print("Orden de finalizacion enviada")

    class msgToTroop(OneShotBehaviour):
        troop = ""

        async def run(self):
            msg = Message()
            msg.set_metadata(PERFORMATIVE, "get")
            msg.to = self.troop
            msg.body = json.dumps({NAME: 'allied', TEAM: 100})
        
    async def setup(self):
        print("Setup de launcher")
        

        
if __name__ == "__main__":
    print("------ Iniciando launcher ------")
    print("http://localhost:8001/pygomas")

    launcher = Launcher("launcher@desktop-5hmpkhv", "secret")
    launcher.start(auto_register=True)

    launcher.web.app.router.add_static('/static/', path='static', name='static')
    
    launcher.web.add_get('/pygomas', home, 'templates/home.html')
    launcher.web.add_post('/pygomas', home, 'templates/home.html')
    
    launcher.web.add_get('/pygomas/menu', lambda request: menu(request, launcher), 'templates/menu.html')
    launcher.web.add_post('/pygomas/menu', lambda request: menu(request, launcher), 'templates/menu.html')

    launcher.web.add_get('/pygomas/menu/mapEditor', createMap, 'templates/mapEditor.html')
    launcher.web.add_post('/pygomas/menu/mapEditor', createMap, 'templates/mapEditor.html')

    launcher.web.add_get('/pygomas/menu/monitorize', lambda request: monitorizar(request, launcher), 'templates/monitorize.html')
    launcher.web.add_post('/pygomas/menu/monitorize', lambda request: monitorizar(request, launcher), 'templates/monitorize.html')

    launcher.web.add_get('/pygomas/getAgentList', lambda request: getAgentList(request, launcher), template=None)

    launcher.web.add_get('/pygomas/exit', lambda request: exit(request, launcher, driverChrome), template=None)

    launcher.web.start(hostname="localhost", port="8001")

    driverChrome.get("http://localhost:8001/pygomas")

    time.sleep(LONG_RECEIVE_WAIT)
    print("----- Launcher cerrado ------")
         



