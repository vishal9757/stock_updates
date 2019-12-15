function generateStatsWindow(e){
  var input = document.getElementById('myInput').value
  axios.get("/company_stats?companyName="+input).then(function(res){
    if (res.data['NAME'] != null){
      buildTable([res.data], 'modalContent')
    }
    else{
      buildMessage("No such Company", "modalContent")
    }
  })
  e.preventDefault()
  return false
}

function autocomplete(inp) {
  var currentFocus;
  inp.addEventListener("input", function(e) {
    var self = this
      axios.get('/company_suggestions?text='+this.value.toUpperCase())
        .then(function(res) {
          var a, b, i, val = self.value;
          var arr = res.data && res.data.companies ? res.data.companies : []
          closeAllLists();
          if (!val) { return false;}
          currentFocus = -1;
          a = document.createElement("DIV");
          a.setAttribute("id", self.id + "autocomplete-list");
          if (arr.length > 0){
            a.setAttribute("class", "autocomplete-items");}
          self.parentNode.appendChild(a);
          for (i = 0; i < arr.length; i++) {
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
              b = document.createElement("DIV");
              b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
              b.innerHTML += arr[i].substr(val.length);
              b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
              b.addEventListener("click", function(e) {
                  inp.value = this.getElementsByTagName("input")[0].value;
                  closeAllLists();
              });
              a.appendChild(b);
            }
          }
        })
  });
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        currentFocus++;
        addActive(x);
      } else if (e.keyCode == 38) { //up
        currentFocus--;
        addActive(x);
      } else if (e.keyCode == 13) {
        e.preventDefault();
        if (currentFocus > -1) {
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

function buildTable(responseData, id, click_function){
  var element = document.getElementById(id)
  element.innerText = ""
  var table = document.createElement('table')
  table.className = 'table table-hover table-bordered'
  var field = Object.keys(responseData[0])
  var node = document.createElement('thead')
  table.appendChild(node)
  var row = document.createElement('tr')
  row.onclick = 
  node.appendChild(row)
  for (var key in field){
    var data = document.createElement('th')
    data.style = "text-align:center;"
    if (click_function == true){
    data.innerHTML = "<b>"+field[key]+"</b> <i class='fa fa-fw fa-sort' onclick=sortedResponse('"+field[key]+"')></i>"
    }else {
      data.innerText = field[key]
    }

    row.appendChild(data)
  }
  var node = document.createElement('tbody')
  table.appendChild(node)
  for (row_index in responseData){
    var row = document.createElement('tr')

    node.appendChild(row)
    for (var key in field){
      var data = document.createElement('td')
      data.style = "text-align: center;"
      data.innerText = responseData[row_index][field[key]]
      row.appendChild(data)
    }
  }
  element.appendChild(table)
}

function sortedResponse(sortKey){
  element = document.getElementById('sortTableBlock')
  meta_element = document.getElementById('sortMeta')
  meta_element.innerText = ""
  node = document.createElement('h3')
  node.innerText = "Sorted Table ("+sortKey+")"
  meta_element.appendChild(node)
  axios.get("/sorted_company?sort="+sortKey).then(function(res){
      buildTable(res.data, 'sortTableBlock', click_function=true)
  })
  return false
}

function buildMessage(message, id){
  element = document.getElementById(id)
  element.innerText = ""
  node = document.createElement('h3')
  node.innerText = message
  element.appendChild(node)
}