from django.db import models


class BaseModel(models.Model):
    """Model provides the defualt creation and update times
       for all models.

    Args:
        created_at (datetime): the exact time the row was inserted
        updated_at (datetime): the last time the row was updated.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
