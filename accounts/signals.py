import uuid
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
User = get_user_model()


@receiver(post_save, sender=User)
def set_referral_count(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(email=instance)
        if user.referral_code:
            refer_by = User.objects.get(my_ref_code=user.referral_code)
            if refer_by is not None:
                refer_by.my_ref_count = refer_by.my_ref_count + 1
                refer_by.save()

