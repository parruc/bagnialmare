# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'NewsletterUser.name'
        db.delete_column(u'newsletters_newsletteruser', 'name')

        # Deleting field 'NewsletterUser.slug'
        db.delete_column(u'newsletters_newsletteruser', 'slug')


        # Changing field 'NewsletterUser.user'
        db.alter_column(u'newsletters_newsletteruser', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(default=None, unique=True, to=orm['auth.User']))

        # Changing field 'NewsletterUser.old_email'
        db.alter_column(u'newsletters_newsletteruser', 'old_email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'NewsletterUser.name'
        raise RuntimeError("Cannot reverse this migration. 'NewsletterUser.name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'NewsletterUser.name'
        db.add_column(u'newsletters_newsletteruser', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=100),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'NewsletterUser.slug'
        raise RuntimeError("Cannot reverse this migration. 'NewsletterUser.slug' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'NewsletterUser.slug'
        db.add_column(u'newsletters_newsletteruser', 'slug',
                      self.gf('autoslug.fields.AutoSlugField')(max_length=50, unique_with=(), unique=True, populate_from='name'),
                      keep_default=False)


        # Changing field 'NewsletterUser.user'
        db.alter_column(u'newsletters_newsletteruser', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['auth.User']))

        # Changing field 'NewsletterUser.old_email'
        db.alter_column(u'newsletters_newsletteruser', 'old_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'newsletters.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sent_on': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sent_to': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'newsletters'", 'to': u"orm['newsletters.NewsletterTarget']"}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'newsletters'", 'to': u"orm['newsletters.NewsletterTemplate']"}),
            'text': ('ckeditor.fields.RichTextField', [], {'max_length': '2000'})
        },
        u'newsletters.newslettersubscription': {
            'Meta': {'unique_together': "(('email', 'target'),)", 'object_name': 'NewsletterSubscription'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'hash_field': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscribers'", 'to': u"orm['newsletters.NewsletterTarget']"})
        },
        u'newsletters.newslettertarget': {
            'Meta': {'object_name': 'NewsletterTarget'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'})
        },
        u'newsletters.newslettertemplate': {
            'Meta': {'object_name': 'NewsletterTemplate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'})
        },
        u'newsletters.newsletteruser': {
            'Meta': {'object_name': 'NewsletterUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'newsletter_user'", 'unique': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['newsletters']