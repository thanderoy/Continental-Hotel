"""
Houses code used acroos multiple apps.
"""
import uuid

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Base class for all models."""

    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    created = models.DateTimeField(
        db_index=True, editable=False, default=timezone.now)
    updated = models.DateTimeField(db_index=True, default=timezone.now)

    def save(self, *args, **kwargs):
        """Ensure validations are run and updated/created preserved."""
        self.updated = timezone.now()
        self.full_clean(exclude=None)
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        """Define a default least recently used ordering."""

        abstract = True
        ordering = ("-updated", "-created")
