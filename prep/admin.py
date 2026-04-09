from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Course, MockTest, Question, Result, UserProfile


@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(MockTest)
class MockTestAdmin(ImportExportModelAdmin):
    list_display = ("id", "course", "year", "duration")
    list_filter = ("course", "year")
    search_fields = ("course__name",)


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    list_display = ("id", "mocktest", "text", "correct_answer", "has_explanation")
    list_filter = ("mocktest",)
    search_fields = ("text", "explanation")
    exclude = ("type",)

    def save_model(self, request, obj, form, change):
        obj.type = 'MCQ'
        super().save_model(request, obj, form, change)

    def has_explanation(self, obj):
        return bool(obj.explanation)

    has_explanation.boolean = True
    has_explanation.short_description = "Explanation"


@admin.register(Result)
class ResultAdmin(ImportExportModelAdmin):
    list_display = ("id", "user", "mocktest", "score", "date")
    list_filter = ("mocktest", "date")
    search_fields = ("user__username",)


@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin):
    list_display = ("id", "user", "full_name", "phone", "updated_at")
    search_fields = ("user__username", "full_name", "phone")