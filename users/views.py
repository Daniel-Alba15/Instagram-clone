from django import forms
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import DetailView, FormView, UpdateView
from django.contrib.auth.models import User
from .forms import ProfileForm, SingUpForm
from .models import Profile
from posts.models import Post


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')

        return context


"""
def sign_up(request):
    form = RawUserForm(request.POST or None)

    if form.is_valid(): 
            User.objects.create(**form.cleaned_data)

    context = {
        'form': form,
    }

    return render(request, 'users/sign_up.html', context)
"""


class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'


def log_in_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            # Se usa el nombre de la url definida en el archivo urls.py
            return redirect('posts:feed')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid user or password'})

    return render(request, 'users/login.html', {})


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    template_name = 'users/logout.html'


@login_required()
def log_out_view(request):
    logout(request)
    return redirect('users:login')


class SignupView(FormView):
    template_name = 'users/signup.html'
    form_class = SingUpForm
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error'] = self.get_form().errors

        return context

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)

    def form_invalid(self, form):

        return super().form_invalid(form)


def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')

    if request.method == 'POST':
        form = SingUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        else:
            return render(request, 'users/signup.html', {'error': form.errors})

    form = SingUpForm()

    return render(request, 'users/signup.html', {'form': form})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'bio', 'phone_number', 'picture']

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        username = self.object.user.username

        return reverse('users:detail', kwargs={'username': username})


@login_required()
def update_profile(request):
    form = ProfileForm()
    profile = request.user.profile
    if request.method == 'POST':
        # request.Files para pasar archivos
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            profile.website = data['website']
            profile.bio = data['bio']
            profile.phone_number = data['phone_number']
            profile.picture = data['picture']
            profile.save()

            # Como la url detail recibe como parametro el nombre de usuario
            # se pasa como kwargs y en forma de diccionario
            # Tambien se usa reverse para crear la url ya que redirect no la puede
            # crear como users:detail y el argumento que hay que pasarles
            url = reverse('users:detail', kwargs={
                          'username': request.user.username})
            return redirect(url)
        else:
            return render(request, 'users/update_profile.html', {'form': form})

    context = {
        'user': request.user,
        'profile': profile,
        'form': form,
    }

    return render(request, 'users/update_profile.html', context)


"""
def create_user(request):
    if request.method == 'POST':
        form = UserForm()
    context = { }
    return render(request, 'create_user.html', context)
"""


"""
def create_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = UserForm()

    context = {
        'form': form,
    }

    return render(request, 'create_user.html', context)
"""
