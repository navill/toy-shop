from typing import Dict, Optional, Tuple

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel, SafeDeleteMixin


class MetaDateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class CommonModel(SafeDeleteMixin, MetaDateModel):
    restored_at = models.DateTimeField(null=True, blank=True)

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        abstract = True

    def undelete(self, force_policy: Optional[int] = None, **kwargs) -> Tuple[int, Dict[str, int]]:
        self.restored_at = now()
        modify_fields = ["restored_at", "deleted_at"]
        if kwargs.get("updated_fields", None):
            kwargs["updated_fields"].extend(modify_fields)
        else:
            kwargs["update_fields"] = modify_fields
        return super().undelete(force_policy, **kwargs)
