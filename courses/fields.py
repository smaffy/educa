from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # нет текущего значения
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # фильтруем объекты с теми же значениями поля
                    # для поля в "for_fields"
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                    # получить последний отсортированый элемент
                    last_item = qs.latest(self.attname)
                    value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField, self).pre_save(model_instance, add)


"""
Вы можете найти дополнительную информацию о написании
пользовательских полей модели в https://docs.djangoproject.com/en/2.0/
howto/custom-model-fields/ .
"""