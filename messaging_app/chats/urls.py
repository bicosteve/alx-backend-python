from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("/api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("/api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("/api", include(router.urls)),
    path("/api/message/<int:pk>/", include(router.urls)),
    path("/api/conversation/<int:pk>/", include(router.urls)),
]
