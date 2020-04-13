var alert = new eliminar();
function eliminar() {
    this.render=function(txt){
        var msg = document.getElementById("msg")
        document.getElementById('text-00').innerHTML = txt;
        msg.classList.add("is-active");
    }
    this.confirmar=function(elementId = 'del'){
        var href = document.getElementById(elementId).value;
        window.location.href = href;
    }
    this.cancelar=function(){
        var msg = document.getElementById("msg")
        msg.classList.remove("is-active");
    }   
}

function resetForm(){
    oFormObject = document.forms['filter'];
    elements = oFormObject.elements;
    for (var i = 0, element; element = elements[i++];)
        if(element.type != 'hidden')
            element.value='';
}

function displayDetails(idForDetails){
    var objectDetails = document.getElementById("Details"+idForDetails);
    if(objectDetails.style.display == 'none') {
        objectDetails.style.display = "contents";
    } else objectDetails.style.display = "none";
}

function sortTable(n, isDate) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("table01");
  switching = true;
  dir = "asc";
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 3); i+=2) {
        shouldSwitch = false;
        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 2].getElementsByTagName("TD")[n];
        
        if(isDate != true) {
            xInner=x.innerHTML.toLowerCase();
            yInner=y.innerHTML.toLowerCase();
        } else {
            xInner=new Date(x.getAttribute('date-value'));
            yInner=new Date(y.getAttribute('date-value'));
        } 
        
        if (dir == "asc") {
            if (xInner > yInner) {
                shouldSwitch = true;
                break;
            }
        } else if (dir == "desc") {
            if (xInner < yInner) {
                shouldSwitch = true;
                break;
            }
        }
    }
    if (shouldSwitch) {
        rows[i].parentNode.insertBefore(rows[i + 2], rows[i]);
        rows[i].parentNode.insertBefore(rows[i + 3], rows[i+1]);
        switching = true;
        switchcount ++;
    } else {
        if (switchcount == 0 && dir == "asc") {
            dir = "desc";
            switching = true;
      }
    }
  }
}