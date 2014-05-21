# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NewsletterSubscription'
        db.create_table(u'newsletters_newslettersubscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subscribers', to=orm['newsletters.NewsletterTarget'])),
            ('hash_field', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
        ))
        db.send_create_signal(u'newsletters', ['NewsletterSubscription'])

        # Adding unique constraint on 'NewsletterSubscription', fields ['email', 'target']
        db.create_unique(u'newsletters_newslettersubscription', ['email', 'target_id'])

        # Adding field 'Newsletter.name'
        db.add_column(u'newsletters_newsletter', 'name',
                      self.gf('django.db.models.fields.CharField')(default='Title', max_length=100),
                      keep_default=False)

        # Adding field 'Newsletter.slug'
        db.add_column(u'newsletters_newsletter', 'slug',
                      self.gf('autoslug.fields.AutoSlugField')(default='title', unique=True, max_length=50, populate_from='name', unique_with=()),
                      keep_default=False)

        # Deleting field 'NewsletterTarget.filter'
        db.delete_column(u'newsletters_newslettertarget', 'filter')

        # Adding field 'NewsletterTarget.slug'
        db.add_column(u'newsletters_newslettertarget', 'slug',
                      self.gf('autoslug.fields.AutoSlugField')(default='Title', unique=True, max_length=50, populate_from='name', unique_with=()),
                      keep_default=False)

        # Adding field 'NewsletterTemplate.slug'
        db.add_column(u'newsletters_newslettertemplate', 'slug',
                      self.gf('autoslug.fields.AutoSlugField')(default='title', unique=True, max_length=50, populate_from='name', unique_with=()),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'NewsletterSubscription', fields ['email', 'target']
        db.delete_unique(u'newsletters_newslettersubscription', ['email', 'target_id'])

        # Deleting model 'NewsletterSubscription'
        db.delete_table(u'newsletters_newslettersubscription')

        # Deleting field 'Newsletter.name'
        db.delete_column(u'newsletters_newsletter', 'name')

        # Deleting field 'Newsletter.slug'
        db.delete_column(u'newsletters_newsletter', 'slug')


        # User chose to not deal with backwards NULL issues for 'NewsletterTarget.filter'
        raise RuntimeError("Cannot reverse this migration. 'NewsletterTarget.filter' and its values cannot be restored.")

        # The following code is provided here to aid in writing a correct migration        # Adding field 'NewsletterTarget.filter'
        db.add_column(u'newsletters_newslettertarget', 'filter',
                      self.gf('django.db.models.fields.CharField')(max_length=500),
                      keep_default=False)

        # Deleting field 'NewsletterTarget.slug'
        db.delete_column(u'newsletters_newslettertarget', 'slug')

        # Deleting field 'NewsletterTemplate.slug'
        db.delete_column(u'newsletters_newslettertemplate', 'slug')


    models = {
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
        }
    }

    complete_apps = ['newsletters']
