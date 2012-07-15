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

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    is_photographer = models.BooleanField()
    fhp_id = models.IntegerField(blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    fhp_about = models.CharField(max_length=255, blank=True, null=True)
    fhp_domain = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebookpage = models.URLField(blank=True, null=True)
    flickr = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    fhp_affection = models.IntegerField(blank=True, null=True)
    fhp_photos_count = models.IntegerField(blank=True, null=True)
    profilepic = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20,blank=True, null=True)

    @staticmethod
    def createUser(user, email=None, password=None):
        username = user['username']

        baseUser = User.objects.create_user(username, email, password)
        photographer = UserProfile.objects.create(user=baseUser)
        photographer.is_photographer = True
        photographer.fhp_id = user['id']
        photographer.firstname = user['firstname']
        photographer.lastname = user['lastname']
        photographer.fullname = user['fullname']
        location = filter(None, [user["city"], user["state"], user["country"]])
        location = ", ".join(location)
        photographer.location = location
        photographer.fhp_about = user['about']
        photographer.fhp_domain = user['domain']
        if 'website' in user['contacts']:
            photographer.website = user['contacts']['website']
        if 'twitter' in user['contacts']:
            photographer.twitter = user['contacts']['twitter']
        if 'facebookpage' in user['contacts']:
            photographer.facebookpage = user['contacts']['facebookpage']
        if 'flickr' in user['contacts']:
            photographer.flickr = user['contacts']['flickr']
        if 'facebook' in user['contacts']:
            photographer.facebook = user['contacts']['facebook']
        photographer.fhp_affection = user['affection']
        photographer.fhp_photos_count = user['photos_count']
        photographer.profilepic = user['userpic_url']
        if "http://" not in user['userpic_url']:
            photographer.profilepic = 'http://500px.com%s' % user['userpic_url']
        photographer.save()
        return photographer

class Photo(models.Model):
    user = models.ForeignKey(UserProfile)

    photo_id = models.IntegerField()
    name = models.CharField(max_length=255)
    image_url = models.URLField()

    description = models.TextField(blank=True, null=True)
    times_viewed = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    votes_count = models.IntegerField(blank=True, null=True)
    favorites_count = models.IntegerField(blank=True, null=True)
    comments_count = models.IntegerField(blank=True, null=True)

    @staticmethod
    def createPhoto(user, info):
        photo_id = info['id']
        name = info['name']
        image_url = info['image_url']

        pic = Photo.objects.create(photo_id=photo_id, user=user, name=name, image_url=image_url)

        pic.description = info['description']
        pic.times_viewed = info['times_viewed']
        pic.rating = info['rating']
        pic.created_at = info['created_at']
        pic.width = info['width']
        pic.height = info['height']
        pic.votes_count = info['votes_count']
        pic.favorites_count = info['favorites_count']
        pic.comments_count = info['comments_count']

        pic.save()

class Tag(models.Model):
    tagname = models.CharField(max_length=255)
    user = models.ManyToManyField(UserProfile, blank=True, null=True)
    
