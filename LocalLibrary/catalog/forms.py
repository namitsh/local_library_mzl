from django import forms

from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text=_('Enter a date between now and 4 weeks (default 3).'))

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < date.today():
            raise ValidationError(_("Invalid date - renewal in past"))

        if data > date.today() + timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data
