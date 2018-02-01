$(document).ready(function(){

$('#makeOrder').on('click', makeOrder);
$('#clearOrder').on('click', clearOrder);

var feedback = $('#feedback');

function makeOrder(e){
	e.preventDefault();
	
	var xhr = new XMLHttpRequest();
	
	
	var order = $('input#orderBox').val().toLowerCase();
	if (order.length >= 11){
		feedback.html("Sorry. We don't take orders this large.");
		return
	}
	
	xhr.open('GET', '/serve?order=' + order, true);
	
	xhr.onreadystatechange = function(){
		if (this.readyState == 4){
			// our order is here
			serveOrder(order, this.responseText);
		}
	}
	
	xhr.send();
	feedback.html("processing");
}

function serveOrder(order, delivery){
	package = JSON.parse(delivery);
	
	var time_taken = package["time_taken"];
	var serving = package ["serving"];
	
	var size = serving.length;
	var serving_size = "servings";
	var unit = "seconds";
	
	if (size == 1){
		serving_size = "serving";
	}
	
	if (time_taken == "1.00"){
		unit = "second"
	}
	
	msg = "your order: " + order + "<br/>" + 
		" (" + size + " " + serving_size + " long)" + 
		" [" + time_taken + " " + unit + "]"
	
	feedback.html(msg)
	
	$('#menu').html("working on it.. rendering that is");
}

function clearOrder(e){
	e.preventDefault();
	$("#orderBox").val("");
	$("#feedback").text("how about an order");
	$("#menu").html("");
}

// upper case transform is laggy
$( "#orderBox" ).on( "keyup", function() {
  $( this ).val(function( i, val ) {
    return val.toUpperCase();
  });
});

// close document.ready function()
});