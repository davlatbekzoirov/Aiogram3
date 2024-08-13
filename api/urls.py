from django.urls import path
from .views import (
                        UserListCreateView, UserDetailView, 
                        ApplicantQuestionListCreateView, 
                        ApplicantOptionListCreateView, 
                        ApplicantDetailView, StudentQuestionListCreateView, 
                        StudentOptionListCreateView, StudentDetailView,
                        ApplicantOptionsView, StudentOptionsView,
                        check_telegram_id, ReferralCodeDetailView, 
                        ReferralCodeListCreateView, UserPointsView
                    )

urlpatterns = [
    path('check_telegram_id/', check_telegram_id, name='check_telegram_id'),

    path('users/', UserListCreateView.as_view()),   
    path('users/<int:pk>/', UserDetailView.as_view()),

    path('applicants/questions/', ApplicantQuestionListCreateView.as_view()),
    path('applicants/questions/<int:pk>/', ApplicantOptionListCreateView.as_view()),
    path('applicants/options/', ApplicantOptionsView.as_view()),
    path('applicants/<int:pk>/', ApplicantDetailView.as_view()),

    path('students/questions/', StudentQuestionListCreateView.as_view()),
    path('students/questions/<int:pk>/', StudentOptionListCreateView.as_view()),
    path('students/options/', StudentOptionsView.as_view()),
    path('students/<int:pk>/', StudentDetailView.as_view()),

    path('referral-codes/', ReferralCodeListCreateView.as_view(), name='referralcode-list-create'),
    path('referral-codes/<int:pk>/', ReferralCodeDetailView.as_view(), name='referralcode-detail'),

    path('user-points/<int:user_id>/', UserPointsView.as_view(), name='user_points'),

]