$(function() {
	$('#photos').on('click', '.photo', function() {

		var $el = $(this);

		if ($el.hasClass('active')) {

			$el.removeClass('active');

			$el.children('.glyph').text('g');

		} else {

			$el.addClass('active');

			$el.children('.glyph').text('f');

		}

	});

	$('#photos-form').submit(function() {

		var $form = $(this),
			$active = $('#photos .active'),
			photoId;

		$.each($active, function(index) {

			photoId = $(this).attr('data-photo-id');

			if (photoId) {
				$('<input type="hidden" name="photo" />')
					.val(photoId)
					.appendTo($form);
			}

		});

		console.log($form.serialize());

	});

});