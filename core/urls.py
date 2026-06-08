from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('building-blocks/', views.building_block_list, name='building_block_list'),
    path('building-blocks/new/', views.building_block_create, name='building_block_create'),
    path('building-blocks/practice/', views.building_block_practice, name='building_block_practice'),
    path('building-blocks/<int:pk>/', views.building_block_detail, name='building_block_detail'),
    path('building-blocks/<int:pk>/json/', views.building_block_json, name='building_block_json'),
    path('building-blocks/<int:pk>/edit/', views.building_block_update, name='building_block_update'),
    path('building-blocks/<int:pk>/delete/', views.building_block_delete, name='building_block_delete'),
    path('building-blocks/<int:bb_pk>/sentences/new/', views.sentence_create, name='sentence_create'),
    path('building-blocks/<int:bb_pk>/sentences/<int:pk>/edit/', views.sentence_update, name='sentence_update'),
    path('building-blocks/<int:bb_pk>/sentences/<int:pk>/delete/', views.sentence_delete, name='sentence_delete'),
    path('situations/', views.situation_list, name='situation_list'),
    path('situations/new/', views.situation_create, name='situation_create'),
    path('situations/<int:pk>/', views.situation_detail, name='situation_detail'),
    path('situations/<int:pk>/edit/', views.situation_update, name='situation_update'),
    path('situations/<int:pk>/delete/', views.situation_delete, name='situation_delete'),
    path('situations/<int:situation_pk>/speech-acts/new/', views.speech_act_create, name='speech_act_create'),
    path('situations/<int:situation_pk>/speech-acts/<int:pk>/edit/', views.speech_act_update, name='speech_act_update'),
    path('situations/<int:situation_pk>/speech-acts/<int:pk>/delete/', views.speech_act_delete, name='speech_act_delete'),
]
