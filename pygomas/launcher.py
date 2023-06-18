import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from functions import *
from controllers.home import *
from pygomas.ontology import *
LONG_RECEIVE_WAIT: int = 1000000

class Launcher(Agent):
    
    class getSoldiers(CyclicBehaviour):

        finished_event = ""
        resultAxis = ""
        resultAllied = ""
        serviceName = ""
        XMPPServer= ""

        async def run(self):
            msg = Message()
            msg.set_metadata(PERFORMATIVE, "get")
            msg.to = self.serviceName + "@" + self.XMPPServer
            msg.body = json.dumps({NAME: 'allied', TEAM: 100})
            await self.send(msg)

            result = await self.receive(timeout=LONG_RECEIVE_WAIT)
            
            if result: 
                self.resultAllied = json.loads(result.body)
                 
            msg.body = json.dumps({NAME: 'axis', TEAM: 200})
            await self.send(msg)
    
            result = await self.receive(timeout=LONG_RECEIVE_WAIT)

            if result:
                self.resultAxis = json.loads(result.body)
                self.finished_event.set() 

            self.finished_event.set() ##Acaba la ejecución

                
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

    launcher.web.start(hostname="localhost", port="8001")

    time.sleep(LONG_RECEIVE_WAIT)

    print("----- Launcher cerrado ------")
         



