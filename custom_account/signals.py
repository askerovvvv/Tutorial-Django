# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from custom_account.models import CustomUser, UserProfile
# from custom_account.views import ActivationView
#
#
# @receiver(post_save, sender=CustomUser)
# def user_profile(sender, instance, created, **kwargs):
#     profile = UserProfile.objects.create(user=instance.email, date_joined=instance.date_joined, is_active=instance.is_active, is_superuser=instance.is_superuser)
#     profile.save()
#
#     print(instance.date_joined)
#     print(instance.is_active)
#     print(instance.is_superuser)
#
#     print('=================')
    # course = Course.objects.get(pk=instance.course.id)
    # if instance.description != '':
    #     course.comment += 1
    #     print(course.comment)
    #     course.save()


