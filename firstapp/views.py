from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from . import models
from .models import Room,Topic,Message
# Create your views here.
from django.http import HttpResponse
from .forms import RoomForm
from django.db.models import Q #is it used to add and or operator in filter methods for multiple fliltering 
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required  #it is used to add restricted pages based on whether user is loggin in if user is loggin in he can acces the pages 
from django.contrib.auth.forms import UserCreationForm

def loginform(request):
    page='login' 
    if request.user.is_authenticated:
      return redirect('home')

    if request.method == 'POST':
        userr=request.POST.get('username')
        pas=request.POST.get('password')

        try:
            user=User.objects.get(username=userr)
        
        except:
            messages.error(request, "user does not exist")


        userra=authenticate(request,username=userr,password=pas)

        if userra is not None:
          login(request,userra)
          return redirect('home')
        

    return render(request,'firstapp/login-register.html',{'paage':page})

def logoutuser(request):
    logout(request)
    return redirect('loginform')


def registeruser(request):
    form1=UserCreationForm()
    if request.method == 'POST':
        form1=UserCreationForm(request.POST)
        if form1.is_valid():
            user= form1.save(commit=False)
            user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
    return render(request,'firstapp/login-register.html',{'form1':form1})

@login_required(login_url='loginform')
def home(request):
    q=request.GET.get('q')  if request.GET.get('q') else ''
    room=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) ) #icontains is used for filtering it see sub query words or query words like first one or two words and start filerting and startswith and endswith can also be used instead
    topicc=Topic.objects.all()
    rooms=Room.objects.count()
    mess=Message.objects.filter( Q(room__topic__name__icontains = q) | Q( room__name__icontains=q ) )
    context={"rooms":room,"topic":topicc,"rooms_count":rooms,'room_message':mess}
    return render(request,'home.html',context)



def userprofile(request,pk):
    user=User.objects.get(id=pk)
    room=user.room_set.all() #used to get child tables data here user is parent and Room model have many children.always use small letter for starting letter of model name.ex:for model Room we use room_set
    room_message=user.message_set.all()
    topic=Topic.objects.all()
    
    context={'user1':user, 'rooms':room,'room_message':room_message,'topic':topic}

    return render(request,'firstapp/profile.html',context)

def myname(request):
    return HttpResponse("this is myname  route that i have created")



def room(request):
 
    return render(request,'firstapp/room.html',) 


def showoneroom(request,pk):

    room=Room.objects.get(id=pk)
    roommessage=room.message_set.all()   #.order_by('-created') 
     #this is used to get to query or get children model,as example:room is parent and message model is child of rooom model we can query child data.as it gives all mesages with that particular room
    p=room.participants.all()

    if request.method == 'POST':
         mess=Message.objects.create(
             user=request.user,
             body=request.POST.get('body'),
             room=room
         )
         mess.save()
         room.participants.add(request.user)
         
         return redirect('showoneroom',pk=room.id )
    
    context={'room1':room,'roommessage':roommessage,'part':p}
        

    return render(request,'firstapp/showoneroom.html',context)



'''this is decorator that restiricts certain pages based on user is logged in  if log in he can acces pages else not. middleware can also be used but this is easy method '''
@login_required(login_url='loginform')
def createroom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    # if request.method == 'POST':
    #     form = RoomForm(request.POST)
    #     if form.is_valid():
    #         room =form.save(commit=False)
    #         room.host=request.user
    #         room.save()
    #         return redirect('home')

    if request.method == 'POST':
        topicname = request.POST.get('topic')
        roomname=request.POST.get('roomname')
        roomabout=request.POST.get('roomabout')
        a=Topic.objects.create(name=topicname).save()
        Room.objects.create(
            host=request.user,
            name=roomname,
            topic=a,
            description=roomabout,
        ).save()
        return redirect('home')

          
    context={'formm':form,topics:topics}
    return render(request,'firstapp/roomform.html',context)




@login_required(login_url='loginform')
def updateroom(request,pk):

    room=Room.objects.get(id=pk)
    
    if request.user!=room.host:
        return HttpResponse('you are noit allowd to do that!!!!')
    
    form1=RoomForm(instance=room)

    if(request.method == 'POST'):
        form1=RoomForm(request.POST,instance=room)
        if(form1.is_valid):
            form1.save()
            return redirect('home')
    context={'formm':form1}
    return render(request,'firstapp/roomform.html',context)


@login_required(login_url='loginform')
def deleteroom(request,pk):
    room=Room.objects.get(id=pk)

    if request.user!=room.host:
        return HttpResponse('you are noit allowd to do that!!!!')
    if(request.method=='POST'):
        room.delete()
        return redirect('home')
    return render(request,'firstapp/deleteform.html',{'obj':room})




@login_required(login_url='loginform')
def deletemessage(request,pk):
    mess=Message.objects.get(id=pk)

    if request.user!=mess.user:
        return HttpResponse('you are not allowd to do that!!!!')
    if(request.method=='POST'):
        mess.delete()
        return redirect('showoneroom',pk=mess.room.id)
    return render(request,'firstapp/deleteform.html',{'obj':mess})
    


