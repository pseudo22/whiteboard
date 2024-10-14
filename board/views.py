from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView

from .forms import UserRegistrationForm
from .models import Room, Drawing
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin



class RoomCreationView(LoginRequiredMixin ,View ):
    template_name = 'board/room_create.html'
    login_url = 'login/'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        room_name = request.POST.get('room_name')

        if not request.user.is_authenticated:
            return redirect('room_create')
        

        room= Room.objects.get_or_create(name=room_name, defaults={'created_by': request.user})
        
        return redirect('board_with_chat', room_name=room_name)



from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Room, Drawing, ChatMessage
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


class BoardWithChatView(LoginRequiredMixin, TemplateView):
    template_name = 'board/whiteboard.html'
    login_url = 'login/'

    def get(self, request, *args, **kwargs):
        room_name = kwargs.get('room_name')
        room = get_object_or_404(Room, name=room_name)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_name = self.kwargs['room_name']

        context['room_name'] = room_name
        context['messages'] = ChatMessage.objects.filter(room__name=room_name).values('user__username', 'message', 'timestamp')
        context['user'] = self.request.user

        return context

from django.views import View
from django.http import JsonResponse
from .models import Room, ChatMessage

class SendMessageView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        room_name = kwargs.get('room_name')
        room = get_object_or_404(Room, name=room_name)

        content = request.POST.get('message')
        if content:
            ChatMessage.objects.create(room=room, user=request.user, content=content)
        
        return redirect('board_with_chat', room_name=room_name)


from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

class LoginView(View):
    template_name = 'board/login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('room_create')
        return render(request, self.template_name, {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login') 
    

from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully! You can now login.')
            return redirect('login') 
    else:
        form = UserRegistrationForm()
    return render(request, 'board/register.html', {'form': form})






