from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.template import loader, RequestContext, Context
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from twilio.rest import TwilioRestClient
import sys, os, urllib

from lightning_app.models import *
from lightning_app.model_forms import *
from lightning_app.forms import *
from lightning_app.fivehundred import *

CONSUMER_KEY = getattr(settings, "FIVEHUNDRED_CONSUMER_KEY", None)
api = FiveHundredPx(CONSUMER_KEY)

account = getattr(settings, "TWILIO_ACCOUNT", None)
token = getattr(settings, "TWILIO_TOKEN", None)
twilio = TwilioRestClient(account, token)

from datetime import datetime
from pytz import timezone
pacific = timezone('US/Pacific')
startdate = datetime.strptime('July 17 2012 1:00PM', '%B %d %Y %I:%M%p')
startdate = pacific.localize(startdate)

def login_redirect(request):
    return redirect('/%s' % request.user.username)

def index(request):
    users = User.objects.filter(userprofile__is_invited=True).select_related()

    # returns UserProfile object with their photos as properties
    def getUserPics(u):
        try:
            username = u.username
            user = u.get_profile()
            user.username = username
            
            photos = user.photo_set.all()

            # for each photo, assign it a display url from its image set
            map(lambda p: p.getImage('280x280'), photos)

            user.pics = photos

            user.getTags()

            return user
        except ObjectDoesNotExist:
            pass

    def isBadUser(u):
        if u is None:
            return False

        if len(u.pics) == 0:
            return False

        return True

    import random
    users = map(getUserPics, users)
    users = filter(isBadUser, users)

    def isRecentUser(u):
        if u.created_at > startdate:
            return True
        return False

    # grab most recent users
    recentUsers = filter(isRecentUser, users)
    recentUsers.reverse()
    recentUsers = list(recentUsers[:9])

    tags = Tag.getAllNames()

    return render(request, "index.html", locals())

def users(request, category, location=None):

    users = User.objects.filter(userprofile__is_invited=True).select_related()

    if category != "anything":
        users = users.filter(userprofile__tag__tagname=category)

    # returns UserProfile object with their photos as properties
    def getUserJson(u):
        try:
            username = u.username

            profile = u.get_profile()
            photos = profile.photo_set.all()[:1]

            user = {
                "id": profile.id,
                "username": username,
                "fullname": profile.fullname,
                "location": profile.location,
                "fhp_domain": profile.fhp_domain,
                "website": profile.website,
                "twitter": profile.twitter,
                "facebookpage": profile.facebookpage,
                "flickr": profile.flickr,
                "facebook": profile.facebook,
                "fhp_affection": profile.fhp_affection,
                "pics": []
            }

            # populate image_url property
            map(lambda p: p.getImage('280x280'), photos)

            for photo in photos:
                data = {
                    "id": photo.id,
                    "photo_id": photo.photo_id,
                    "name": photo.name,
                    "image_url": photo.image_url
                }

                user['pics'].append(data)

            return user
        except ObjectDoesNotExist:
            pass

    def isDeadUser(u):
        if u is None:
            return False

        if len(u['pics']) == 0:
            return False

        return True

    users = map(getUserJson, users)
    users = filter(isDeadUser, users)
    users = list(users)
    import random
    random.shuffle(users)

    data = simplejson.dumps(users)
    
    return HttpResponse(data, mimetype='application/json')

# Step 1 to register photographer
# Saves all their information, photos, and logs them in
def register(request):
    if request.user.is_authenticated():
        logout(request)

    if request.method == "POST":
        if all (key in request.POST for key in ("username", "password", "account")):
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            account = request.POST["account"]

            def validateEmail(email):
                from django.core.validators import validate_email
                from django.core.exceptions import ValidationError
                try:
                    validate_email(email)
                    return True
                except ValidationError:
                    return False

            try:
                # pull user by email address if it's valid, username otherwise
                if validateEmail(account):
                    user = api.get_user(email=account)['user']
                else:
                    user = api.get_user(username=account)['user']

                # determine if username/password already belongs to an account
                print user

                photographer = UserProfile.createUser(user, username, email=email, password=password)

                auth_user = authenticate(username=username, password=password)
                
                photos = api.get_user_photos(user['id'])
                
                for pics in photos:
                    photo = Photo.createPhoto(photographer, pics)
                    Image.createForPhoto(photo, pics['image_url'])

                if auth_user is not None:
                    if auth_user.is_active:
                        login(request, auth_user)

                        return redirect('account')
            
            except Exception, e:
                print 'ERROR with the user %s' % account
                print e

    return render(request, "register.html", locals())

