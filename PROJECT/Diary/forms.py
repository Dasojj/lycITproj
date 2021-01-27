from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
import datetime

NUM_CHOICES=((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))
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
  def __init__(self, *args, **kwargs):
    kwargs.update(initial={'eventdate': format(datetime.datetime.now(),'%H:%M')})
    super(MakeEventNote, self).__init__(*args, **kwargs)
  eventdate = forms.TimeField(required=False, initial=format(datetime.datetime.now().time(), '%H:%M'),
                                  widget=forms.DateInput(attrs={'type': 'datetime-local'}), localize=True, label="Enter time of event")
  intext = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':80, 'rows':9}), label='')
  eventtype = forms.ChoiceField(choices=EVENT_CHOICES, required=True, label="Choose what kind of event do you register",
                                widget=forms.RadioSelect)
  isphoto = forms.ChoiceField(choices = COMPLETED_CHOICES, required = True, label="Would you like to add the photo?")
  image = forms.ImageField(required=False)

class RedactEventNote(forms.Form):
  intext = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':90, 'rows':10}), label='')
  eventtype = forms.ChoiceField(choices=EVENT_CHOICES, required=True, label="Choose what kind of event is it",
                                widget=forms.RadioSelect)

class MakeMoodNote(forms.Form):
  def __init__(self, *args, **kwargs):
    kwargs.update(initial={'mooddate': format(datetime.datetime.now(),'%H:%M')})
    super(MakeMoodNote, self).__init__(*args, **kwargs)
  title = forms.CharField(required=True, max_length=50)
  mooddate = forms.TimeField(required=False, initial=format(datetime.datetime.now().time(), '%H:%M'),
                                  widget=forms.DateInput(attrs={'type': 'datetime-local'}), localize=True, label="Enter time of event")
  intext = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':80, 'rows':9}), label='')
  eventtype = forms.ChoiceField(choices=EVENT_CHOICES, required=True, label="Choose what kind of event do you register",
                                widget=forms.RadioSelect)
  moodtype = forms.ChoiceField(choices=NUM_CHOICES, required=True, label="Score mood you have(had)",
                                widget=forms.RadioSelect)

class Survey(forms.Form):
  quest1 = forms.ChoiceField(choices=NUM_CHOICES, required=True, label="Do you think you have many friends?",
                             widget=forms.RadioSelect)
  quest2 = forms.ChoiceField(choices=NUM_CHOICES, required=True, label="Do you feel happy after talking to your comrade?",
                             widget=forms.RadioSelect)
  quest3 = forms.ChoiceField(choices=NUM_CHOICES, required=True, label="Do you feel bored being alone for a long time?",
                             widget=forms.RadioSelect)
  quest4 = forms.ChoiceField(choices=NUM_CHOICES, required=True, label="Do you think you better then others?",
                             widget=forms.RadioSelect)
  quest5 = forms.ChoiceField(choices=NUM_CHOICES, required=True, label="Do you think you spend more time to work than to your social life?",
                             widget=forms.RadioSelect)