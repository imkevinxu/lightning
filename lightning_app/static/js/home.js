$(function() {

	$.fn.digits = function(){ 
	    return this.each(function(){ 
	        $(this).text( $(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") ); 
	    })
	}

	$('#find-photographer').click(function() {
		$.get('/users/'+$('#tags').val(), function(data) {
			$('#gallery').empty();

			count = 51;
			if (data.length < count) count = data.length;

			for (var i=0, j=count; i<j; i++) {
				console.log(data[i].username);

				var item = data[i];
				var affection = String(item.fhp_affection).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
				var elem = $('<a></a>').attr("href", "/"+item.username)
					    .append($('<div></div>').addClass("photo-thumb")
					    	.append($('<div></div>').addClass("name").html(item.fullname)
					    		.append($('<span></span>').addClass("right").css("padding-right", "10px").css("margin-top", "-4px")
					    			.append($('<span></span>').addClass("glyph general").css("font-size", "14px").css("color", "#D41616").html("b").after(affection))))
					    	.append($('<img></img>').attr("src", item.pics[0].image_url))
					   	);

				$('#gallery').prepend(elem).delay(100);
			}
		});

		return false;
	});
});