from django.core.management.base import BaseCommand, CommandError

from lightning_app.models import *
from lightning_app.fivehundred import *

from django.conf import settings


class Command(BaseCommand):
    help = 'Imports Images to Photos without any'

    def handle(self, *args, **options):
        CONSUMER_KEY = getattr(settings, "FIVEHUNDRED_CONSUMER_KEY", None)
        api = FiveHundredPx(CONSUMER_KEY)

        photos = Photo.objects.all().select_related()

        for photo in photos:
            images = photo.image_set.all()

            # no images, need to populate
            if len(images) == 0:
                try:
                    data = api.get_photo(photo.photo_id, {
                        "image_size[]": [1, 2, 3, 4]
                    })

                    urls = data['photo']['image_url']

                    print urls

                    Image.createForPhoto(photo, urls)

                except Exception, e:
                    print
                    print 'ERROR %s' % e
