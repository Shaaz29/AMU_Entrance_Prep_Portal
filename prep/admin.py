from django.contrib import admin
from .models import Course, MockTest, Question, Result


# ================= COURSE ADMIN =================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# ================= MOCKTEST ADMIN =================
@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "year", "duration")
    list_filter = ("course", "year")
    search_fields = ("course__name",)


# ================= QUESTION ADMIN =================
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "mocktest", "type", "text", "correct_answer")
    list_filter = ("mocktest", "type")
    search_fields = ("text",)


# ================= RESULT ADMIN =================
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "mocktest", "score", "date")
    list_filter = ("mocktest", "date")
    search_fields = ("user__username",)