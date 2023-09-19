import urllib.parse
import asyncio
from functions import *
from MapObject import Map
from aiohttp import web
from spade.template import Template

map = Map()
mainSave = ""
# Crear una instancia del controlador ChromeDriver

async def home(request):
    global mainSave
    saves = obtenerSaves()

    if(request.method == 'POST'):
        form = await request.post()
        formName = form.get('button')

        if(formName == 'loadGame'): ##Cargamos partida
            mainSave = str(form.get('GameName'))
            raise web.HTTPFound("/pygomas/menu")

        elif(formName == 'createGame'):
            createConfigFolder(str(form.get('GameName')))
            mainSave = str(form.get('GameName'))

            raise web.HTTPFound("/pygomas/menu")
    return {
         "saves": saves
    }

async def menu(request, launcher):
    global mainSave
    dataGame = getDataGame(mainSave)
    
    if(request.method == 'POST'):
        formData = await request.post()
        formName = formData.get('button')

        if(formName == 'showSoldiers'):
            number = formData.get('players')
            playerNumber = [i for i in range(int(number))]
            data = {'playerNumber': playerNumber, 'number': number, 'data_game': dataGame, 'mainSave':mainSave, 'form' : "configPlayers"}
            return data
        elif(formName == 'saveSoldiers'):
            createJSONAgents(request , formData, dataGame)
            assignTroops(mainSave, formData.get("troopsName"))
            raise web.HTTPFound("/pygomas/menu") 
        elif(formName == 'saveManager'):
            configurarManager(mainSave,formData)
            data={'data_game': getDataGame(mainSave), 'mainSave':mainSave, 'form' : "configManager"}
            raise web.HTTPFound("/pygomas/menu") 
        elif(formName=='launchManager'):
            launchManagerOnline(formData)
            time.sleep(5)
            template = Template()
            template.set_metadata('performative', 'finished_game')
            launcher.informFinishedGameBehaviour = launcher.informFinishedGame()
            launcher.add_behaviour(launcher.informFinishedGameBehaviour, template) 
        elif(formName=="launchSoldiers"):
            createJson(formData)
            launchSoldierOnline()
            time.sleep(3)            

        elif(formName=="launchRender"):
            launchRenderOnline(formData)

        elif(formName=='launchLocal'):
            manager = formData.get('manager')
            soldiers = formData.get('soldiers')
            renderI = formData.get('render')
    
            if(manager is not None and manager != ""):
                launchLocal(mainSave,manager)
            if(soldiers is not None and soldiers != ""):
                modifyJSON(formData.get("JSONFile"), dataGame, mainSave)
                launchLocal(mainSave,soldiers)    
            if(renderI is not None and renderI != ""):
                launchLocal(mainSave, renderI)

            template = Template()
            template.set_metadata('performative', 'finished_game')
            launcher.informFinishedGameBehaviour = launcher.informFinishedGame()
            launcher.add_behaviour(launcher.informFinishedGameBehaviour, template)            
        
        elif(formName=='monitorize'):
            
            launcher.soldiers = launcher.getSoldiers()

            launcher.soldiers.serviceName = formData.get('spectatedService')
            launcher.soldiers.XMPPServer = formData.get('XMPPServer')
            launcher.soldiers.finished_event = asyncio.Event()

            launcher.add_behaviour(launcher.soldiers)
            await launcher.soldiers.finished_event.wait()

            url = f"/pygomas/menu/monitorize"
            raise web.HTTPFound(url)    
        
    context = {
        'maps': rellenarMapSelect(),
        'troops_files': obtainTroopsFiles(),
        "data_game": dataGame,
        "mainSave" : mainSave
    }

    return context

async def createMap(request):
    global mainSave
    global map
    mapOptions = rellenarMapSelect()

    if request.method == 'POST':
        formData = await request.post()
        formName = formData.get('button')

        if(formName=='saveMap'):
            map_name =  formData.get("map_name")
            map = buildMap(map, formData)
            map.createTxt(map_name)
            
            context = {
                'options': rellenarMapSelect(),
                'map': map.get_map(),
                'map_name': map_name
            }

            return context   

        elif(formName == 'loadMap'):
            map.loadMap(formData.get("select-map"))  
            mapOptions = rellenarMapSelect()
            context = {
                'options': mapOptions,
                'map': map.get_map(),
                'map_name': formData.get("select-map")
            }
            return context   
        
        elif(formName=="assignMap"):
            map_name =  formData.get("map_name")
            map = buildMap(map, formData)
            map.createTxt(map_name)
            assignMap(mainSave, map_name)
            raise web.HTTPFound("/pygomas/menu") 
        
    context = {
        'map': map.get_map(),
        'options': mapOptions
    }
    return context

async def monitorizar(request, launcher):
    global mainSave
    
    if request.method == 'GET':
        initAlliedSoldiers = launcher.soldiers.resultAllied
        initAxisSoldiers = launcher.soldiers.resultAxis
        return {'initAlliedSoldiers':initAlliedSoldiers,'initAxisSoldiers':initAxisSoldiers}
    
    elif request.method == 'POST':
        '''enviar mensajes a troops''' 
   
async def getAgentList(request, launcher):
    global mainSave
    axisSoldiers = launcher.soldiers.resultAxis
    alliedSoldiers = launcher.soldiers.resultAllied
    finishedGame = launcher.informFinishedGameBehaviour.finished
    
    return {
       'axisSoldiers': axisSoldiers,
       'alliedSoldiers' : alliedSoldiers,
       'finishedGame' : finishedGame
    }

async def exit(request, launcher, driverChrome):
    driverChrome.quit()
    await launcher.stop(); 

async def stopManager(request, launcher):
        dataGame = getDataGame(mainSave) 
        launcher.killManagerBehaviour = launcher.killManager()
        launcher.killManagerBehaviour.manager = dataGame["MANAGER"]
        launcher.killManagerBehaviour.XMPPServer = dataGame["SERVER"]
        launcher.add_behaviour(launcher.killManagerBehaviour)
        raise web.HTTPFound("/pygomas/menu")

async def viewstats(request, launcher):
    global mainSave
    getStats(mainSave)
    dir = "saves/"+mainSave+"/pygomas_stats.txt"
    print(dir)
    try:
        with open(dir, 'r') as archivo:
            content = archivo.read()
        return {
            'content': content,
            'save' : mainSave

        }
    except FileNotFoundError:
        return {
            'content' : "No se ha ejecutado ninguna partida en " + mainSave
        }
        
 
        
  

     
    


