# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Newsletter.sent_to'
        db.add_column(u'newsletters_newsletter', 'sent_to',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Newsletter.sent_on'
        db.add_column(u'newsletters_newsletter', 'sent_on',
                      self.gf('django.db.models.fields.TimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Newsletter.sent_to'
        db.delete_column(u'newsletters_newsletter', 'sent_to')

        # Deleting field 'Newsletter.sent_on'
        db.delete_column(u'newsletters_newsletter', 'sent_on')


    models = {
        u'newsletters.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent_on': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sent_to': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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