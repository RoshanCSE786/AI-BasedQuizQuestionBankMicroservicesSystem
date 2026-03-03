from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = router.urls 