# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Service.description'
        db.add_column(u'bagni_service', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=2000, blank=True),
                      keep_default=False)

        # Adding field 'Service.description_en'
        db.add_column(u'bagni_service', 'description_en',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Service.description_it'
        db.add_column(u'bagni_service', 'description_it',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Municipality.description_en'
        db.add_column(u'bagni_municipality', 'description_en',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Municipality.description_it'
        db.add_column(u'bagni_municipality', 'description_it',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Language.description_en'
        db.add_column(u'bagni_language', 'description_en',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Language.description_it'
        db.add_column(u'bagni_language', 'description_it',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'ServiceCategory.name_en'
        db.add_column(u'bagni_servicecategory', 'name_en',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'ServiceCategory.name_it'
        db.add_column(u'bagni_servicecategory', 'name_it',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'ServiceCategory.description_en'
        db.add_column(u'bagni_servicecategory', 'description_en',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'ServiceCategory.description_it'
        db.add_column(u'bagni_servicecategory', 'description_it',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'ServiceCategory.slug_en'
        db.add_column(u'bagni_servicecategory', 'slug_en',
                      self.gf('autoslug.fields.AutoSlugField')(max_length=50, unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'ServiceCategory.slug_it'
        db.add_column(u'bagni_servicecategory', 'slug_it',
                      self.gf('autoslug.fields.AutoSlugField')(max_length=50, unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'District.description_en'
        db.add_column(u'bagni_district', 'description_en',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'District.description_it'
        db.add_column(u'bagni_district', 'description_it',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Image.description'
        db.add_column(u'bagni_image', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=2000, blank=True),
                      keep_default=False)

        # Adding field 'Image.description_en'
        db.add_column(u'bagni_image', 'description_en',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Image.description_it'
        db.add_column(u'bagni_image', 'description_it',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Service.description'
        db.delete_column(u'bagni_service', 'description')

        # Deleting field 'Service.description_en'
        db.delete_column(u'bagni_service', 'description_en')

        # Deleting field 'Service.description_it'
        db.delete_column(u'bagni_service', 'description_it')

        # Deleting field 'Municipality.description_en'
        db.delete_column(u'bagni_municipality', 'description_en')

        # Deleting field 'Municipality.description_it'
        db.delete_column(u'bagni_municipality', 'description_it')

        # Deleting field 'Language.description_en'
        db.delete_column(u'bagni_language', 'description_en')

        # Deleting field 'Language.description_it'
        db.delete_column(u'bagni_language', 'description_it')

        # Deleting field 'ServiceCategory.name_en'
        db.delete_column(u'bagni_servicecategory', 'name_en')

        # Deleting field 'ServiceCategory.name_it'
        db.delete_column(u'bagni_servicecategory', 'name_it')

        # Deleting field 'ServiceCategory.description_en'
        db.delete_column(u'bagni_servicecategory', 'description_en')

        # Deleting field 'ServiceCategory.description_it'
        db.delete_column(u'bagni_servicecategory', 'description_it')

        # Deleting field 'ServiceCategory.slug_en'
        db.delete_column(u'bagni_servicecategory', 'slug_en')

        # Deleting field 'ServiceCategory.slug_it'
        db.delete_column(u'bagni_servicecategory', 'slug_it')

        # Deleting field 'District.description_en'
        db.delete_column(u'bagni_district', 'description_en')

        # Deleting field 'District.description_it'
        db.delete_column(u'bagni_district', 'description_it')

        # Deleting field 'Image.description'
        db.delete_column(u'bagni_image', 'description')

        # Deleting field 'Image.description_en'
        db.delete_column(u'bagni_image', 'description_en')

        # Deleting field 'Image.description_it'
        db.delete_column(u'bagni_image', 'description_it')


    models = {
        u'bagni.bagno': {
            'Meta': {'object_name': 'Bagno'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address_it': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '125', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'description_en': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'description_it': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '125', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bagni.Language']", 'symmetrical': 'False', 'blank': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'blank': 'True'}),
            'municipality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bagni.Municipality']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bagni.Service']", 'symmetrical': 'False', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '75', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'slug_en': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_it': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '125', 'blank': 'True'}),
            'winter_tel': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'})
        },
        u'bagni.district': {
            'Meta': {'object_name': 'District'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'description_it': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'slug_en': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_it': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'bagni.image': {
            'Meta': {'object_name': 'Image'},
            'bagno': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bagni.Bagno']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'description_it': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'slug_en': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_it': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'bagni.language': {
            'Meta': {'object_name': 'Language'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'description_en': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'description_it': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'slug_en': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_it': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'bagni.municipality': {
            'Meta': {'object_name': 'Municipality'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'description_it': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bagni.District']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'slug_en': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_it': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'bagni.service': {
            'Meta': {'object_name': 'Service'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bagni.ServiceCategory']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'description_it': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'free': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'slug_en': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_it': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'bagni.servicecategory': {
            'Meta': {'object_name': 'ServiceCategory'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'description_en': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'description_it': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'slug_en': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_it': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['bagni']