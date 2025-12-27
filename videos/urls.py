from django.urls import path
from . import views

urlpatterns = [
    path("", views.video_list, name="video_list"),
    path("upload/", views.upload_video, name="upload_video"),
    path("watch:<uuid:video_id>/", views.watch_video, name="watch_video"),
    path("keys/<str:asset_id>/", views.serve_key, name="serve_key"),
]
