from django.contrib import admin

from lesson.models import *

#
# class ImageInAdminForAdviser(admin.TabularInline):
#     model = AdviserImage
#     fields = ('image', )
#     max_num = 1
#
#
# @admin.register(Adviser)
# class AdviserAdmin(admin.ModelAdmin):
#     inlines = [
#         ImageInAdminForAdviser
#     ]


# class VideoInAdmin(admin.TabularInline):
#     # model = Video
#     # fields = ('video', )
#     # max_num = 1


# @admin.register(Lesson)
# class LessonAdmin(admin.ModelAdmin):
#     inlines = [
#         VideoInAdmin
#     ]

admin.site.register(Lesson)