from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Recipe(models.Model):
    name = models.CharField(_('name'), null=False, blank=False, max_length=128, db_index=True, help_text=_('Recipe Name'))
    description = models.TextField(_('description'), null=True, blank=True, help_text=_('Recipe Description'))
    status = models.BooleanField(_('status'), choices=settings.STATUSES,
                                 default=settings.HIDDEN, help_text=_("published/hidden this recipe."))


    def __str__(self):
        return self.name
