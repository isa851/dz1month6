from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Product,
    Category,
    Models,
    ProductImage,
    Favorite,
    Cart,
    CartItem,
    Order,
    OrderItem
)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)



@admin.register(Models)
class ModelsAdmin(admin.ModelAdmin):
    list_display = ("title", "category")
    search_fields = ("title",)
    list_filter = ("category",)



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price",
        "category",
        "model",
        "size",
        "is_active",
        "created_at",
    )
    search_fields = ("title", "description")
    list_filter = ("category", "model", "is_active", "created_at")
    list_editable = ("is_active",)
    readonly_fields = ("uuid", "created_at")
    inlines = [ProductImageInline]



@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image_preview")
    search_fields = ("product__title",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="70" style="border-radius:6px;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Превью"



@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")
    search_fields = ("user__email", "product__title")
    list_filter = ("created_at",)



class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    inlines = [CartItemInline]



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "manager_by",
        "courier",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("user__email", "address", "phone")
    readonly_fields = ("created_at",)
    inlines = [OrderItemInline]



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "price", "quantity")