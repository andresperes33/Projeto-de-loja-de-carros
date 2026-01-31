from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from cars.models import Car

@receiver(post_save, sender=Car)
def car_post_save(sender, instance, created, **kwargs):
    if created:
        print('Carro criado com sucesso!')
    else:
        print('Carro atualizado com sucesso!')

@receiver(post_delete, sender=Car)
def car_post_delete(sender, instance, **kwargs):
    print('Carro deletado com sucesso!')
