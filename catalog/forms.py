import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Enter a date between now and 4 weeks (default 3)')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        if data < datetime.date.today():
            raise ValidationError('Invalid date - renewal in past')
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError('Invalid date - renewal date more than 4 weeks')

        return data

# Так же ~ вариант из класса ModelForm
class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        if data < datetime.date.today():
            raise ValidationError(('Invalid date - renewal in past'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(('Invalid date - renewal more than 4 weeks ahead'))
        return data

    class Meta:
        model = BookInstance
        fields = ('due_back',)
        labels = {'due_back': 'Renewal date', }
        help_text = {'due_back': "Enter a date between now and 4 weeks (default 3).", }
