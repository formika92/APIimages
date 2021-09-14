from rest_framework.routers import DefaultRouter

from pictures.views import ImageList

router = DefaultRouter()

router.register(r'images', ImageList,)
