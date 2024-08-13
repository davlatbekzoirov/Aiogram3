from rest_framework import serializers
from .models import (
                        User, ApplicantQuestion, 
                        ApplicantOption, Applicant, 
                        StudentQuestion, StudentOption, 
                        Student, ReferralCode
                    )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'age', 'phone_number', 'role' ,'telegram_id']  # Fixed the typo here

class ApplicantQuestionSerializer(serializers.ModelSerializer):
    options = serializers.StringRelatedField(many=True)

    class Meta:
        model = ApplicantQuestion
        fields = ['id', 'text', 'options']

class ApplicantOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantOption
        fields = ['id', 'question', 'text', 'is_true']

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ['id']

class StudentQuestionSerializer(serializers.ModelSerializer):
    options = serializers.StringRelatedField(many=True)

    class Meta:
        model = StudentQuestion
        fields = ['id', 'text', 'options']

class StudentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOption
        fields = ['id', 'question', 'text', 'is_true']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id']

class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ['id', 'reffer_id', 'flag', 'user_realy_name', 'points']
