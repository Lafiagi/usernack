from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    CONFIRMED = "confirmed", _("Confirmed")
    PREPARING = "preparing", _("Preparing")
    BAKING = "baking", _("Baking")
    READY = "ready", _("Ready")
    DELIVERED = "delivered", _("Delivered")
    CANCELLED = "cancelled", _("Cancelled")
