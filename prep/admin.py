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
    list_display = ("id", "mocktest", "type", "text", "correct_answer", "has_explanation", "has_concept")
    list_filter = ("mocktest", "type")
    search_fields = ("text", "explanation", "concept")

    def has_explanation(self, obj):
        return bool(obj.explanation)

    has_explanation.boolean = True
    has_explanation.short_description = "Explanation"

    def has_concept(self, obj):
        return bool(obj.concept)

    has_concept.boolean = True
    has_concept.short_description = "Concept"


@admin.register(Result)
class ResultAdmin(ImportExportModelAdmin):
    list_display = ("id", "user", "mocktest", "score", "date")
    list_filter = ("mocktest", "date")
    search_fields = ("user__username",)


@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin):
    list_display = ("id", "user", "full_name", "phone", "updated_at")
    search_fields = ("user__username", "full_name", "phone")