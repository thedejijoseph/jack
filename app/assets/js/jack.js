$(document).ready(function(){

$('#order-btn').on('click', makeOrder);
$('#clear-btn').on('click', clearOrder);

var feedback = $('#feedback');

function makeOrder(e){
	e.preventDefault();
	
	var order = $('input#order-box').val().toLowerCase();
	if (order.length >= 11){
		feedback.text("Sorry. We don't take orders this large.");
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
	var order = $("#order-box").val()
	
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
	
	$('#canvas').html("working on it.. rendering that is");
}

function clearOrder(e){
	e.preventDefault();
	$("#order-box").val("");
	$("#feedback").text("how about an order");
	$("#canvas").html("");
}

// close document.ready function()
});
