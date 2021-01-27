from django.shortcuts import render, redirect
from datetime import datetime as dt
from datetime import timedelta
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from Diary.forms import *
from Diary.models import *
from django.core.mail import send_mail
from background_task import background
import locale
from transliterate import translit
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot
import matplotlib.pyplot as plt
from django.template import loader

locale.setlocale(locale.LC_ALL, '')

class RegisterFormView(FormView):
    form_class = SignUpForm
    success_url = "login"
    template_name = "register.html"
    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        item = Profile(username=username, usermail=email)
        item.save()
        return super(RegisterFormView, self).form_valid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")

def MainPage(request):
    context = {}
    if request.method == "GET":
        context['frm'] = Survey()
    elif request.method == "POST":
        o = Survey(request.POST)
        q1 = int(o.data['quest1'])
        q2 = int(o.data['quest2'])
        q3 = int(o.data['quest3'])
        q4 = int(o.data['quest4'])
        q5 = int(o.data['quest5'])
        survscore = (q1+q2+q3+q4+q5)/5
        newres = SurveyResults(creatorname=request.user.username, score=survscore)
        newres.save()
        context['frm'] = o
    return render(request, "mainpage.html", context)

def profilesettings(request):
    context = {}
    if request.method == "GET":
        context['frm'] = ChangeEmail()
        current = Profile.objects.get(username = request.user.username)
        context['thisname'] = current.username
        context['thismail'] = current.usermail
        context['check'] = False
    elif request.method == "POST":
        o = ChangeEmail(request.POST)
        m = o.data['intext']
        current = Profile.objects.get(username=request.user.username)
        context['thisname'] = current.username
        send_mail('AdwancedWebDiary', current.username + ", your mail has been changed. \nYour new mail: " + m + ". \nYou can change it any time in your profile settings", 'KirillM281@gmail.com', [current.usermail], fail_silently=False)
        send_mail('AdwancedWebDiary', "This email address has been added as your new email in AdvancedWebDiary. \nIf you haven't done that or you don't have an accont in AdwancedWebDiary, click the link below \n \n" + "http://127.0.0.1:8000/reverse?user=" + current.username, 'KirillM281@gmail.com', [m], fail_silently=False)
        current.oldmail = current.usermail
        current.usermail = m
        current.save()
        context['thismail'] = current.usermail
        context['check'] = True
        context['frm'] = o
    return render(request, "profile.html", context)

def revmail(request):
    chosen = request.GET.get('user')
    item = Profile.objects.get(username=chosen)
    if item.oldmail != None:
        item.usermail = item.oldmail
        item.oldmail = None
        item.save()
    return HttpResponseRedirect("/")



def makenewbignote(request):
    context = {}
    if request.method == "GET":
        context['frm'] = MakeBigNote()
    elif request.method == "POST":
        o = MakeBigNote(request.POST)
        title = o.data['title']
        text = o.data['intext']
        newnote = BigNote(creatorname=request.user.username, title=title, notetext=text)
        newnote.save()
        context['frm'] = o
        return HttpResponseRedirect("bignotelist")
    return render(request, "newbignote.html", context)

def viewbignotes(request):
    context = {}
    context['notes'] = BigNote.objects.filter(creatorname = request.user.username)
    if request.method == 'POST':
        o = UploadFile(request.POST, request.FILES)
        if o.is_valid():
            f = request.FILES['file']
            f.seek(0)
            ntxt = f.read().decode('utf8')
            titl = o.data['name']
            newnote = BigNote(creatorname=request.user.username, title=titl, notetext=ntxt)
            newnote.save()
            return HttpResponseRedirect("bignotelist")
    else:
        context['frm'] = UploadFile()
    return render(request, "viewbignotes.html", context)

def redactbignotes(request):
    context = {}
    context['notes'] = BigNote.objects.filter(creatorname = request.user.username)
    return render(request, "redactbignotes.html", context)

def deletebignotes(request):
    current = BigNote.objects.filter(creatorname = request.user.username)
    current.delete()
    return HttpResponseRedirect("bignotelistred")

def viewbignote(request):
    context = {}
    chosen = request.GET.get('notetitle')
    item = BigNote.objects.get(title = chosen)
    context['title'] = str(item.title)
    context['text'] = str(item.notetext)
    return render(request, "viewbignote.html", context)

def redactbignote(request):
    context = {}
    chosen = request.GET.get('notetitle')
    item = BigNote.objects.get(title=chosen)
    context['title'] = str(item.title)
    if request.method == "GET":
        context['frm'] = RedactBigNote(initial = {'intext': str(item.notetext)})
    elif request.method == "POST":
        o = RedactBigNote(request.POST)
        text = o.data['intext']
        item.notetext = text
        item.save()
        context['frm'] = o
        return HttpResponseRedirect("bignoteview?notetitle="+str(item.title))
    return render(request, "redactbignote.html", context)

def deletebignote(request):
    chosen = request.GET.get('notetitle')
    item = BigNote.objects.get(title = chosen)
    item.delete()
    return HttpResponseRedirect("bignotelistred")


