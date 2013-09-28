from django.contrib.admin.options import TabularInline

__author__ = 'tptak'

from django.contrib import admin
from models import *


class ConfigurationInline(TabularInline):
    model = Configuration


class StatisticInline(TabularInline):
    model = Statistic


class GameAdmin(admin.ModelAdmin):
    inlines = [ConfigurationInline, StatisticInline]

    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide inline forms in the add view
            if obj is None:
                continue
            yield inline.get_formset(request, obj)


admin.site.register(MemoUser)
admin.site.register(Game, GameAdmin)
admin.site.register(Configuration)
admin.site.register(Statistic)