$(document).ready(function(){
	// APP VARIABLES
	let dev_socket = "ws://localhost:3303/serve"
	let prod_socket = "ws://wx-jack.herokuapp.com/serve"
	let dest_socket = prod_socket
	
	// EVENT LISTENERS
	
	// event listener (-ish) to determine server in operation
	let check_server = function(){
		s = new WebSocket("ws://localhost:3303/handshake")
		s.onopen = function(){
			s.send("hello")
		}
		s.onmessage = function(e){
			var reply = e.data;
			if (reply == "hi"){
                dest_socket = dev_socket;
			}
		}
	}
	
	// event listener on clear btn
	$("#clear-btn").on("click", function(e){
		e.preventDefault();
		$("#feedback").text("how about an order");
		$("#order-box").val("");
		$("#canvas").html("");
	});
	
	// event listener on order btn
	$("#order-btn").on("click", function(e){
		e.preventDefault();
		
		var order = $("#order-box").val()
		if (order == ""){return;}
		if (order.length >= 12){
			$("#feedback").text("We don't serve orders this large")
			return;
		}
		
		// open a new websocket
		socket = new WebSocket(dest_socket)
		socket.onopen = function(){
			var orderPacket = {"order": order}
			socket.send(JSON.stringify(orderPacket))
			$("#canvas").html("");
		}
		
		socket.onmessage = function(event){
			$("#feedback").text("serving...");
			
			var packet = event.data;
			serve(packet)
		}
		
		socket.onclose = function(){
			// pass
			return;
		}
	})
	
	// APP FUNCTIONS
	
	let wrap = function(el, content, attrs){
		// wrap content in given element tags
		p_attrs = ""
		if (attrs){
			Object.keys(attrs).forEach(function(key){
				attr = key;
				val = attrs[key].join(" ");
				pair = attr + "=" + '"' + val + '"'
				p_attrs += pair
			});
		}
		opening = "<" + el + " " + p_attrs + ">"
		closing = "</" + el + ">"
		return opening + content + closing
		// pretty much minimal
	}
	
	let serve = function(packet){
		// unpack packet
		packet = JSON.parse(packet)
		var end = packet["time"];
		if (end){
			order = packet["order"]
			count = packet["count"]
			total_time = packet["time"]
			
			s1 = order + ": ";
			s2 = count + " total "
			s3 = "in " + total_time + "s."
			$("#feedback").text(s1 + s2 + s3);
			return
		}
		
		// if not..
		serving = packet["serving"];
		blk_size = packet["blk_size"];
		blk_count = packet["blk_count"];
		
		size = blk_size + " lettered"
		count = blk_count + " large"
		desc = wrap("span", size + " " + count)
		t_btn = wrap("span", "", {"onclick": ["$(this).parent().siblings('div').toggle()"], "class": ["tgl-btn"]})
		
		header = wrap("div", desc + t_btn, {"class": ["blk-header"]})
		
		let rows = ""
		for (block_id in serving){
			block = serving[block_id]
			let row = ""
			for (word_id in block){
				word = block[word_id]
				p_word = wrap("td", word)
				row += p_word
			}
			p_row = wrap("tr", row)
			rows += p_row
		}
		
		head = wrap("thead", "")
		body = wrap("tbody", rows)
		table = wrap("table", head + body, {"class": ["table"]})
		
		content = wrap("div", table, {"class": ["blk-content"], "style": ["display: none;"]})
		
		packet = wrap("div", header + content, {"class" 
: ["packet"]})
		$("#canvas").append(packet)
	}
	
	// START APP
	// on loading variables, functions and listeners
	// call whatever needs to start the app
	check_server();
});
