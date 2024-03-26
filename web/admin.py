from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import Category, SubCategory, Product , ProductImage,OrderItem,Order,Slider

# Register your models here.
@admin.register(Slider)
class CategoryAdmin(ImportExportActionModelAdmin):
    list_display = ("title", "description", "background_image","is_active",)
    search_fields = ("title",)

@admin.register(Category)
class CategoryAdmin(ImportExportActionModelAdmin):
    list_display = ("title", "slug", "image",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}

@admin.register(SubCategory)
class SubCategoryAdmin(ImportExportActionModelAdmin):
    list_display = ("title", "slug", "category", "image","our_top_pics","is_home")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    inlines = (ProductImageInline,)
    list_display = ("name", "slug", "subcategory", "image", "sale_price","new_arrival","is_home")
    list_filter = ("subcategory", "new_arrival")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id','first_name',"payment_method"]
    list_filter = ['order_status','payment_status']
    inlines = [OrderItemInline]