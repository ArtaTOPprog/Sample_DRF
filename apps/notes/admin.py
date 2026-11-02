from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "is_pinned", "is_archived", "created_at", "updated_at")
    list_display_links = ("id", "title")
    list_filter = ("is_pinned", "is_archived", "created_at")
    list_editable = ("is_pinned", "is_archived")
    search_fields = ("title", "content", "owner__username", "owner__email")
    list_select_related = ("owner",)
    autocomplete_fields = ("owner",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": ("owner", "title", "content")}),
        ("Статус", {"fields": ("is_pinned", "is_archived")}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
