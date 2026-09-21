from django.urls import path
from . import views

urlpatterns = [
    path("api/orders/<int:order_id>/recommend-box/", views.recommend_box_view),
    path(
        "orders/<int:order_id>/recommend/",
        views.recommend_box_page,
        name="recommend_box",
    ),
]
