from django.contrib import admin

from .models import Node, Rel, Situation, SituationRelation


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ("id", "kind", "language", "content", "state")
    list_filter = ("kind", "language", "state")
    search_fields = ("content", "credit")


@admin.register(Rel)
class RelAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "label", "receiver", "state")
    list_filter = ("label", "state")
    search_fields = ("note", "credit")
    autocomplete_fields = ("sender", "receiver")


@admin.register(Situation)
class SituationAdmin(admin.ModelAdmin):
    list_display = ("id", "language", "description")
    list_filter = ("language",)
    search_fields = ("description",)


@admin.register(SituationRelation)
class SituationRelationAdmin(admin.ModelAdmin):
    list_display = ("id", "situation", "node", "relevance")
    list_filter = ("relevance",)
    autocomplete_fields = ("situation", "node")
