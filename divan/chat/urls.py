
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('user/<str:uid>/refresh', views.RefreshToken.as_view(), name='refresh'),
    path('user/<str:uid>/revoke', views.Signout.as_view(), name='revoke'),
    path('user/<str:uid>/profile', views.Profile.as_view(), name='profile'),
    path('user/<str:user1_id>/follow/<str:user2_id>',
         views.FriendRequest.as_view(), name='request'),
    path('user/<str:uid>/requests',
         views.FriendRequestView.as_view(), name='profile'),
    path('user/<str:uid>/requests/<int:request_id>/accept',
         views.AcceptRequest.as_view(), name='accept'),
    path('user/<str:uid>/requests/<int:request_id>/refuse',
         views.RefuseRequest.as_view(), name='refuse'),
    path('user/<str:user1_id>/create/conversation/<str:user2_id>',
         views.CreateCoversation.as_view(), name='create'),
    path('user/<str:uid>', views.ViewUsers.as_view(), name='view_user'),
    path('user/<str:user_id>/friends',
         views.ViewFriend.as_view(), name='view_friend'),
    path('user/<str:user_id>/conversation/<int:conversation_id>',
         views.CreateMessage.as_view(), name='send'),
    path('user/<str:user_id>/conversations',
         views.ViewConversations.as_view(), name='view_conver'),
    path('user/<str:user_id>/conversations/<int:conversation_id>',
         views.ViewConversationMessage.as_view(), name='view_message_conver')

]
