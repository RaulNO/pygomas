import urllib.parse
import asyncio
from functions import *
from executeGame import ExecuteGame;
from MapObject import Map;
from aiohttp import web

executeGame = ExecuteGame()
map = Map()
mainSave = ""
initAlliedSoldiers = ""
initAxisSoldiers = ""
firstLoad = True;

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
            createJSONAgents(request, executeGame)
            ##return redirect("/pygomas/menu")
        elif(formName == 'saveManager'):
            configurarManager(mainSave,formData)
            data={'data_game': getDataGame(mainSave), 'mainSave':mainSave, 'form' : "configManager"}
            return data
        elif(formName=='launchManager'):
            print("Lanzando manager...")
            launchManagerOnline(formData)
            time.sleep(20)
            

        elif(formName=="launchSoldiers"):
            print("Lanzando soldier...")
            createJson(formData)
            launchSoldierOnline()
            time.sleep(10)            

        elif(formName=="launchRender"):
            print("Lanzando render...")
            launchRenderOnline(formData)

        elif(formName=='launchLocal'):
            manager = formData.get('manager')
            soldiers = formData.get('soldiers')
            renderI = formData.get('render')
    
            if(manager is not None and manager != ""):
                launchLocal(mainSave,manager)
            if(soldiers is not None and soldiers != ""):
                launchLocal(mainSave,soldiers)    
            if(renderI is not None and renderI != ""):
                launchLocal(mainSave, renderI)
        
        elif(formName=='monitorize'):
            print("Monitorizando...")

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
    global initAlliedSoldiers, initAxisSoldiers, firstLoad
    if(firstLoad):
        print(firstLoad)
        firstLoad = False;
        ##Lista inicial de soldados (todos vivos) solo se ejecuta una vez
        initAlliedSoldiers = launcher.soldiers.resultAllied
        initAxisSoldiers = launcher.soldiers.resultAxis
        ##Listas actualizables
        alliedSoldiers = launcher.soldiers.resultAllied
        axisSoldiers = launcher.soldiers.resultAxis
        return {'alliedSoldiers':alliedSoldiers, 'axisSoldiers': axisSoldiers,'initAlliedSoldiers':initAlliedSoldiers,'initAxisSoldiers':initAxisSoldiers, 'firstLoad':'true'}
    else:
        print(firstLoad)

        alliedSoldiers = launcher.soldiers.resultAllied
        axisSoldiers = launcher.soldiers.resultAxis
        return {'alliedSoldiers':alliedSoldiers, 'axisSoldiers': axisSoldiers,'initAlliedSoldiers':initAlliedSoldiers,'initAxisSoldiers':initAxisSoldiers, 'firstLoad':'false'}
    

     
    


