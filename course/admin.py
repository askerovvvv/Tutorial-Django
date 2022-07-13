from django.contrib import admin

from course.models import *


admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Course)
admin.site.register(SavedCourse)
admin.site.register(CourseRegister)
admin.site.register(SearchHistory)

