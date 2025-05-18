from django.urls import path
from . import views

app_name = 'medical_care'

urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<slug:slug>/', views.tagged, name='tagged'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('assessment/', views.patient_assessment, name='patient_assessment'),
    path('assessment/step/<int:step_id>/', views.patient_assessment_step, name='assessment_step'),
    path('assessment/result/', views.assessment_result, name='assessment_result'),
    path('cpr-timer/', views.cpr_timer_view, name='cpr_timer'),
    path('<slug:emergency_slug>/', views.get_info_medical_care, name='info'),
    path('call-ambulance/', views.call_ambulance, name='call_ambulance'),
]
