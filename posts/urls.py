from django.urls import path
from . import views

urlpatterns = [
    path(route='', view=views.PostFeedView.as_view(), name='feed'),
    path(route='posts/new/', view=views.CreatePostView.as_view(), name='create'),
    path(route='posts/<int:pk>/', view=views.PostDetailView.as_view(), name='detail'),
    path(route='posts/delete/<int:pk>/', view=views.delete_post, name="delete"),
]
