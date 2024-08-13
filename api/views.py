from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import (
                        User, ApplicantQuestion, 
                        ApplicantOption, Applicant, 
                        StudentQuestion, StudentOption, 
                        Student, ReferralCode
                    )
from .serializers import(
                            UserSerializer, ApplicantQuestionSerializer, 
                            ApplicantOptionSerializer, 
                            ApplicantSerializer, 
                            StudentQuestionSerializer, 
                            StudentOptionSerializer, StudentSerializer,
                            ReferralCodeSerializer                            
                        )
from django.http import JsonResponse
from django.views import View

# User Views
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Applicant Views
class ApplicantQuestionListCreateView(generics.ListCreateAPIView):
    queryset = ApplicantQuestion.objects.all()
    serializer_class = ApplicantQuestionSerializer

class ApplicantOptionListCreateView(generics.ListCreateAPIView):
    queryset = ApplicantOption.objects.all()
    serializer_class = ApplicantOptionSerializer

class ApplicantOptionsView(generics.ListAPIView):
    serializer_class = ApplicantOptionSerializer

    def get_queryset(self):
        question_id = self.kwargs.get('question_id')
        return ApplicantOption.objects.filter(question_id=question_id)

class ApplicantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

# Student Views
class StudentQuestionListCreateView(generics.ListCreateAPIView):
    queryset = StudentQuestion.objects.all()
    serializer_class = StudentQuestionSerializer

class StudentOptionListCreateView(generics.ListCreateAPIView):
    queryset = StudentOption.objects.all()
    serializer_class = StudentOptionSerializer

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentOptionsView(generics.ListAPIView):
    serializer_class = StudentOptionSerializer

    def get_queryset(self):
        question_id = self.kwargs.get('question_id')
        return StudentOption.objects.filter(question_id=question_id)
    
class ReferralCodeListCreateView(generics.ListCreateAPIView):
    queryset = ReferralCode.objects.all()
    serializer_class = ReferralCodeSerializer

class ReferralCodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReferralCode.objects.all()
    serializer_class = ReferralCodeSerializer

class UserPointsView(View):
    def get(self, user_id):
        try:
            user = ReferralCode.objects.get(reffer_id=user_id)
            points = user.points  # Assuming 'points' is a field in your ReferralCode model
            return JsonResponse({'points': points})
        except ReferralCode.DoesNotExist:
            return JsonResponse({'error': 'Referral code not found'}, status=404)


        
def check_telegram_id(request):
    telegram_id = request.GET.get('telegram_id')
    
    if not telegram_id:
        return JsonResponse({"error": "No telegram_id provided"}, status=400)
    
    try:
        telegram_id = int(telegram_id)
    except ValueError:
        return JsonResponse({"error": "Invalid telegram_id format"}, status=400)
    
    is_registered = User.objects.filter(telegram_id=telegram_id).exists()
    
    return JsonResponse({"is_registered": is_registered})

def user_points_detail(request, user_id):
    try:
        user_points = get_object_or_404(ReferralCode, reffer_id=user_id)
        return JsonResponse({'points': user_points.points})
    except ReferralCode.DoesNotExist:
        return JsonResponse({'error': 'User points not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

