from django.urls import path
from .views import (
    CategoryGroupList,
    CategoryGroupDetail,
    CategoryGroupCreate,
    CategoryList,
    CategoryDetail,
    CategoryCreate,
    CategoriesByGroup,
)

urlpatterns = [
    path("groups/", CategoryGroupList.as_view(), name="category-group-list"),
    path("groups/create/", CategoryGroupCreate.as_view(), name="category-group-create"),
    path(
        "groups/<int:pk>/", CategoryGroupDetail.as_view(), name="category-group-detail"
    ),
    path("", CategoryList.as_view(), name="category-list"),
    path("create/", CategoryCreate.as_view(), name="category-create"),
    path("<int:pk>/", CategoryDetail.as_view(), name="category-detail"),
    path(
        "group/<int:group_id>/", CategoriesByGroup.as_view(), name="categories-by-group"
    ),
]