@background(schedule=60)
def littlenotenotify(nusername, ntitle, nmail):
    send_mail('AdwancedWebDiary',
              nusername + ", you have set a notification on this time to the note called " + ntitle + "\nYou may check this note using the link below\n" + "http://127.0.0.1:8000/littlenoteview?notetitle=" + ntitle,
              'KirillM281@gmail.com', [nmail], fail_silently=False)

def makenewlittlenote(request):
    context = {}
    if request.method == "GET":
        context['frm'] = MakeLittleNote()
    elif request.method == "POST":
        o = MakeLittleNote(request.POST)
        title = o.data['title']
        text = o.data['intext']
        isnot = o.data['isnotify']
        ndate = None
        if isnot == 'True':
            ndate = (dt.strptime(o.data['notifydate'], '%Y-%m-%d %H:%M')+timedelta(hours=3))
            timeleft = ndate - dt.now() - timedelta(hours=3)
            currentprof = Profile.objects.get(username=request.user.username)
            littlenotenotify(request.user.username, title, currentprof.usermail, schedule=timeleft)
        newnote = LittleNote(creatorname=request.user.username, title=title, notetext=text, notifydate=ndate)
        newnote.save()
        context['frm'] = o
        return HttpResponseRedirect("littlenotelist")
    return render(request, "newlittlenote.html", context)

def viewlittlenotes(request):
    context = {}
    context['notes'] = LittleNote.objects.filter(creatorname = request.user.username)
    if request.method == 'POST':
        o = UploadFile(request.POST, request.FILES)
        if o.is_valid():
            f = request.FILES['file']
            f.seek(0)
            ntxt = f.read().decode('utf8')
            titl = o.data['name']
            newnote = LittleNote(creatorname=request.user.username, title=titl, notetext=ntxt)
            newnote.save()
            return HttpResponseRedirect("littlenotelist")
    else:
        context['frm'] = UploadFile()
    return render(request, "viewlittlenotes.html", context)

def redactlittlenotes(request):
    context = {}
    context['notes'] = LittleNote.objects.filter(creatorname = request.user.username)
    return render(request, "redactlittlenotes.html", context)

def deletelittlenotes(request):
    current = LittleNote.objects.filter(creatorname = request.user.username)
    current.delete()
    return HttpResponseRedirect("littlenotelistred")

def viewlittlenote(request):
    context = {}
    chosen = request.GET.get('notetitle')
    item = LittleNote.objects.get(title = chosen)
    context['title'] = str(item.title)
    context['text'] = str(item.notetext)
    if item.notifydate == None:
        context['isnoty'] = False
    else:
        context['isnoty'] = True
        context['notifydate'] = dt.strftime(item.notifydate, '%d.%m.%Y %H:%M')
    return render(request, "viewlittlenote.html", context)

def redactlittlenote(request):
    context = {}
    chosen = request.GET.get('notetitle')
    item = LittleNote.objects.get(title=chosen)
    context['title'] = str(item.title)
    if item.notifydate == None:
        context['isnoty'] = False
    else:
        context['isnoty'] = True
        context['notifydate'] = dt.strftime(item.notifydate, '%d.%m.%Y %H:%M')
    if request.method == "GET":
        context['frm'] = RedactLittleNote(initial={'intext': str(item.notetext)})
    elif request.method == "POST":
        o = RedactLittleNote(request.POST)
        text = o.data['intext']
        item.notetext = text
        item.save()
        context['frm'] = o
        return HttpResponseRedirect("littlenoteview?notetitle=" + str(item.title))
    return render(request, "redactlittlenote.html", context)

def deletelittlenote(request):
    chosen = request.GET.get('notetitle')
    item = LittleNote.objects.get(title = chosen)
    item.delete()
    return HttpResponseRedirect("littlenotelistred")

def importlittlenote(request):
    chosen = request.GET.get('notetitle')
    item = LittleNote.objects.get(title=chosen)
    filename = str(item.title) + ".txt"
    content = str(item.notetext)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(translit(filename, "ru", reversed=True))
    return response

def importbignote(request):
    chosen = request.GET.get('notetitle')
    item = BigNote.objects.get(title=chosen)
    filename = str(item.title) + ".txt"
    content = str(item.notetext)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(translit(filename, "ru", reversed=True))
    return response

def makeneweventnote(request):
    context = {}
    if request.method == "GET":
        context['frm'] = MakeEventNote()
    elif request.method == "POST":
        o = MakeEventNote(request.POST, request.FILES)
        f = None
        evtype = o.data['eventtype']
        text = o.data['intext']
        isphoto = o.data['isphoto']
        if isphoto == 'True':
            f = request.FILES['image']
        ndate = dt.strptime(str(dt.now().date()) + " " + o.data['eventdate'], '%Y-%m-%d %H:%M')
        newnote = EventNote(creatorname=request.user.username, eventdate=ndate, notetext=text, eventtype=evtype, eventimage=f, isaddphoto=isphoto)
        newnote.save()
        context['frm'] = o
        return HttpResponseRedirect("eventnotelist")
    return render(request, "neweventnote.html", context)

