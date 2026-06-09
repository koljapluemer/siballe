from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('languages/', views.language_list, name='language_list'),
    path('languages/new/', views.language_create, name='language_create'),
    path('languages/<str:pk>/', views.language_detail, name='language_detail'),
    path('languages/<str:pk>/edit/', views.language_update, name='language_update'),
    path('languages/<str:pk>/delete/', views.language_delete, name='language_delete'),
    path('building-blocks/', views.building_block_list, name='building_block_list'),
    path('building-blocks/new/', views.building_block_create, name='building_block_create'),
    path('building-blocks/practice/', views.building_block_practice, name='building_block_practice'),
    path('building-blocks/<int:pk>/', views.building_block_detail, name='building_block_detail'),
    path('building-blocks/<int:pk>/json/', views.building_block_json, name='building_block_json'),
    path('building-blocks/<int:pk>/edit/', views.building_block_update, name='building_block_update'),
    path('building-blocks/<int:pk>/delete/', views.building_block_delete, name='building_block_delete'),
    path('sentences/search/', views.sentence_search, name='sentence_search'),
    path('sentences/', views.sentence_list, name='sentence_list'),
    path('sentences/new/', views.sentence_create, name='sentence_create'),
    path('sentences/<int:pk>/', views.sentence_detail, name='sentence_detail'),
    path('sentences/<int:pk>/edit/', views.sentence_update, name='sentence_update'),
    path('sentences/<int:pk>/delete/', views.sentence_delete, name='sentence_delete'),
    path('situations/', views.situation_list, name='situation_list'),
    path('situations/new/', views.situation_create, name='situation_create'),
    path('situations/<int:pk>/', views.situation_detail, name='situation_detail'),
    path('situations/<int:pk>/edit/', views.situation_update, name='situation_update'),
    path('situations/<int:pk>/delete/', views.situation_delete, name='situation_delete'),
    path('speech-acts/search/', views.speech_act_search, name='speech_act_search'),
    path('speech-acts/', views.speech_act_list, name='speech_act_list'),
    path('speech-acts/new/', views.speech_act_create, name='speech_act_create'),
    path('speech-acts/<int:pk>/', views.speech_act_detail, name='speech_act_detail'),
    path('speech-acts/<int:pk>/edit/', views.speech_act_update, name='speech_act_update'),
    path('speech-acts/<int:pk>/delete/', views.speech_act_delete, name='speech_act_delete'),
    path('situational-utterances/', views.situational_utterance_list, name='situational_utterance_list'),
    path('situational-utterances/new/', views.situational_utterance_create, name='situational_utterance_create'),
    path('situational-utterances/<int:pk>/', views.situational_utterance_detail, name='situational_utterance_detail'),
    path('situational-utterances/<int:pk>/edit/', views.situational_utterance_update, name='situational_utterance_update'),
    path('situational-utterances/<int:pk>/delete/', views.situational_utterance_delete, name='situational_utterance_delete'),
]
