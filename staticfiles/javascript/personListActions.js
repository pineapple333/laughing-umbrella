//variables for my shopping list
var input = document.getElementById("userinput");
var button = document.getElementById("enter");
var ul = document.querySelector("ul");
var list = document.getElementsByTagName("li");
var trash = document.getElementsByClassName("delete");
var btndelete = document.getElementById("trash");
var addNewFormField = document.getElementById("addNew");
// const myUL = document.getElementById("bold");

//For removing items with delete button
Array.prototype.slice.call(trash).forEach(function(item) {
  item.addEventListener("click", function(e) {
    e.target.parentNode.remove()
  });
})

var authors = [];

//loop for to strikeout the list
for (var i = 0; i < list.length; i++) {
  list[i].addEventListener("click", strikeout);
}

//toggle between classlist
function strikeout() {
  this.classList.toggle("done");
}

//check the length of the string entered
function inputlength() {
  return input.value.length;
}

//collect data that is inserted
function addli() {
  var li = document.createElement("div");
  var btn = document.createElement("button");
  var div = document.createElement("div");

  li.addEventListener("click", strikeout);
  li.className = "author-search-card";

  btn.className = "delete-bttn";
  btn.innerHTML = "x";

  div.className = "authorName";
  div.innerText = input.value + "";

  li.appendChild(div);
  li.appendChild(btn);

  ul.appendChild(li);

  authors.push(input.value);

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

//this will add a new list item after click
function addListAfterClick() {
  if (inputlength() > 0) {
    addli();
  }
}

//this will add a new list item with keypress
function addListKeyPress(event) {
  if (inputlength() > 0 && event.which === 13) {
    addli();
  }
}

//this will check for the event/keypress and create new list item
input.addEventListener("keypress", addListKeyPress);

//this will check for a click event and create new list item
button.addEventListener("click", addListAfterClick);