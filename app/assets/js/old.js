$(document).ready(function(){

$('#order-btn').on('click', makeOrder);
$('#clear-btn').on('click', clearOrder);

var feedback = $('#feedback');

function makeOrder(e){
	e.preventDefault();
	
	var order = $('input#order-box').val().toLowerCase();
	if (order.length >= 13){
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
	delivery = JSON.parse(delivery);
	var order = $("#order-box").val()
	/*
	var time = delivery["time"];
	var size = delivery["size"];
	var serving = delivery["serving"];
	
	var serving_size = "servings";
	var unit = "seconds";
	
	if (size == 1){serving_size = "serving";}
	if (time == "1.00"){unit = "second"}
	
	msg = order + ": " + 
		size + " " + serving_size + " long" + 
		" (" + time + " " + unit + ")"
	
	feedback.text(msg)
	*/
	var serving = delivery["serving"]
	feedback.text(serving)
	$('#canvas').html("package delivered");
}

function clearOrder(e){
	e.preventDefault();
	$("#order-box").val("");
	$("#feedback").text("how about an order");
	$("#canvas").html("");
}

// close document.ready function()
});
