from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_score, name='점수 등록'),
    path('rankings/', views.get_rankings, name='랭킹 조회'),
    path('clear/', views.clear_scores, name='랭킹 초기화'),
]