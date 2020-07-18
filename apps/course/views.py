from django.shortcuts import render


def course_index(request):
    return render(request, 'course/course.html')


def course_detail(request, course_id):
    return render(request, 'course/course_detail.html')