def photos(request):
    if not request.user.is_authenticated() or request.user.is_superuser:
        return redirect('register')

    photographer = User.objects.get(username=request.user.username).get_profile()

    if request.method == 'POST':
        
        chosen = request.POST.getlist('photo')

        for photoId in chosen:

            try:
                photoId = int(photoId)
            except ValueError:
                continue

            try:
                photo = Photo.objects.get(id=photoId)
            except ObjectDoesNotExist:
                continue

            if photographer != photo.user:
                continue

            photo.is_chosen = True
            photo.save()

    photos = Photo.objects.filter(user=photographer)
    
    # for each photo, assign it a display url from its image set
    for photo in photos:
        photo.getImage('280x280')

    return render(request, "photos.html", locals())


# Step 2 to register photographer
# Creates user with 500px username, email, and bcrypted password
# and stores additional data about full name, location, etc. from the URL
# https://github.com/500px/api-documentation/blob/master/endpoints/user/GET_users_show.md

def account(request):
    if request.user.is_authenticated() and not request.user.is_superuser:
        photographer = User.objects.get(username=request.user.username).get_profile()

        photographer.getTags()

    else:
        return redirect('register')

    tags = Tag.getAllNames()

    if request.method == "POST":
        form = AccountForm(request.POST)

        if form.is_valid():
            photographer.location = form.cleaned_data['location']
            photographer.website = form.cleaned_data['website']
            photographer.fhp_about = form.cleaned_data['about']
            photographer.phone = form.cleaned_data['phone']

            # compute which tags were removed because it's not set for us
            current = set(request.POST.getlist('tags'))
            removed = [x for x in tags if x not in current]

            # add all tags that user checked
            if current is not None:
                for tag in current:
                    tag_tuple = Tag.objects.get_or_create(tagname=tag)
                    print "adding %s" % tag_tuple[0]
                    tagged_users = tag_tuple[0].user.all()
                    if photographer not in tagged_users:
                        tag_tuple[0].user.add(photographer)
                    tag_tuple[0].save()

            # remove tags that were unchecked
            for tag in removed:
                tag = Tag.objects.get(tagname=tag)
                print "removing %s" % tag
                tag.user.remove(photographer)
                tag.save()

            photographer.save()

            return redirect('show', request.user.username)

    else:
        form = AccountForm()


    photographer.getTags()

    return render(request, "account.html", locals())

# Step 3 to register photographer
# Saves the rest of the information needed
# Redirects to user's profile page
def reg3(request):
    if request.user.is_authenticated():
        photographer = User.objects.get(username=request.user.username).get_profile()

    return redirect('/%s' % request.user.username)

def show(request, username):

    user = get_object_or_404(User, username=username).get_profile()

    if request.method == 'POST':

        if user.user.email:

            name = request.POST['name']
            email = request.POST['email']

            tags = request.POST.getlist('tags')

            day = request.POST['date']
            date = datetime.strptime(day, '%Y-%m-%d')
            date = pacific.localize(date)

            message = request.POST['message']

            context = Context({
                'name': name,
                'tags': tags,
                'date': date,
                'message': message
            })

            emailTemplate = loader.get_template('email/message.txt')

            subject = "New message on Lightning"
            body = emailTemplate.render(context)

            send_mail(subject, body, settings.SENDGRID_FROM, [user.user.email])

            # send SMS notification if we have their number
            if user.phone:
                numTo = user.phone
                body = "%s, you have a new message on Lightning from %s" % (username, name)
                twilio.sms.messages.create(to=numTo, from_=settings.TWILIO_FROM, body=body)

    isSelf = request.user.is_authenticated() and request.user.username == username

    user.getTags()

    photos = Photo.objects.filter(user=user).filter(is_chosen=True)
    
    # for each photo, assign it a display url from its image set
    for photo in photos:
        photo.getImage('full')

    return render(request, "photog.html", locals())




