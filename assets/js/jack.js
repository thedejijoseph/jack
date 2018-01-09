$(document).ready(function(){

$('#makeOrder').on('click', makeOrder);
$('#orderBox').on('keyup', uppercaseTransform);
$('#clearOrder').on('click', clearOrder);

function makeOrder(e){
	e.preventDefault();
	
	var xhr = new XMLHttpRequest();
	
	var feedback = $('#feedback');
	var order = $('input#orderBox').val();
	
	if (order.length >= 11){
		feedback.html("Sorry. We don't take orders this large.");
		return
	}
	
	xhr.open('GET', '/serve?order=' + order.toLowerCase(), true);
	
	xhr.onreadystatechange = function(){
		if (this.readyState == 4){
			// our order is here
			serveOrder(this.responseText);
		}
	}
	
	xhr.send();
	feedback.html("processing");
}

function serveOrder(delivery){
	delivery = JSON.parse(delivery);
	
	var size = delivery.length;
	var serving_size;
	var feedback = $('#feedback');
	
	if (size == 1){
		serving_size = "serving";
	}else{serving_size = "servings";}
	
	var msg = "here's your order (" + size + " " + serving_size + " long)"
	
	feedback.html(msg)
	serving = "<ul>";
	
	delivery.forEach(function(item) {
		serving += "<li>" + item.toUpperCase() + "</li>";
	});
	
	serving += "</ul>";
	$('#menu').html(serving);
}
function clearOrder(e){
	e.preventDefault();
	document.getElementById("orderBox").value = "";
	document.getElementById("menu").innerHTML = "";
	feedback.innerHTML = "";
}

function uppercaseTransform(){
	var orderBox = $('#orderBox');
	var ugly = orderBox.val()
	var fine = ugly.toUpperCase();
	orderBox.val() = fine;
	alert("grapes")
}

// close document.ready function()
});