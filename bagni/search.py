# -*- coding: utf-8 -*-
import os
import shutil
import operator
import re
from collections import OrderedDict
from django.db.models import signals
from django.conf import settings
from django.utils.translation import get_language, activate, deactivate

from whoosh import fields, index, qparser, sorting, query, analysis

from .models import Bagno, Service, Language

WHOOSH_SCHEMA = fields.Schema(id=fields.ID(stored=True, unique=True),
                              text=fields.TEXT(analyzer=analysis.StandardAnalyzer(minsize=1)),
                              services=fields.IDLIST(stored=True, expression=re.compile(r"[^#]+"),),
                              languages=fields.IDLIST(stored=True, expression=re.compile(r"[^#]+"),),
                              )

LANGS = [l[0] for l in settings.LANGUAGES]

def index_path(lang):
    return os.path.join(settings.WHOOSH_INDEX, lang)

def create_index(sender=None, langs=LANGS, **kwargs):
    """ Creates the index schema (no data at this point)
    """
    for lang in langs:
        if not os.path.exists(index_path(lang)):
            os.mkdir(index_path(lang))
            index.create_in(index_path(lang), schema=WHOOSH_SCHEMA)


def delete_index(sender=None, langs=LANGS, **kwargs):
    """ Deletes the index schema and eventually the contained data
    """
    for lang in langs:
        if os.path.exists(index_path(lang)):
            shutil.rmtree(index_path(lang))


def recreate_index(sender=None, langs=LANGS, **kwargs):
    """ Deletes the index schema and eventually the contained data
        and rebuilds the index schema (no data at this point)
    """
    delete_index(sender=sender, langs=langs, **kwargs)
    create_index(sender=sender, langs=langs, **kwargs)


def update_index(sender, langs=LANGS, **kwargs):
    """ Adds/updates an entry in the index. It's connected with
        the post_save signal of the Object objects so will automatically
        index every new or modified Object
    """
    old_language = get_language()
    for lang in langs:
        ix = index.open_dir(index_path(lang))
        activate(lang)
        writer = ix.writer()
        obj = kwargs['instance']
        if "created" in kwargs and kwargs['created']:
                writer.add_document(**obj.index_features())
        else:
            writer.update_document(**obj.index_features())
        writer.commit()
    activate(old_language)

signals.post_save.connect(update_index, sender=Bagno)
signals.m2m_changed.connect(update_index, sender=Bagno.services.through)


def recreate_data(sender=None, langs=LANGS, **kwargs):
    """ Readds all the Object in the index. If they already exists
        will be duplicated
    """
    for lang in langs:
        ix = index.open_dir(index_path(lang))
        writer = ix.writer()
        activate(lang)
        for obj in Bagno.objects.all():
            writer.add_document(**obj.index_features())
        deactivate()
        writer.commit()


def recreate_all(sender=None, langs=LANGS, **kwargs):
    """ Deletes the schema, creates it back and recreate all the data
        Good to create from scratch or for schema/data modification
    """
    recreate_index(sender=sender, langs=langs, **kwargs)
    recreate_data(sender=sender, langs=langs,**kwargs)

#signals.post_syncdb.connect(recreate_all)

def set_active_facets_first(facets, active_facets):
    sorted_facets = OrderedDict()
    non_active_facet_items = []
    for item in facets.items():
        if any(facet_dict in active_facets for facet_dict in item[1]):
            sorted_facets[item[0]] = item[1]
        else:
            non_active_facet_items.append(item)
    for non_active_facet_item in non_active_facet_items:
        sorted_facets[non_active_facet_item[0]] = non_active_facet_item[1]
    return sorted_facets


def search(q, filters, groups, query_string, max_facets=5):
    """ Search for a query term and a set o filters
        Returns a list of hits and the representation of the facets
    """
    lang = get_language()
    ix = index.open_dir(index_path(lang))
    hits = []
    facets = [sorting.FieldFacet(g, allow_overlap=True, maptype=sorting.Count) for g in groups]
    # Commented due to a boost error
    #og = qparser.OrGroup.factory(0.5)
    parser = qparser.QueryParser("text", schema=ix.schema)# , group=og)
    #parser.remove_plugin_class(qparser.WildcardPlugin)
    parser.add_plugin(qparser.FuzzyTermPlugin())
    #Adds fuzzy search of distance 1 and prefix 0 to all search terms
    if q not in ("", "*"):
        q = "".join([item + "~" for item in q.split()])
    try:
        q = parser.parse(q)
    except:
        q = None
    if q or filters:
        searcher = ix.searcher()
        for filter in filters:
            filter_name, filter_value = filter.split(":", 1)
            q = q & query.Term(filter_name, filter_value)
        hits = searcher.search(q.normalize(), groupedby=facets)
        facet_groups = {}
        active_facets = []
        querysets = {}
        querysets['services'] = Service.objects.values('slug', 'name', 'hidden',
                                                       'category__slug',
                                                       'category__name',
                                                       'category__order')
        querysets['languages'] = Language.objects
        for group in groups:
            items = [(k, v) for k, v in hits.groups(group).items() if k and v] 
            sorted_facets = sorted(items,
                                   key=operator.itemgetter(1, 0),
                                   reverse=True)
            for facet_slug, facet_value in sorted_facets:
                qs = query_string.copy()
                if not facet_slug:
                    continue
                qs["p"] = "1"
                filter = group + ":" + facet_slug
                if filter in filters:
                    qs.setlist('f', [f for f in filters if f != filter])
                    state = "active"
                else:
                    qs.appendlist('f', filter)
                    state = "available"
                url = qs.urlencode(safe=":")

                if group == "services":
                    for c, o in enumerate(querysets[group]):
                        if o['slug'] == facet_slug:
                            obj = o
                            break
                    if obj['hidden']:
                        continue
                    group_slug = obj['category__slug']
                    group_name = obj['category__name']
                    group_order = obj['category__order']
                    facet_name = obj['name']
                else:
                    obj = querysets[group].get(slug=facet_slug)
                    group_slug = group
                    group_name = obj._meta.verbose_name_plural
                    group_order = 5
                    facet_name = obj.name
                if group_slug not in facet_groups or "facets" not in facet_groups[group_slug]:
                    facet_groups[group_slug] = {'facets': []}
                if len(facet_groups[group_slug]['facets']) < max_facets:
                    facet_groups[group_slug]['name'] = group_name
                    facet_groups[group_slug]['order'] = group_order

                    facet_dict = {
                        'slug': facet_slug,
                        'name': facet_name,
                        'count': facet_value,
                        'url': url,
                    }

                    if state == 'active':
                        facet_dict['group'] = group_name
                        active_facets.append(facet_dict)
                        if len(facet_groups[group_slug]['facets']) == 0:
                            del(facet_groups[group_slug]['facets'])
                    else:
                        facet_groups[group_slug]['facets'].append(facet_dict)
        facets = OrderedDict(sorted(facet_groups.items(),
                             key=lambda x: (x[1]['order'], x[1]['name'])))

    return hits, facets, active_facets
