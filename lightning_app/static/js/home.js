$(function() {

	var photo_thumb = $('#photo-thumb-template').html(),
		template = Handlebars.compile(photo_thumb);

	$('#find-photographer').click(function() {
		alert('clicked');
		$.get('/users', function(data) {
			$('#gallery').empty();

			for (var i=0, j=data.length; i<j; i++) {
				console.log(data[i]);

				var output = template({
					username: data.username,
					fullname: data.fullname,
					image_url: data.pics[0].image_url
				});

				$('#gallery').append(output);
			}
		});

		return false;
	});
});