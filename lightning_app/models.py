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