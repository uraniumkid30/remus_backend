from django.contrib import admin
from . import models
from conf.core.admin import CustomAdmin
from conf.core.utils import get_user_profile


class ProductAdmin(CustomAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "point",
        "sub_category",
        "unit_price",
        "wait_time",
        "status",
        "created_at",
    ]
    list_filter = ("sub_category",)
    search_fields = ["name"]
    autocomplete_fields = [
        "sub_category",
    ]

    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(sub_category__restaurant__workers=user_profile)
        else:
            return qs.none()


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)

    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(restaurant__workers=user_profile)
        else:
            return qs.none()


class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("category",)

    def get_queryset(self, request):
        qs = super(SubCategoryAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(restaurant__workers=user_profile)
        else:
            return qs.none()


class ProductStockAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(ProductStockAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(product__sub_category__restaurant__workers=user_profile)
        else:
            return qs.none()


class IngredientAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(IngredientAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(restaurant__workers=user_profile)
        else:
            return qs.none()


admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.SubCategory, SubCategoryAdmin)
admin.site.register(models.ProductStock, ProductStockAdmin)
