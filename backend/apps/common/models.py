import uuid

from django.db import models


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(archived_at__isnull=False)

    def archive(self):
        from django.utils import timezone

        return self.update(archived_at=timezone.now())


class SoftDeleteModel(models.Model):
    archived_at = models.DateTimeField(null=True, blank=True)
    objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True

    def archive(self):
        from django.utils import timezone

        self.archived_at = timezone.now()
        self.save(update_fields=["archived_at", "updated_at"])


class TenantModel(UUIDModel):
    organization = models.ForeignKey(
        "tenants.Organization",
        on_delete=models.CASCADE,
        related_name="records",
    )

    class Meta:
        abstract = True
