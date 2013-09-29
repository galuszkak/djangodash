$(document).ready(function() {
	var username = $("#username").text();
	var usocket = io.connect('/users');

	usocket.on('join', function(users) {
		var tbl_body = "";
		for (var i = 0; i < users.length; i++) {
			
			tbl_body += "<tr id='" + users[i].username + "'><td>" + users[i].username + "</td>" + "<td>" + users[i].gamestate + "</td>";

			if(username == users[i].username) {
				tbl_body += "<td><a href=\"/create_game\" class=\"btn btn-info\">Create game.</a></td>";
				continue;
			}
			
			if (users[i].gamestate == 1) {
				//tbl_body += "<td><button type=\"button\" class=\"btn btn-success\">Waiting. Click to play with me :)</button></td>";
				tbl_body += "<td></td>";
			} else if (users[i].gamestate == 2) {
				tbl_body += "<td><button type=\"button\" class=\"btn btn-danger\">I'm playing. Do not disturb :)</button></td>";
			} else {
				tbl_body += "<td><button type=\"button\" class=\"btn btn-warning\">Waiting. Click to play with me :)</button></td>";
			}
		}
		$('#playerTable').append(tbl_body);
	});

	usocket.on('connected', function(user) {
		var tbl_body = "";
		tbl_body += "<tr id='" + user.username + "'><td>" + user.username + "</td>" + "<td>" + user.gamestate + "</td>";
		
		if(user == user.username) {
			tbl_body += "<td><a href=\"/create_game\" class=\"btn btn-info\">Create game.</a></td>";
			tbl_body += "</tr>";
			$('#playerTable').append(tbl_body);
			return;
		}		
		
		if (user.gamestate == 1) {
			tbl_body += "<td></td>";
		} else if (user.gamestate == 2) {
			tbl_body += "<td><button type=\"button\" class=\"btn btn-danger\">I'm playing. Do not disturb :)</button></td>";
		} else {
			tbl_body += "<td><a href='" + user.url + "' class=\"btn btn-warning\">Waiting. Click to play with me :)</a></td>";
		}
		tbl_body += "</tr>";
		$('#playerTable').append(tbl_body);
	});

	usocket.on('left', function(user) {
		$("#" + user.username).remove();
	});

	usocket.emit('join', {
		'username' : username
	});
});
