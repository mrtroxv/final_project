
from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('refresh/', views.RefreshToken.as_view(), name='refresh'),
    path('revoke/<str:uid>', views.Signout.as_view(), name='revoke'),
    path('user/<str:uid>/profile', views.Profile.as_view(), name='profile'),
    path('user/<str:user_id>/follow/<str:friend_id>',
         views.FriendRequest.as_view(), name='request'),
    path('user/<str:uid>/requests', views.RequestView.as_view(), name='profile'),
    path('user/requests/<int:request_id>/accept',
         views.AcceptRequest.as_view(), name='accept'),
    path('user/requests/<int:request_id>/refuse',
         views.RefuseRequest.as_view(), name='refuse'),
    path('user/<str:user1_id>/create/conversation/<str:user2_id>',
         views.CreateCoversation.as_view(), name='create'),
    path('user/', views.ViewUser.as_view(), name='view_user'),
    path('user/<str:user_id>/friends',
         views.ViewFriend.as_view(), name='view_friend'),
    path('user/<str:user_id>/conversation/<int:conversation_id>',
         views.CreateMessage.as_view(), name='send'),
    path('user/<user_id>/conversations',
         views.ViewConversation.as_view(), name='view_conver'),
    path('user/conversation/<int:conversation_id>',
         views.ViewConversationMessage.as_view(), name='view_message_conver')

]
