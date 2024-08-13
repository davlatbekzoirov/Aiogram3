from django.contrib import admin
from .models import (
                        User, ApplicantQuestion, 
                        ApplicantOption, Applicant, 
                        StudentQuestion, StudentOption, 
                        Student, ReferralCode
                    )

admin.site.register(User)
admin.site.register(ApplicantQuestion)
admin.site.register(ApplicantOption)
admin.site.register(Applicant)
admin.site.register(StudentQuestion)
admin.site.register(StudentOption)
admin.site.register(Student)
admin.site.register(ReferralCode)
