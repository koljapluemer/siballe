from django.contrib import admin

from core.models import BuildingBlock, Dialog, DialogLine, DialogNode, DialogUtterance, Situation, SituationalUtterance, SpeechAct

admin.site.register(BuildingBlock)
admin.site.register(Dialog)
admin.site.register(DialogNode)
admin.site.register(DialogUtterance)
admin.site.register(DialogLine)
admin.site.register(Situation)
admin.site.register(SituationalUtterance)
admin.site.register(SpeechAct)
