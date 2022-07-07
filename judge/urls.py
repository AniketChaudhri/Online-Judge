from django.contrib import admin
from django.urls import path
from judge import views

urlpatterns = [
    path('judge/', views.index, name='home'),
    # path('^$', views.index, name='index'),
    path('judge/register/', views.register_user, name='register'),
    # path('^logout/$', views.loguserout, name='loguserout'),
    path('judge/login/', views.loguserin, name='loguserin'),
    path('judge/add-problem/', views.add_problem, name="add_problem"),
    path('judge/problems', views.all_problems, name="all_problems"),
    path('problems/<pid>', views.view_problem, name="view_prob"),
    # path('^submit/(?P<pid>[\w\-]+)$', views.submit, name="submit"),
    # path('^submission/(?P<submission_id>[\d]+)$',
    #     views.view_submission, name="view_sub"),
]
