from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('', views.search_action, name='home'),
    # path('search', views.search_action, name='search'),
    # path('create', views.create_action, name='create'),
    # path('delete/<int:id>', views.delete_action, name='delete'),
    # path('edit/<int:id>', views.edit_action, name='edit'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('profile-edit', views.profile_edit, name='profile-edit'),
    path('follow/<int:user_id>', views.follow_action, name='follow'),
    path('unfollow/<int:user_id>', views.unfollow_action, name='unfollow'),
    # path('profile', views.profile_action, name='profile'),
    path('other-profile/<int:user_id>', views.other_profile_action, name='other-profile'),
    path('register', views.register_action, name='register'),
    path('global-stream', views.global_stream_action, name='global-stream'),
    path('follower-stream', views.follower_stream_action, name='follower-stream'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('get-global', views.get_global, name='get-global'),
    path('get-follower', views.get_follower, name='get-follower'),
    path('add-comment', views.add_comment, name='add-comment'),

]

