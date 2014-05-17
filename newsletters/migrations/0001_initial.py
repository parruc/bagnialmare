# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NewsletterTarget'
        db.create_table(u'newsletters_newslettertarget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('filter', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'newsletters', ['NewsletterTarget'])

        # Adding model 'NewsletterTemplate'
        db.create_table(u'newsletters_newslettertemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'newsletters', ['NewsletterTemplate'])

        # Adding model 'Newsletter'
        db.create_table(u'newsletters_newsletter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('ckeditor.fields.RichTextField')(max_length=2000)),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='newsletters', to=orm['newsletters.NewsletterTarget'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='newsletters', to=orm['newsletters.NewsletterTemplate'])),
        ))
        db.send_create_signal(u'newsletters', ['Newsletter'])


    def backwards(self, orm):
        # Deleting model 'NewsletterTarget'
        db.delete_table(u'newsletters_newslettertarget')

        # Deleting model 'NewsletterTemplate'
        db.delete_table(u'newsletters_newslettertemplate')

        # Deleting model 'Newsletter'
        db.delete_table(u'newsletters_newsletter')


    models = {
        u'newsletters.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'newsletters'", 'to': u"orm['newsletters.NewsletterTarget']"}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'newsletters'", 'to': u"orm['newsletters.NewsletterTemplate']"}),
            'text': ('ckeditor.fields.RichTextField', [], {'max_length': '2000'})
        },
        u'newsletters.newslettertarget': {
            'Meta': {'object_name': 'NewsletterTarget'},
            'filter': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'newsletters.newslettertemplate': {
            'Meta': {'object_name': 'NewsletterTemplate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['newsletters']