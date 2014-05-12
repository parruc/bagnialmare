import json

from django import http
from django.views.generic import View

from .forms import UserFeedbackForm

class UserFeedbackFormView(View):
    def post(self, request, *args, **kwargs):
        form = UserFeedbackForm(request.POST)
        content = {}
        if form.is_valid():
            form.save()
        else:
            content = form.errors
            # clean the wrong email and save the form with empty mail
            form = UserFeedbackForm({'bagno' : form.data['bagno'],
                                     'email' : '',
                                     })
            form.save()
        return http.HttpResponse(json.dumps(content),
                                 content_type='application/json')


