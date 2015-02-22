# coding=utf-8

from django.db import models
from django.utils.timezone import now


# class CPBaseManager(models.Manager):
#     def get_queryset(self):
#         return super(CPBaseManager, self).get_queryset().filter(deleted=False)


# class CPBaseDeleteManager(models.Manager):
#     def get_queryset(self):
#         return super(CPBaseDeleteManager, self).get_queryset().filter(deleted=True)


class CPBaseModel(models.Model):
    # deleted = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False, blank=True, null=True)
    modified = models.DateTimeField(editable=False, blank=True, null=True)

    objects = models.Manager()
    # valid_objects = CPBaseManager()
    # deleted_objects = CPBaseDeleteManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = now()
        self.modified = now()
        return super(CPBaseModel, self).save(*args, **kwargs)

    # def delete(self, real=False, *args, **kwargs):
    #     if real:
    #         super(KSBaseModel, self).delete(*args, **kwargs)
    #     else:
    #         self.deleted = True
    #         self.save()
