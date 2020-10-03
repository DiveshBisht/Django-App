from django.contrib import admin
from .models import testDetail, studentProfile, testQuestion, studentMark, clientProfile


admin.site.register(testDetail)
admin.site.register(studentProfile)
admin.site.register(testQuestion)
admin.site.register(studentMark)
admin.site.register(clientProfile)