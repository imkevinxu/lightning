from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django import forms

from tagging.fields import TagField

import datetime
import os

class Base(models.Model):
    created_at  = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        abstract = True

class UserProfile(Base):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    is_invited          = models.BooleanField(default=False)
    is_photographer     = models.BooleanField()

    fhp_id              = models.IntegerField(blank=True, null=True)
    fhp_username        = models.CharField(max_length=255, blank=True, null=True)
    firstname           = models.CharField(max_length=255, blank=True, null=True)
    lastname            = models.CharField(max_length=255, blank=True, null=True)
    fullname            = models.CharField(max_length=255, blank=True, null=True)
    location            = models.CharField(max_length=255, blank=True, null=True)
    fhp_about           = models.TextField(blank=True, null=True)
    fhp_domain          = models.URLField(blank=True, null=True)
    website             = models.URLField(blank=True, null=True)
    twitter             = models.URLField(blank=True, null=True)
    facebookpage        = models.URLField(blank=True, null=True)
    flickr              = models.URLField(blank=True, null=True)
    facebook            = models.URLField(blank=True, null=True)
    fhp_affection       = models.IntegerField(blank=True, null=True)
    fhp_photos_count    = models.IntegerField(blank=True, null=True)
    profilepic          = models.URLField(blank=True, null=True)

    phone = models.CharField(max_length=20,blank=True, null=True)

    def __unicode__(self):
        if self.fullname is not None:
            return self.fullname
        else:
            return ''

    @staticmethod
    def createUser(user, username, email=None, password=None, tag=None):
        try:
            baseUser = User.objects.create_user(username=username, email=email, password=password)
        except:
            baseUser = User.objects.get(username=username)

        photographer = UserProfile.objects.get_or_create(user=baseUser)[0]

        photographer.is_photographer = True
        
        photographer.fhp_id                 = user['id']
        photographer.fhp_username           = user['username']
        photographer.firstname              = user['firstname']
        photographer.lastname               = user['lastname']
        photographer.fullname               = user['fullname']
        
        # sets location like "San Francisco, CA, United States"
        location                            = filter(None, [user["city"], user["state"], user["country"]])
        location                            = ", ".join(location)
        photographer.location               = location
        
        photographer.profilepic             = user['userpic_url']
        if "http://" not in user['userpic_url']:
            photographer.profilepic         = 'http://500px.com%s' % user['userpic_url']

        photographer.fhp_about              = user['about']
        photographer.fhp_domain             = user['domain']
        photographer.fhp_affection          = user['affection']
        photographer.fhp_photos_count       = user['photos_count']

        if 'website' in user['contacts']:
            photographer.website            = user['contacts']['website']
        if 'twitter' in user['contacts']:
            photographer.twitter            = user['contacts']['twitter']
        if 'facebookpage' in user['contacts']:
            photographer.facebookpage       = user['contacts']['facebookpage']
        if 'flickr' in user['contacts']:
            photographer.flickr             = user['contacts']['flickr']
        if 'facebook' in user['contacts']:
            photographer.facebook           = user['contacts']['facebook']

        # add tag to photographer
        if tag is not None:
            tag_tuple = Tag.objects.get_or_create(tagname=tag)
            
            tagged_users = tag_tuple[0].user.all()

            if photographer not in tagged_users:
                tag_tuple[0].user.add(photographer)

            tag_tuple[0].save()

        photographer.save()

        return photographer

    # sets user.tags to be a list of tag names
    def getTags(self):
        # tags = []

        # for tag in Tag.objects.all():
        #     for u in tag.user.all():
        #         if u.id == self.id:
        #             tags.append(tag.tagname)
        
        self.tags = []

        tags = self.tag_set.all()
        for tag in tags:
            self.tags.append(tag.tagname)

        return self

class Photo(models.Model):
    user = models.ForeignKey(UserProfile)

    photo_id            = models.IntegerField()
    name                = models.CharField(max_length=255)

    description         = models.TextField(blank=True, null=True)
    times_viewed        = models.IntegerField(blank=True, null=True)
    rating              = models.FloatField(blank=True, null=True)
    created_at          = models.DateTimeField(blank=True, null=True)
    width               = models.IntegerField(blank=True, null=True)
    height              = models.IntegerField(blank=True, null=True)
    votes_count         = models.IntegerField(blank=True, null=True)
    favorites_count     = models.IntegerField(blank=True, null=True)
    comments_count      = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return "%s ID:%d User: %s" % (self.name, self.photo_id, self.user.id)

    @staticmethod
    def createPhoto(user, info):
        photo_id = info['id']
        name = info['name']

        pic = Photo.objects.create(photo_id=photo_id, user=user, name=name)

        pic.description         = info['description']
        pic.times_viewed        = info['times_viewed']
        pic.rating              = info['rating']
        pic.created_at          = info['created_at']
        pic.width               = info['width']
        pic.height              = info['height']
        pic.votes_count         = info['votes_count']
        pic.favorites_count     = info['favorites_count']
        pic.comments_count      = info['comments_count']

        pic.save()

        return pic

    # SIDE EFFECT: assign image_url to this photo
    def getImage(self, size):
        image = self.image_set.filter(image_size=size)
        if len(image) > 0:
            self.image_url = image[0].image_url
        return self

IMAGE_SIZES = (
    ('70x70', '70x70'),
    ('140x140', '140x140'),
    ('280x280', '280x280'),
    ('full', 'full'),
)

class Image(models.Model):
    photo = models.ForeignKey(Photo)

    image_url           = models.URLField()
    image_size          = models.CharField(choices=IMAGE_SIZES, max_length=10, null=True)

    def __unicode__(self):
        return "%s %s" % (self.photo.id, self.image_size)

    @staticmethod
    def createForPhoto(photo, urls):
        for url, size in zip(urls, IMAGE_SIZES):
            img = Image.objects.create(photo=photo, image_url=url, image_size=size[0])
            img.save()

class Tag(models.Model):
    tagname = models.CharField(max_length=255)
    user = models.ManyToManyField(UserProfile, blank=True, null=True)
    
    def __unicode__(self):
        return self.tagname

    # list of all tag names
    @staticmethod
    def getAllNames():
        tags = []

        for tag in Tag.objects.all():
            tags.append(tag.tagname)

        # TODO: consider other sorting, other than alphabetical?
        tags.sort()

        return tags

