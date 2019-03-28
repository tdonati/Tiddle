var myButton = document.querySelector('button');

myButton.onclick = function(){
	getTwitterName();
}

function getTwitterName(){
	var myName = prompt('Please enter your Twitter name.');
	localStorage.setItem('name',myName);
}
