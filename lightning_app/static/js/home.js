$(function() {

	var photo_thumb = $('#photo-thumb-template').html(),
		template = Handlebars.compile(photo_thumb);

	console.log(photo_thumb);

	$('#find-photographer').click(function() {
		$.get('/users', function(data) {
			$('#gallery').empty();

			for (var i=0, j=data.length; i<j; i++) {
				console.log(data[i]);

				var item = data[i];

				var output = template({
					'username': item.username,
					'fullname': item.fullname,
					'image_url': item.pics[0].image_url
				});

				$('#gallery').append(output);
			}
		});

		return false;
	});
});