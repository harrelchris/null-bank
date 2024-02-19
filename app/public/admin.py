from django.contrib import admin

from public.models import Contact, Question


class AnonymousFilter(admin.SimpleListFilter):
    title = "User Type"
    parameter_name = "anonymous"

    def lookups(self, request, model_admin):
        return (
            ("True", "Anonymous"),
            ("False", "Registered"),
        )

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(user__isnull=True)
        elif self.value() == "False":
            return queryset.filter(user__isnull=False)


class ContactAdmin(admin.ModelAdmin):
    actions = ("mark_resolved", "mark_unresolved")
    list_display = ("email", "user", "message", "resolved")
    list_display_links = ("email", "user", "message")
    list_editable = ("resolved",)
    list_filter = ("resolved", AnonymousFilter, "user__is_staff", "user__is_active")
    ordering = ("-created_at",)
    search_fields = ("email", "user", "message")

    def mark_resolved(self, request, queryset):
        queryset.update(resolved=True)

    def mark_unresolved(self, request, queryset):
        queryset.update(resolved=False)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "answer")


admin.site.register(Contact, ContactAdmin)
admin.site.register(Question, QuestionAdmin)
