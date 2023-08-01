const MAX_FLAG = 1;
const MAX_AXIS = 2;
const MAX_ALLIED = 2;

var toggleButtons;
console.log(toggleButtons);
var coords;
var mode = ""
var maxFlag = MAX_FLAG
var maxAxis = MAX_AXIS
var maxAllied = MAX_ALLIED
var FirstAxis = ""
var SecondAxis = ""
var FirstAllied = ""
var SecondAllied = ""

var activeButton = null;
    

document.addEventListener('DOMContentLoaded', function() {
    coords = document.getElementsByName('coords');
    console.log(coords);
    coords.forEach(function (td) {
        td.addEventListener('click', function () {
            var input;
            input = td.querySelector('input');
            if (mode != "" && mode != "box") {
                input.value = mode;
                td.className = "box has-" + mode
                controlMaxBox(input.name);
            }
            else if (mode == "box"){
                if(input.value == "axis" || input.value == "allied"){
                    deleteSpawn(input.value);
                }else if(input.value == "flag"){
                    input.value = "";
                    td.className = mode;
                    maxFlag = MAX_FLAG
                    document.getElementById("add-flag-button").disabled = false;
                    document.getElementById("add-flag-button").className = "toggle-button";
                }
                else{
                    input.value = "";
                    td.className = mode; 
                }
            }
            
        })
    });
    toggleButtons = document.querySelectorAll('.toggle-button');
    console.log(toggleButtons);
    toggleButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            console.log("click en button");
            changeActiveButton(button);
        });
    });
  });


function controlMaxBox(coord){
    
    if(mode=="flag"){
        maxFlag--;
    } else if (mode == "axis"){
        maxAxis--;
    } else if(mode == "allied"){
        maxAllied--;
    }


    if(maxFlag == 0 && mode=="flag"){
        var addFlagButton = document.getElementById("add-flag-button");
        addFlagButton.className = "disabled"
        addFlagButton.disabled = true;
        mode = "";
    }

    if(maxAxis == 0 && mode == "axis"){
        SecondAxis = coord;
        formarArea(FirstAxis, SecondAxis, mode);
        var addAxisButton = document.getElementById("add-spawn-axis-button");
        addAxisButton.className = "disabled"
        addAxisButton.disabled = true;
        mode = "";
    }else if(maxAxis == 1 && mode == "axis"){
        FirstAxis = coord; 
    }

    if(maxAllied == 0 && mode == "allied"){
        SecondAllied = coord;
        formarArea(FirstAllied, SecondAllied, mode);
        var addAlliedButton = document.getElementById("add-spawn-allied-button");
        addAlliedButton.className = "disabled"
        addAlliedButton.disabled = true;
        mode = "";
    }else if(maxAllied == 1 && mode == "allied"){
        FirstAllied = coord;
    }
}

function changeActiveButton(button) {
    if (activeButton) {

        activeButton.classList.remove('active');
    }

    activeButton = button;
    mode = activeButton.value
    activeButton.classList.add('active');
}



function reset (){

}

function formarArea(coord1, coord2, mode) {
    const [x1, y1] = coord1.split("-").map(coord => parseInt(coord));
    const [x2, y2] = coord2.split("-").map(coord => parseInt(coord));

    const ancho = Math.abs(x2 - x1) + 1;
    const alto = Math.abs(y2 - y1) + 1;

    const area = {
        x: Math.min(x1, x2),
        y: Math.min(y1, y2),
        ancho,
        alto
    };

    const coordenadas = [];
    for (let i = area.x; i < area.x + area.ancho; i++) {
        for (let j = area.y; j < area.y + area.alto; j++) {
            coordenadas.push(`${i}-${j}`);
        }
    }

    rellenarArea(coordenadas, mode)
}

function rellenarArea(coordsArea, mode){
    coordsArea.forEach(coord => {
        const input = document.querySelector(`input[name="${coord}"]`);
        if (input && input.value !== "wall" && input.value !== "flag") {
          input.value = mode;
          const td = input.parentNode;
          if (!td.classList.contains("has-axis")) {
            td.className = "box has-" + mode;
          }
        }
      });
}

function deleteSpawn(team){
    var coordsSpawn = document.querySelectorAll(".box.has-"+team);
    coordsSpawn.forEach((td) => {
        td.querySelector('input').value = "";
        td.className= "box"
    });
     
    if(team == "axis"){
        maxAxis = MAX_AXIS;
        document.getElementById("add-spawn-axis-button").disabled = false;
        document.getElementById("add-spawn-axis-button").className = "toggle-button";
    }
    else{
        maxAllied = MAX_ALLIED;
        document.getElementById("add-spawn-allied-button").disabled = false;
        document.getElementById("add-spawn-allied-button").className = "toggle-button";
    }
}

function checkElements(){
    var flag = document.querySelectorAll(".box.has-flag");
    var axis = document.querySelectorAll(".box.has-axis");
    var allied = document.querySelectorAll(".box.has-allied");
    if (flag.length > 0) {
        maxFlag = 0;
        document.getElementById("add-flag-button").className = "disabled";
        document.getElementById("add-flag-button").disabled = true;
    }
    if (axis.length > 0) {
        maxAxis = 0;
        document.getElementById("add-spawn-axis-button").className = "disabled";
        document.getElementById("add-spawn-axis-button").disabled = true;
    }
    if (allied.length > 0) {
        maxAllied = 0;
        document.getElementById("add-spawn-allied-button").className = "disabled";
        document.getElementById("add-spawn-allied-button").disabled = true;
    }
    
}