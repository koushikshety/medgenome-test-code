from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    
    # Categories
    path('api/categories/', views.categories, name='categories'),
    path('api/categories/<str:name>/', views.category_detail, name='category_detail'),
    
    # Documents
    path('api/documents/', views.documents, name='documents'),
    path('api/documents/<str:name>/', views.document_detail, name='document_detail'),
    
    # Test Codes
    path('api/test-codes/', views.test_codes, name='test_codes'),
    path('api/test-codes/<str:mgm_code>/', views.test_code_detail, name='test_code_detail'),
    
    # Pre Data
    path('api/pre-data/', views.pre_data, name='pre_data'),
    path('api/pre-data/<int:id>/', views.pre_data_detail, name='pre_data_detail'),
    path('api/pre-data/approve/', views.approve_pre_data, name='approve_pre_data'),
    path('api/pre-data/delete-all/', views.delete_all_pre_data, name='delete_all_pre_data'),
    
    # Logs
    path('api/logs/', views.logs, name='logs'),
    path('api/logs/clear/', views.clear_logs, name='clear_logs'),
    path('api/logs/delete-last-week/', views.delete_last_week_logs, name='delete_last_week_logs'),
    
    # Lock Code
    path('api/lock-code/', views.lock_code, name='lock_code'),
]