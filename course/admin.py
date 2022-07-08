from django.contrib import admin

from course.models import *

from lesson.models import AdviserImage
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Like)


class ImageInAdminForAdviser(admin.TabularInline):
    model = AdviserImage
    fields = ('image', )
    max_num = 1


@admin.register(Adviser)
class AdviserAdmin(admin.ModelAdmin):
    inlines = [
        ImageInAdminForAdviser
    ]


class ImageForCourse(admin.TabularInline):
    model = CourseImage
    fields = ('course_image', )
    max_num = 1


@admin.register(Course)
class CourseInAdmin(admin.ModelAdmin):
    inlines = [
        ImageForCourse
    ]


