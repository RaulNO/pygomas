
from django.shortcuts import render, redirect
from mainApp.functions import *
from mainApp.executeGame import ExecuteGame;
from mainApp.map import Map;
from django.utils.translation import gettext_lazy as _
from spade.agent import Agent



executeGame = ExecuteGame()
map = Map()
mainSave = ""


def home(request):
    global map
    global mainSave

    if(request.method == 'GET'):
        mainSave = ""
        map = Map()

        return render(request,'home.html')

def crearConfig(request):
    global mainSave
    if(request.method == 'GET'):
        return render(request,'createConfig.html')
    elif(request.method == 'POST'):
        configName = request.POST.get("NewConfigName")
        if(configName == ""):
            return redirect("/pygomas")
        else:
            createConfigFolder(configName)
            mainSave = configName
            return redirect("/pygomas/menu")
    
def selectConfig(request):  
    global mainSave
    if(request.method == 'GET'):
        saves = obtenerSaves()
        return render(request,'selectConfig.html', {"saves": saves})
    elif(request.method == 'POST'):
        mainSave = request.POST.get("ConfigName")
        return redirect("/pygomas/menu")
    
def menu(request):
    global mainSave
    if(request.method == 'GET'):
        print("MS" + mainSave)
        dataGame = getDataGame(mainSave)
        context = {
            "data_game": dataGame,
            "mainSave" : mainSave
        }
        print(dataGame)
        return render(request,'menu.html', context)

def change_language(request):
    
    redirect_to = request.META.get('HTTP_REFERER') or '/'
    response = redirect(redirect_to)
    response.set_cookie("idioma", request.POST.get("language"))
    return response
           
def agentConfig(request):
    global mainSave
    if(request.method == "GET"):
        dataGame = getDataGame(mainSave)
        context = {
            "data_game": dataGame,
            "mainSave" : mainSave
        }
        return render(request, 'agentConfig.html', context)
    else:
        if(request.POST.get("saveNumberOfPlayers")=="saveButton"):
            number = request.POST.get("players")
            playerNumber = [i for i in range(int(number))]
            dataGame = getDataGame(mainSave)
            context = {'playerNumber': playerNumber, 'number': number, 'data_game': dataGame, 'mainSave':mainSave}
            return render(request, 'agentConfig.html', context)
        else:
            createJSONAgents(request, executeGame)
            return redirect("/pygomas/menu")

def launcher(request):
    global mainSave
    dataGame = getDataGame(mainSave)
    context = {
            "data_game": dataGame,
            "mainSave" : mainSave
        }
    if(request.method == 'GET'):
        
        return render(request, 'launcher.html', context)
    elif(request.method == 'POST'):
        
        manager = request.POST.get('manager')
        soldiers = request.POST.get('soldiers')
        renderI = request.POST.get('render')
    
        if(manager is not None and manager != ""):
            launchLocal(mainSave,manager)
        if(soldiers is not None and soldiers != ""):
            launchLocal(mainSave,soldiers)    
        if(renderI is not None and renderI != ""):
            launchLocal(mainSave, renderI)
        
        return render(request, 'launcher.html', context)
        

        
def createMap(request):
    global mainSave
    global map
    if request.method == 'POST':
        if(request.POST.get("action-button")=="saveMap"):
            map_name =  request.POST.get("map_name")
            map = buildMap(map, request.POST)
            map.createTxt(map_name)
            mapOptions = rellenarMapSelect()
            context = {
                'options': mapOptions,
                'map': map.get_map(),
                'map_name': request.POST.get("map_name")
            }

            return render(request, 'mapEditor.html', context)   

        elif(request.POST.get("action-button")=="loadMap"):
            map.loadMap(request.POST.get("select-map"))  
            mapOptions = rellenarMapSelect()
            context = {
                'options': mapOptions,
                'map': map.get_map(),
                'map_name': request.POST.get("select-map")
            }
            return render(request, 'mapEditor.html', context)   
        
        elif(request.POST.get("action-button")=="assignMap"):
            map_name =  request.POST.get("map_name")
            map = buildMap(map, request.POST)
            map.createTxt(map_name)
            assignMap(mainSave, map_name)
            return redirect("/pygomas/menu")  
       
    else:
        mapOptions = rellenarMapSelect()
        context = {
            'map': map.get_map(),
            'options': mapOptions
        }
        return render(request, 'mapEditor.html', context)


def managerConfig(request):
    global mainSave
    dataGame = getDataGame(mainSave)
    context = {
            "data_game": dataGame,
            "mainSave" : mainSave
        }
    if(request.method == "GET"):
        return render(request, 'managerConfig.html', context)
    else:
        print("Post obtenido")
        configurarManager(mainSave,request)
        return redirect("/pygomas/menu/")
    
def onlinemode(request):
    return render(request, 'onlinemode.html')

def sendManager(request):
    mapOptions = rellenarMapSelect()
    context = {
            'options': mapOptions
        }
    if(request.method == 'GET'):
        return render(request, 'sendManager.html', context)
    else:
        launchManagerOnline(request)
        return render(request, 'sendManager.html')

def sendSoldier(request):
    
    if(request.method == 'GET'):
        return render(request, 'sendSoldier.html')
    else:
        createJson(request)
        launchSoldierOnline()
        return render(request, 'sendSoldier.html')

def sendRender(request):
    if(request.method == 'GET'):
        return render(request, 'sendRender.html')
    else:
        launchRenderOnline(request)
        return render(request, 'sendRender.html')

'''launcher = Agent("launcher@desktop-5hmpkhv", "secret")
launcher.start()

time.sleep(5)
launcher.web.add_get("/pygomas", home, "home.html")
launcher.start(auto_register=True)
launcher.web.start(hostname="127.0.0.1", port="8001")'''

    
   
    