def vieweventnotes(request):
    context = {}
    context['notes'] = EventNote.objects.filter(creatorname = request.user.username)
    return render(request, "vieweventnotes.html", context)

def vieweventnote(request):
    context = {}
    chosen = request.GET.get('eventdate')
    item = EventNote.objects.get(eventdate = dt.strptime(chosen, '%d %B %Y г. %H:%M'))
    context['eventdate'] = item.eventdate
    context['text'] = str(item.notetext)
    context['eventtype'] = str(item.eventtype)
    context['isphoto'] = item.isaddphoto
    if item.isaddphoto == 'True':
        context['eventimage'] = item.eventimage
    return render(request, "vieweventnote.html", context)

def redacteventnotes(request):
    context = {}
    context['notes'] = EventNote.objects.filter(creatorname = request.user.username)
    return render(request, "redacteventnotes.html", context)

def deleteeventnotes(request):
    current = EventNote.objects.filter(creatorname = request.user.username)
    current.delete()
    return HttpResponseRedirect("eventnotelistred")

def redacteventnote(request):
    context = {}
    chosen = request.GET.get('eventdate')
    item = EventNote.objects.get(eventdate=dt.strptime(chosen, '%d %B %Y г. %H:%M'))
    context['eventdate'] = item.eventdate
    if request.method == "GET":
        context['frm'] = RedactEventNote(initial={'intext': str(item.notetext)})
    elif request.method == "POST":
        o = RedactEventNote(request.POST)
        text = o.data['intext']
        evtype = o.data['eventtype']
        item.notetext = text
        item.eventtype = evtype
        item.save()
        context['frm'] = o
        return HttpResponseRedirect("eventnoteview?eventdate=" + dt.strftime(item.eventdate + timedelta(hours=3), '%d %B %Y г. %H:%M'))
    return render(request, "redacteventnote.html", context)

def deleteeventnote(request):
    chosen = request.GET.get('eventdate')
    item = EventNote.objects.get(eventdate=dt.strptime(chosen, '%d %B %Y г. %H:%M'))
    item.delete()
    return HttpResponseRedirect("eventnotelistred")

def makenewmoodnote(request):
    context = {}
    if request.method == "GET":
        context['frm'] = MakeMoodNote()
    elif request.method == "POST":
        o = MakeMoodNote(request.POST)
        titl = o.data['title']
        evtype = o.data['eventtype']
        mdtype = int(o.data['moodtype'])
        text = o.data['intext']
        ndate = dt.strptime(str(dt.now().date()) + " " + o.data['mooddate'], '%Y-%m-%d %H:%M')
        newnote = MoodNote(creatorname=request.user.username, title=titl, mooddate=ndate, notetext=text, eventtype=evtype, moodtype=mdtype)
        newnote.save()
        context['frm'] = o
        return HttpResponseRedirect("moodnotelist")
    return render(request, "newmoodnote.html", context)

def viewmoodnotes(request):
    context = {}
    context['notes'] = MoodNote.objects.filter(creatorname = request.user.username)
    return render(request, "viewmoodnotes.html", context)

def viewmoodnote(request):
    context = {}
    chosen = request.GET.get('notetitle')
    item = MoodNote.objects.get(title=chosen)
    context['title'] = str(item.title)
    context['text'] = str(item.notetext)
    context['eventtype'] = str(item.eventtype)
    context['moodtype'] = str(item.moodtype)
    return render(request, "viewmoodnote.html", context)

def deletemoodnotes(request):
    current = MoodNote.objects.filter(creatorname = request.user.username)
    current.delete()
    return HttpResponseRedirect("moodnotelist")

def showstats(request):
    mdevindtmp = []
    mdevind = []
    mdevval = []
    mdtype = []
    mdtime = []
    srtime = []
    srscore = []
    mdnotes = MoodNote.objects.filter(creatorname = request.user.username)
    for md in mdnotes:
        mdevindtmp.append(md.eventtype)
    mdevindtmp = set(mdevindtmp)
    for n in mdevindtmp:
        mdevind.append(n)
        tmp = MoodNote.objects.filter(creatorname = request.user.username).filter(eventtype = n)
        mdevval.append(sum([int(i.moodtype) for i in tmp])/len(tmp))
    for md in mdnotes:
        mdtype.append(md.eventtype)
        mdtime.append(md.mooddate)
    sures = SurveyResults.objects.filter(creatorname = request.user.username)
    for sr in sures:
        srscore.append(sr.score)
        srtime.append(sr.creationdate)
    f = plt.figure(figsize=(16, 7))
    plt.subplot(131)
    plt.bar(mdevind, mdevval)
    plt.title("Mood-event stat")
    plt.subplot(132)
    plt.plot(srtime, srscore)
    plt.title("Communication-time stat")
    plt.subplot(133)
    plt.plot(mdtime, mdtype)
    plt.title("Mood-time stat")
    canvas = FigureCanvasAgg(f)
    resp = HttpResponse(content_type='image/png')
    canvas.print_png(resp)
    plt.close(f)
    return resp

def rendstats(request):
    return render(request, "statistics.html")