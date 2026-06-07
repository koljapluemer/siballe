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
]
