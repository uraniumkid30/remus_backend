from datetime import datetime

from django.contrib import admin
from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
    DateRangeQuickSelectListFilterBuilder,
)


class CustomAdmin:
    """
    autocomplete_fields fk m2m
    raw_id_fields fk m2m
    search_fields
    """

    date_hierarchy = "created_at"
    readonly_fields = ["deleted_at"]
    empty_value_display = "--"
    list_filter = (
        # ("created_at", DateRangeFilterBuilder()),
        (
            "updated_at",
            DateTimeRangeFilterBuilder(
                title="Custom title",
                default_start=datetime(2020, 1, 1),
                default_end=datetime(2030, 1, 1),
            ),
        ),
        # ("num_value", NumericRangeFilterBuilder()),
        (
            "created_at",
            DateRangeQuickSelectListFilterBuilder(),
        ),  # Range + QuickSelect Filter
    )


# class BookInline(admin.TabularInline):
#     model = Book
#     raw_id_fields = ["pages"]
#     def get_extra(self, request, obj=None, **kwargs):
#         extra = 2
#         if obj:
#             return extra - obj.binarytree_set.count()
#         return extra
#     def get_max_num(self, request, obj=None, **kwargs):
#         max_num = 10
#         if obj and obj.parent:
#             return max_num - 5
#         return max_num
# inlines =[]
# fieldsets = [
#         (
#             None,
#             {
#                 "fields": ["url", "title", "content", "sites"],
#             },
#         ),
#         (
#             "Advanced options",
#             {
#                 "classes": ["collapse"],# wide
#                 "fields": ["registration_required", "template_name"],
#             },
#         ),
#     ]
