$(function() {

	$('#tags').on("change", function() {
		var search_tag = $('#tags').val();
		$('#gallery').css("opacity", 0.5);

		$.get('/users/'+search_tag, function(data) {
			var results = $('<div></div>');
			var count = 51;
			if (data.length < count) count = data.length;

			for (var i=0, j=count; i<j; i++) {
				// console.log(data[i].username);

				var item = data[i];
				var affection = String(item.fhp_affection).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
				var elem = $('<a></a>').attr("href", "/"+item.username)
					    .append($('<div></div>').addClass("photo-thumb")
					    	.append($('<div></div>').addClass("name").html(item.fullname)
					    		.append($('<span></span>').addClass("right").css("padding-right", "10px").css("margin-top", "-4px")
					    			.append($('<span></span>').addClass("glyph general").css("font-size", "14px").css("color", "#D41616").html("b").after(affection))))
					    	.append($('<img></img>').attr("src", item.pics[0].image_url))
					   	);

				results.append(elem);
			}

			$('#newest_photog').remove();
			$('#featured_photog').empty();

			$('#featured_photog').append('<h2>Search for "'+search_tag+'"</h2>');
			$('#featured_photog').append(results);
			console.log(results);
			$('#gallery').css("opacity", 1);
		});

		return false;
	});
});