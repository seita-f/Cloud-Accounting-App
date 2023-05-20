from collections import OrderedDict

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

# Date for expense_cost_past_month function
from datetime import datetime, timedelta

def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


# summary per_year_month for the total mount spend
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


def expense_cost_past_month(queryset):
    result_dict = {}  # 空の辞書を作成

    # 過去30日間の開始日を計算
    start_date = datetime.now().date() - timedelta(days=30)

    # 過去30日間のExpenseを取得し、日付別に集計
    for expense in queryset.filter(date__gte=start_date):
        date = expense.date  # Expenseの日付を取得
        if date not in result_dict:
            result_dict[date] = 0  # 金額の初期化
        result_dict[date] += expense.amount  # 金額を追加

    result_dict = OrderedDict(reversed(list(result_dict.items())))

    return result_dict

