# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, View
from braces.views import LoginRequiredMixin


def home_view(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))


class GameDemoView(TemplateView):
    template_name = "game_demo_ui.html"


class GameView(View):
    game_id = None
    template_name = "game_ui.html"


class AboutView(TemplateView):
    template_name = "about.html"


class MainView(LoginRequiredMixin, TemplateView):
    template_name = "main_view.html"