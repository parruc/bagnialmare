# -*- coding: utf-8 -*-
from django.urls import path, re_path
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    path('', views.HomepageView.as_view(), name="homepage",),
    #  re_path(_(r'^about-us$'), views.AboutUsView.as_view(), name="about-us",),
    re_path(_(r'^concorso2014/$'), views.Concorso2014View.as_view(), name="concorso-2014",),
    # re_path(_(r'^terms/$'), views.UserTermsAndPrivacyView.as_view(), name="user-terms",),
    re_path(_(r'^privacy/$'), views.ManagerPrivacyView.as_view(), name="manager-privacy",),
    re_path(_(r'^conditions/$'), views.ManagerTermsView.as_view(), name="manager-terms",),
    re_path(_(r'^bagni/$'), views.BagniView.as_view(), name="bagni",),
    re_path(_(r'^bagni/(?P<neighbourhood>[-\w]+)/(?P<slug>[-\w]+)/$'), views.BagnoView.as_view(), name="bagno"),
    re_path(_(r'^bagni/(?P<neighbourhood>[-\w]+)/(?P<slug>[-\w]+)/edit/$'), views.BagnoEdit.as_view(), name="bagno-edit"),
    re_path(_(r'^bagni/(?P<neighbourhood>[-\w]+)/(?P<slug>[-\w]+)/contacts/$'), views.BagnoContacts.as_view(), name="bagno-contacts"),
    re_path(_(r'^bagni/(?P<neighbourhood>[-\w]+)/(?P<slug>[-\w]+)/book/$'), views.BagnoBooking.as_view(), name="bagno-booking"),
    re_path(_(r'^search/$'), views.SearchView.as_view(), name="search"),
    # re_path(_(r'^service-categories/$'), views.ServiceCategoriesView.as_view(), name="service-categories"),
    # re_path(_(r'^service-category/(?P<slug>[-\w]+)/$'), views.ServiceCategoryView.as_view(), name="service-category"),
    # re_path(_(r'^services/$'), views.ServicesView.as_view(), name="services"),
    # re_path(_(r'^services/(?P<slug>[-\w]+)/$'), views.ServiceView.as_view(), name="service"),
    # re_path(_(r'^stabilimenti-balneari/services/(?P<facility_slug>[-\w]+)/(?P<neighbourhood_slug>[-\w]+)/$'), views.BagniByFacilityAndNeighbourhoodView.as_view(),  name="bagni-by-facility-and-neighbourhood"),
    # re_path(_(r'^neighbourhood/(?P<slug>[-\w]+)/$'), views.NeighbourhoodView.as_view(), name="neighbourhood"),
    # re_path(_(r'^neighbourhoods/$'), views.NeighbourhoodsView.as_view(), name="neighbourhoods"),
    # re_path(_(r'^municipality/(?P<slug>[-\w]+)/$'), views.MunicipalityView.as_view(), name="municipality"),
    # re_path(_(r'^municipalities/$'), views.MunicipalitiesView.as_view(), name="municipalities"),
    # re_path(_(r'^district/(?P<slug>[-\w]+)/$'), views.DistrictView.as_view(), name="district"),
    # re_path(_(r'^districts/$'), views.DistrictsView.as_view(), name="districts"),
    re_path(_(r'^json/autocomplete/places$'), views.JsonAutocompletePlaces.as_view(), name="json-autocomplete-places"),
    re_path(_(r'^json/autocomplete/searchterms$'), views.JsonAutocompleteSearchterms.as_view(), name="json-autocomplete-searchterms"),
    re_path(_(r'^json/neighbourhood/(?P<id>\d+)/$'), views.JsonBagniInNeighbourhood.as_view(), name="json-bagni-neighbourhood"),
    re_path(_(r'^json/bbox/(?P<x1>[\.\-\+\d]+)/(?P<y1>[\.\-\+\d]+)/(?P<x2>[\.\-\+\d]+)/(?P<y2>[\.\-\+\d]+)$'), views.JsonSearchBoundingBox.as_view(), name="json-search-bbox"),
]
