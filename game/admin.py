__author__ = 'tptak'

from django.contrib import admin
from models import *

admin.site.register(MemoUser)
admin.site.register(Game)
admin.site.register(Configuration)
admin.site.register(Statistic)