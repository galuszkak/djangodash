# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView


def home_view(request):
    return render_to_response('index.html',{}, context_instance=RequestContext(request))


class GameDemoView(TemplateView):
    template_name = "game_demo_ui.html"