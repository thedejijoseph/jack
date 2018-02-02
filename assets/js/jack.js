$(document).ready(function(){

$('#makeOrder').on('click', makeOrder);
$('#clearOrder').on('click', clearOrder);

var feedback = $('#feedback');

function makeOrder(e){
	e.preventDefault();
	
	var order = $('input#orderBox').val().toLowerCase();
	if (order.length >= 11){
		feedback.html("Sorry. We don't take orders this large.");
		return
	}
	feedback.html("processing");
	$.ajax("/serve",
		{
			method: "GET",
			data: {
					"order": order
				},
			success: serveOrder,
		});
}

function serveOrder(delivery, status, xhr){
	package = JSON.parse(delivery);
	var order = $("#orderBox").val()
	
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
	
	msg = order + ": " + 
		size + " " + serving_size + " long" + 
		" (" + time_taken + " " + unit + ")"
	
	feedback.html(msg)
	
	$('#menu').html("working on it.. rendering that is");
	// $('#menu').text(serving)
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