from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
import datetime

MOOD_CHOICES=(("Happy", "Happy"), ("Full of fun", "Full of fun"), ("Sad", "Sad"), ("Bored", "Bored"))
COMPLETED_CHOICES=((True, "Yes"), (False, "No"))
EVENT_CHOICES=(("Sport", "Sport"), ("Job", "Job"), ("Study", "Study"), ("Hobby", "Hobby"), ("Culture", "Culture"), ("Date", "Date"), ("Meeting", "Meeting"), ("Tour", "Tour"), ("Relaxation", "Relaxation"), ("Home", "Home"))


class SignUpForm(UserCreationForm):
  email = forms.EmailField(max_length=254, help_text='Этот адрес будет сохранён в вашем профиле')
  captcha = CaptchaField()

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2', )

class ChangeEmail(forms.Form):
  intext = forms.CharField(required=True, label='Change your email')

class MakeBigNote(forms.Form):
  title = forms.CharField(required=True, max_length=50)
  intext = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':180, 'rows':29}), label='')

class RedactBigNote(forms.Form):
  intext = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':180, 'rows':29}), label='')

class RedactLittleNote(forms.Form):
  intext = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':90, 'rows':10}), label='')

class MakeLittleNote(forms.Form):
  def __init__(self, *args, **kwargs):
    kwargs.update(initial={'notifydate': format(datetime.datetime.now(),'%Y-%m-%d %H:%M')})
    super(MakeLittleNote, self).__init__(*args, **kwargs)
  title = forms.CharField(required=True, max_length=50)
  intext = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':90, 'rows':10}), label='')
  isnotify = forms.ChoiceField(choices = COMPLETED_CHOICES, required = True, label="Would you like to get a notification?")
  notifydate = forms.DateTimeField(required=False, initial=format(datetime.datetime.now(),'%Y-%m-%d %H:%M'), widget=forms.DateInput(attrs={'type': 'datetime-local'}), localize=True)

class UploadFile(forms.Form):
  name = forms.CharField(required=True, max_length=50)
  file = forms.FileField()

class MakeEventNote(forms.Form):
  eventdate = forms.TimeField(required=False, initial=format(datetime.datetime.now().time(), '%H:%M'),
                                  widget=forms.DateInput(attrs={'type': 'datetime-local'}), localize=True, label="Enter time of event")
  intext = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':80, 'rows':9}), label='')
  eventtype = forms.ChoiceField(choices=EVENT_CHOICES, required=True, label="Choose what kind of event do you register",
                                widget=forms.RadioSelect)
  image = forms.ImageField()

class RedactEventNote(forms.Form):
  intext = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':90, 'rows':10}), label='')
  eventtype = forms.ChoiceField(choices=EVENT_CHOICES, required=True, label="Choose what kind of event is it",
                                widget=forms.RadioSelect)

class MakeMoodNote(forms.Form):
  title = forms.CharField(required=True, max_length=50)
  mooddate = forms.TimeField(required=False, initial=format(datetime.datetime.now().time(), '%H:%M'),
                                  widget=forms.DateInput(attrs={'type': 'datetime-local'}), localize=True, label="Enter time of event")
  intext = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':80, 'rows':9}), label='')
  eventtype = forms.ChoiceField(choices=EVENT_CHOICES, required=True, label="Choose what kind of event do you register",
                                widget=forms.RadioSelect)
  moodtype = forms.ChoiceField(choices=MOOD_CHOICES, required=True, label="Choose what kind of mood do(did) you have",
                                widget=forms.RadioSelect)