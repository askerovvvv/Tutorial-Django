from django.db.models.signals import post_save
from django.dispatch import receiver

from course.models import Review, Course


@receiver(post_save, sender=Review,)
def comment_counter(sender, instance, created, **kwargs):
    print(sender)
    course = Course.objects.get(pk=instance.course.id)
    if instance.description != '':
        course.comment += 1
        print(course.comment)
        course.save()


