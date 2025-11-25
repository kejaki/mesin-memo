from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.cms_dashboard, name='cms_dashboard'),
    path('create/', views.create_content, name='create_content'),
    path('manage/', views.manage_content, name='manage_content'),  # Admin content management
    path('content/<int:content_id>/', views.content_detail, name='content_detail'),
    path('content/<int:content_id>/edit/', views.edit_content, name='edit_content'),
    path('content/<int:content_id>/delete/', views.delete_content, name='delete_content'),
    path('content/<int:content_id>/status/', views.update_content_status, name='update_content_status'),
    path('jobs/available/', views.available_jobs, name='available_jobs'),
    path('jobs/my/', views.my_jobs, name='my_jobs'),
    path('jobs/<int:content_id>/claim/', views.claim_job, name='claim_job'),
    path('jobs/<int:content_id>/unclaim/', views.unclaim_job, name='unclaim_job'),
    path('role/<int:role_id>/claim/', views.claim_role, name='claim_role'),
    path('assignment/<int:assignment_id>/unclaim/', views.unclaim_role, name='unclaim_role'),
]
