from django.contrib import admin

from core.models import BuildingBlock, Situation, SituationalUtterance, SpeechAct

admin.site.register(BuildingBlock)
admin.site.register(Situation)
admin.site.register(SituationalUtterance)
admin.site.register(SpeechAct)
