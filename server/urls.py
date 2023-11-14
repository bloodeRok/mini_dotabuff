from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("games/", include("backend.urls.game_urls")),
    path("telegram-profiles/", include("backend.urls.telegram_profile_urls")),
    path("heroes/", include("backend.urls.hero_urls")),
]
