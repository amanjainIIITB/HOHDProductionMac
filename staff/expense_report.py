from rest_framework.views import APIView
from rest_framework.response import Response
from .views import get_month_year_month_name_for_download
from .common_functions import get_total_online_amount_of_the_month, get_total_cash_amount_of_the_month
from .models import Expense


def get_all_expense_of_the_month(shop_id, month, year, total_online_amount_of_the_month,
                                 total_cash_amount_of_the_month):
    if int(month) <= 9:
        month = '0' + str(month)
    expense = Expense.objects.filter(shopID=shop_id,
                                     date__contains=str(year) + "-" + str(month)).order_by('date')
    expenses = []
    remaining_cash = total_cash_amount_of_the_month
    remaining_online = total_online_amount_of_the_month
    print(expense)
    for expenseobj in expense:
        if expenseobj.paymentmode == 'Cash':
            remaining_cash = remaining_cash + expenseobj.amount
        if expenseobj.paymentmode == 'Online':
            remaining_online = remaining_online + expenseobj.amount
        expenses.append(
            [expenseobj.ExpenseID, expenseobj.date, expenseobj.purpose, expenseobj.comment, expenseobj.paymentmode, expenseobj.amount])
    remaining_balance = [['', 'Remaining Online', 'Profit', 'Online', remaining_online],
                         ['', 'Remaining Cash', 'Profit', 'Cash', remaining_cash],
                         ['', 'Remaining Amount', 'Profit', 'NA', remaining_cash + remaining_online]]
    return [expenses, remaining_balance]


class ExpenseReport(APIView):
    def get(self):
        pass

    def post(self, request):
        month = request.data['month']
        year = request.data['year']
        total_online_amount_of_the_month = get_total_online_amount_of_the_month(request.data['shop_id'], month, year)
        total_cash_amount_of_the_month = get_total_cash_amount_of_the_month(request.data['shop_id'], month, year)
        month_year_month_name = get_month_year_month_name_for_download()
        expense_list = get_all_expense_of_the_month(request.data['shop_id'], month, year,
                                                    total_online_amount_of_the_month,
                                                    total_cash_amount_of_the_month)
        return Response({'expense': expense_list[0],
                         'remaining_balance': expense_list[1],
                         'total_online_amount_of_the_Month': total_online_amount_of_the_month,
                         'total_cash_amount_of_the_month': total_cash_amount_of_the_month,
                         'revenue': total_online_amount_of_the_month + total_cash_amount_of_the_month,
                         "month_list": month_year_month_name[0], "year_list": month_year_month_name[2],
                         "month_name": month_year_month_name[1]})
