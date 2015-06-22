# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import six
try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    # Support django < 1.8
    from django.db.models import get_model

def _get_content_type_and_obj(obj, model=None):
    if isinstance(model, six.string_types):
        model = get_model(*model.split("."))

    if isinstance(obj, six.integer_types):
        obj = model.objects.get(pk=obj)

    return ContentType.objects.get_for_model(type(obj)), obj


class FavoriteManager(models.Manager):
    """
    A Manager for Favorite objects
    """

    def for_user(self, user, model=None):
        """
        Returns a Favorite objects queryset for a given user.

        If a model params is provided, it returns only the
        favorited objects of that model class

        Usage:

            Favorite.objects.for_user(user)
            Favorite.objects.for_user(user, model=Song)
            Favorite.objects.for_user(user, model="music.song")
        """

        qs = self.get_queryset().filter(user=user)

        if model:
            if isinstance(model, six.string_types):
                model = get_model(*model.split("."))

            content_type = ContentType.objects.get_for_model(model)
            qs = qs.filter(target_content_type=content_type)

        return qs.order_by("-timestamp")

    def for_model(self, model):
        """
        Returns a Favorite objects queryset for a given model.
        `model` may be a django model class or an string representing
        a model in module-notation, ie: "auth.User"

        Usage:

            Favorite.objects.for_model(Song)
            Favorite.objects.for_model("music.Song")
        """

        # if model is an app_label.model string make it a Model class
        if isinstance(model, six.string_types):
            model = get_model(*model.split("."))

        content_type = ContentType.objects.get_for_model(model)

        qs = self.get_queryset().filter(
            target_content_type=content_type
        )

        return qs.order_by("-timestamp")

    def for_object(self, obj, model=None):
        """
        Returns a Favorite objects queryset for a given object

        Usage:
            Favorite.objects.for_object(1, "music.Song")
            Favorite.objects.for_object(1, Song)

        or given a music app with a Song model:

            song = Song.objects.get(pk=1)
            Favorite.objects.for_object(song)
        """

        content_type, obj = _get_content_type_and_obj(obj, model)

        qs = self.get_queryset().filter(
            target_content_type=content_type,
            target_object_id=obj.pk
        )

        return qs.order_by("-timestamp")

    def get_favorite(self, user, obj, model=None):
        """
        Returns a Favorite instance if the `user` has favorited
        the given object `obj`. Otherwise returns None

        Usage:
            Favorite.objects.get_favorite(user, 1, "music.Song")
            Favorite.objects.get_favorite(user, 1, Song)

        or given a music app with a Song model:

            song = Song.objects.get(pk=1)
            Favorite.objects.get_favorite(user, song)
        """

        content_type, obj = _get_content_type_and_obj(obj, model)

        try:
            return self.get_queryset().get(
                user=user,
                target_content_type=content_type,
                target_object_id=obj.id
            )
        except self.model.DoesNotExist:
            return None

    def create(self, user, obj, model=None):
        """
        Creates and returns a new Favorite obj for the given user and obj
        """

        content_type, content_object = _get_content_type_and_obj(obj, model)
        fav = super(FavoriteManager, self).create(
            user=user,
            target_content_type=content_type,
            target_object_id=content_object.pk,
            target=content_object
        )

        return fav
