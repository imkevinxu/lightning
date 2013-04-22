from django.core.management.base import BaseCommand, CommandError

from lightning_app.models import *
from lightning_app.fivehundred import *

from django.conf import settings


class Command(BaseCommand):
    help = 'Grabs users with popular photos and add them to the DB'

    def handle(self, *args, **options):
        CONSUMER_KEY = getattr(settings, "FIVEHUNDRED_CONSUMER_KEY", None)
        api = FiveHundredPx(CONSUMER_KEY)

        tags = ['Wedding', 'People', 'Commercial', 'Performing Arts', 'Sport', 'Journalism']

        for tag in tags:
            args = {
                "feature": "popular",
                "only": tag,
                "exclude": "Nude",
                "rpp": 20, # results per page
                "image_size[]": [1, 2, 3, 4]
            }
            popular = api.request('/photos', args)['photos']

            for p in popular:
                username = p['user']['username']
                print "GOT %s" % username

                try:
                    user = api.get_user(username=username)['user']
                    UserProfile.createUser(user, username, tag=tag)

                    photos = api.get_user_photos(user['id'], limit=10)

                    user = User.objects.get(username=username).get_profile()
                    
                    print "SAVING"

                    for pics in photos:
                        photo = Photo.createPhoto(user, pics)
                        Image.createForPhoto(photo, pics['image_url'])

                except Exception, e:
                    print
                    print 'ERROR %s' % e
