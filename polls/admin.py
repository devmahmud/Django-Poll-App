from django.contrib import admin
from .models import Poll, Choice, Vote, Category

class ChoiceInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = Choice
    extra = 1

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ["text", "owner", "category", "pub_date", "active", "created_at"]
    search_fields = ["text", "owner__username", "category__name"]
    list_filter = ["active", 'created_at', 'pub_date', 'category']
    date_hierarchy = "pub_date"
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "poll", 'created_at', 'updated_at']
    search_fields = ["choice_text", "poll__text"]
    autocomplete_fields = ["poll"]

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["choice", "poll", "user", 'created_at']
    search_fields = ["choice__choice_text", "poll__text", "user__username"]
    autocomplete_fields = ["choice", "poll", "user"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]
