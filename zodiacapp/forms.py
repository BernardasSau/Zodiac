from django import forms
from .models import Comment, UserProfile
from .models import RelationshipStatus


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Komentaras'
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['location', 'date_of_birth', 'zodiac', 'profile_picture']
        widgets = {
            'zodiac': forms.Select(choices=UserProfile.ZODIAC_CHOICES),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)


class RelationshipStatusForm(forms.ModelForm):
    class Meta:
        model = RelationshipStatus
        fields = ['status', 'color']


class NatalChartForm(forms.Form):
    full_name = forms.CharField(label='Vardas')
    day = forms.IntegerField(label='Diena')
    month = forms.IntegerField(label='Mėnesis')
    year = forms.IntegerField(label='Metai')
    hour = forms.IntegerField(label='Valanda')
    min = forms.IntegerField(label='Minutė')
    sec = forms.IntegerField(label='Sekundė')
    gender = forms.ChoiceField(choices=[('male', 'Vyras'), ('female', 'Moteris')], label='Lytis')
    place = forms.CharField(label='Vieta pvz.: Kaunas')
    lat = forms.FloatField(label='Platuma pvz.: 54.89806')
    lon = forms.FloatField(label='Ilguma pvz.: 23.90361')
    tzone = forms.FloatField(label='Laiko juosta pvz. Lietuva: 2')
