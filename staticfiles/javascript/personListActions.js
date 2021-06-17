var input = document.getElementById("userinput");
var button = document.getElementById("enter");
var ul = document.querySelector("ul");
var list = document.getElementsByTagName("li");
var trash = document.getElementsByClassName("delete");
var btndelete = document.getElementById("trash");
var addNewFormField = document.getElementById("addNew");
var file_input = document.getElementById('input-list');

Array.prototype.slice.call(trash).forEach(function(item) {
  item.addEventListener("click", function(e) {
    e.target.parentNode.remove()
  });
})

var authors = [];

for (var i = 0; i < list.length; i++) {
  list[i].addEventListener("click", strikeout);
}

function strikeout() {
  this.classList.toggle("done");
}

function inputlength() {
  return input.value.length;
}

function addli(input_val) {
console.log("adding " , input_val)
  var li = document.createElement("div");
  var btn = document.createElement("button");
  var div = document.createElement("div");

  li.addEventListener("click", strikeout);
  li.className = "author-search-card";

  btn.className = "delete-bttn";
  btn.innerHTML = "x";

  div.className = "authorName";
  div.innerText = input_val + "";

  li.appendChild(div);
  li.appendChild(btn);

  ul.appendChild(li);

  authors.push(input_val);

  updateFormField();
  btn.addEventListener("click", function(e) {
    var index = authors.indexOf(e.target.parentNode.getElementsByClassName("authorName")[0].innerHTML);
    if (index !== -1) {
      authors.splice(index, 1);
    }
    updateFormField();
    e.target.parentNode.remove();
  });

  input.value = "";
}

function updateFormField() {
    addNewFormField.value = authors.join(";");
}

function addListAfterClick() {
  if (inputlength() > 0) {
    addli(input.value);
  }
}

file_input.onchange = function(event){
  var file = this.files[0];
  var reader = new FileReader();
  reader.onload = function(progressEvent){

    var lines = this.result.split('\n');
    for(var line = 0; line < lines.length; line++){
      addli(lines[line]);
    }
  };
  reader.readAsText(file);
  event.target.value = '';
};

function addListKeyPress(event) {
  if (inputlength() > 0 && event.which === 13) {
    addli();
  }
}

input.addEventListener("keypress", addListKeyPress);

button.addEventListener("click", addListAfterClick);