from django.db import models
from django.utils import timezone

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def get_deleted(self):
        return super().get_queryset().filter(is_deleted=True)

    def restore(self, id):
        try:
            to_restore = self.get_deleted().get(pk=id)
            to_restore.is_deleted = False
            to_restore.deleted_at = None
            to_restore.save()
        except self.model.DoesNotExist:
            raise ValueError("Object with this ID does not exist or is not deleted.")
