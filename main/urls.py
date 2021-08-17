from django.urls import path
from .views import *

app_name = "main"
urlpatterns=[
    path('',showmain,name="index"),
    path('like',like, name = "like"),
    path('experience',experience, name = "experience"),
    path('<str:id>',detail, name = "detail"),
    path('new/',new, name = "new"),
    path('create/',create, name = "create"),
    path('edit/<str:id>', edit, name="edit"),
    path('posts/', posts, name="posts"),
    path('update/<str:id>',update,name = "update"),
    path('delete/<str:id>',delete,name = "delete"),
    path('<str:post_id>/create_comment', create_comment, name="create_comment"),
    path('delete_comment/<str:post_id>/<str:comment_id>',delete_comment,name="delete_comment"),
    path('update_comment/<str:post_id>/<str:comment_id>',update_comment,name="update_comment"),
    path('like_toggle/<int:post_id>/',like_toggle,name="like_toggle"),
    path('dislike_toggle/<int:post_id>/',dislike_toggle,name="dislike_toggle"),
    ]