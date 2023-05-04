from collections import OrderedDict

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


# summary per_year_month for the total mount spend (I don't know what else to add)
def summary_per_year_month(queryset):
    result_dict = {}  # empty dict
    for expense in queryset:
        month_year = expense.date.strftime('%b-%Y')  # Month-Year (Ex: Feb-2021)
        if month_year not in result_dict:
            result_dict[month_year] = 0              # initialize the amount
        result_dict[month_year] += expense.amount    # add amount spend

    # update a dictionary with reversed key-value pairs => => ascending
    result_dict = OrderedDict(reversed(list(result_dict.items())))
    return result_dict


