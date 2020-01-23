from django import forms
from .models import Rating, Book, User


Rating_CHOICES = (
    (1, 'Poor'),
    (2, 'Average'),
    (3, 'Good'),
    (4, 'Very Good'),
    (5, 'Excellent')
)

class RatingForm(forms.ModelForm):
   class Meta:
      model = Rating
      fields = ('book', 'user','value')
      widgets = {
            'value': forms.widgets.RadioSelect(choices=Rating.ratings),
        }

# class AddRatingForm(forms.Form):
#    book = forms.IntegerField(choices=Rating_CHOICES, default=1)
#    user = forms.ModelChoiceField(queryset=User.objects, empty_label=None)
#    rating = forms.ModelChoiceField(queryset=Rating.objects, empty_label=None)