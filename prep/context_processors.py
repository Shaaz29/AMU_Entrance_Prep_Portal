from .models import Course


def navbar_courses(request):
    if not request.user.is_authenticated:
        return {}
    return {
        'navbar_courses': Course.objects.all().order_by('name'),
    }
