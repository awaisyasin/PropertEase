from django.urls import path
from . import views

app_name = "propertease"

urlpatterns = [
    path("", views.home_view, name='home'),
    path("property-form/", views.property_form_view, name="property_form"),
    path("<int:profile_id>/", views.profile_view, name="profile"),
    path("<int:profile_id>/<int:property_id>/", views.property_detail_view, name="property_detail"),
    path("forum/", views.forum_view, name="forum"),
    path("forum/thread-form/", views.thread_form_view, name="thread_form"),
    path("forum/<int:thread_id>/", views.thread_detail_view, name="thread_detail"),
	path("<int:profile_id>/chat-endpoint/", views.chat_endpoint_view, name="chat_endpoint"),
    path("<int:profile_id>/chat/", views.chat_redirect_view, name="chat_redirect"),
    path("save_message/", views.save_message_view, name="save_message"),
	path('follow/<int:follower_id>/<int:followee_id>/', views.follow_user_view, name='follow_user'),
]
