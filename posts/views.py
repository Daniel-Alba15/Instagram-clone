from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .forms import PostForm, DeleteForm
from .models import Post


class PostFeedView(LoginRequiredMixin, ListView):
    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created', )
    context_object_name = 'posts'


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    context_object_name = 'post'


class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'posts/new.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile

        return context


@login_required()
def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        if request.user.id == post.user.id:
            form = DeleteForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['aceptar']:
                    post.delete()
                    url = reverse_lazy('users:detail', kwargs={
                                       'username': request.user.username})
                    return redirect(url)
        else:
            return render(request, 'posts/denied.html', {})

    form = DeleteForm()
    context = {
        'pk': pk,
        'profile': request.user.profile,
        'post': post,
        'form': form
    }

    return render(request, 'posts/delete.html', context)


"""
@login_required()
def list_posts(request):
    posts = Post.objects.all().order_by('-created')
    context = {
        'posts': posts,
        'user': request.user,
        'profile': request.user.profile
    }
    return render(request, 'posts/feed.html', context)
"""


@login_required()
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:feed')
        else:
            print(form.errors)

    form = PostForm()
    context = {
        'form': form,
        'user': request.user,
        'profile': request.user.profile
    }

    return render(request, 'posts/new.html', context)
