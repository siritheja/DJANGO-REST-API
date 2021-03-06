from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('hello-viewsets',views.HelloViewSets, base_name = 'hello-viewsets')
router.register('profiles',views.UserProfileViewset)
router.register('feed',views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/',views.HelloApiView.as_view()),
    path('login/',views.UserLoginApiView.as_view()),
    path('',include(router.urls)), # to run this add just localhost/api
]