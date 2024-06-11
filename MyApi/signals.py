from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Table , Person

@receiver(post_save, sender=Table)
def update_person_table_type(sender,instance,**kwargs):
    if instance.persondetail:
        person=instance.persondetail
        person.tabletype= instance
        person.save()