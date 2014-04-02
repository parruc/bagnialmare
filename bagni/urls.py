# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views
from django.utils.translation import ugettext_lazy as _

urlpatterns = patterns(
    '',
    url(r'^$', views.HomepageView.as_view(), name="homepage",),
    url(r'^about-us$', views.AboutUsView.as_view(), name="about-us",),
    url(_(r'^bagni/$'), views.BagniView.as_view(), name="bagni",),
    url(_(r'^bagno/(?P<slug>[-\w]+)/$'), views.BagnoView.as_view(), name="bagno"),
    url(_(r'^bagno/(?P<slug>[-\w]+)/edit/$'), views.BagnoEdit.as_view(), name="bagno-edit"),
    url(_(r'^bagno/(?P<slug>[-\w]+)/contacts/$'), views.BagnoContacts.as_view(), name="bagno-contacts"),
    url(_(r'^search/$'), views.SearchView.as_view(), name="search"),
    url(_(r'^service-categories/$'), views.ServiceCategoriesView.as_view(), name="service-categories"),
    url(_(r'^service-category/(?P<slug>[-\w]+)/$'), views.ServiceCategoryView.as_view(), name="service-category"),
    url(_(r'^services/$'), views.ServicesView.as_view(), name="services"),
    url(_(r'^services/(?P<slug>[-\w]+)/$'), views.ServiceView.as_view(), name="service"),
    url(_(r'^neighbourhood/(?P<slug>[-\w]+)/$'), views.NeighbourhoodView.as_view(), name="neighbourhood"),
    url(_(r'^neighbourhoods/$'), views.NeighbourhoodsView.as_view(), name="neighbourhoods"),
    url(_(r'^municipality/(?P<slug>[-\w]+)/$'), views.MunicipalityView.as_view(), name="municipality"),
    url(_(r'^municipalities/$'), views.MunicipalitiesView.as_view(), name="municipalities"),
    url(_(r'^district/(?P<slug>[-\w]+)/$'), views.DistrictView.as_view(), name="district"),
    url(_(r'^districts/$'), views.DistrictsView.as_view(), name="districts"),
    url(_(r'^json/autocomplete/places$'), views.JsonAutocompletePlaces.as_view(), name="json-autocomplete-places"),
    url(_(r'^json/autocomplete/searchterms$'), views.JsonAutocompleteSearchterms.as_view(), name="json-autocomplete-searchterms"),
)
