from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'polls'
urlpatterns = [
    url(r'^login', auth_views.login, {'template_name': 'polls/login.html'}, name='login'),  # ログインページ
    url(r'^logout', auth_views.logout, name='logout'),  # ログアウトページ

    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/add_choice/', views.add_choice, name='add_choice'),  # choiceの投稿先
    path('<int:question_id>/upload_image/', views.upload_image, name='upload_image'),  #

]