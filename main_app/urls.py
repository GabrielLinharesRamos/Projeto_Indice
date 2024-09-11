from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainPage,name='mainPage'),
    path('dados/<int:id>/', views.dividePaginas, name='dados_organizados'),
    path('dados/<str:palavra>/<int:dadosPorPagina>', views.busca, name='busca'),
]
