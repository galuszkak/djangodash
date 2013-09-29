$(document).ready(function(){
		var username = $("#username").text(); 
		var usocket = io.connect('/users');
		
		usocket.on('join', function(users){
			var tbl_body = "";
			for (var i = 0; i < users.length; i++) {
				tbl_body += "<tr><td>" + users[i].username + "</td>" + "<td>" + users[i].gamestate + "</td>";
				if(users[i].gamestate == 2  ){
					tbl_body += "<td></td>";
				}
				else{
					tbl_body += "<td><button>Small button</button></td>";
				}
			}
			$('#playerTable').append(tbl_body);	
		});		
		
		usocket.on('connected', function(user) {
			var tbl_body = "";
			tbl_body += "<tr><td>" + user.username + "</td>" + "<td>" + user.gamestate + "</td>";
			if(user.gamestate == 2  ){
				tbl_body += "<td></td>";
			} else {
				tbl_body += "<td><button>Small button</button></td>";
			}
			tbl_body += "</tr>";
			$('#playerTable').append(tbl_body);	
		});
		
		
		usocket.emit('join', {'username':username});
});