from django.db import models
from django_userforeignkey.models.fields import UserForeignKey
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Author(models.Model):
    f_name = models.CharField(max_length=150)
    l_name = models.CharField(max_length=150)

    def __str__(self):
        return "%s %s" % (self.f_name, self.l_name)

    def __unicode__(self):
        return u'%s %s' % (self.f_name, self.l_name)


class Book(models.Model):
    name = models.CharField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published = models.DateField()
    created_by = UserForeignKey(auto_user_add=True, related_name='book_created_by')
    updated_by = UserForeignKey(auto_user_add=True, related_name='book_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ('name', 'author')

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return u'%s' % self.name


class Rack(models.Model):
    name = models.CharField(max_length=150, unique=True)
    max_size = models.IntegerField()
    uid = models.CharField(max_length=50, unique=True)
    created_by = UserForeignKey(auto_user_add=True, null=True, related_name='rack_created_by')
    updated_by = UserForeignKey(auto_user_add=True, related_name='rack_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return u'%s' % self.name


class Rack_books(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    created_by = UserForeignKey(auto_user_add=True, null=True, related_name='rack_books_created_by')
    updated_by = UserForeignKey(auto_user_add=True, related_name='rack_books_updated_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "%s" % self.rack.name

    def __unicode__(self):
        return u'%s' % self.rack.name

    def clean(self):
        if Rack_books.objects.filter(rack=self.rack.id).count() > 9:
            raise ValidationError("Limit of this rack has been reached")


# @receiver(pre_save, sender=Rack_books)
# def check_limits(sender, **kwargs):
#     if sender.objects.filter(rack=kwargs['instance'].rack.id).count() > kwargs['instance'].rack.max_size:
#         raise ValidationError("Limit of this rack has been reached")
