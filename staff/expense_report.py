from rest_framework.views import APIView
from rest_framework.response import Response
from .views import get_month_year_month_name_for_download
from .common_functions import get_total_online_amount_of_the_month, get_total_cash_amount_of_the_month
from .models import Expense
from HOHDProductionMac.common_function import convert_date_dd_mm_yyyy_to_yyyy_mm_dd, convert_date_yyyy_mm_dd_to_dd_mm_yyyy
from datetime import date 


def expense_of_the_month(shop_id, month, year):
    if int(month) <= 9:
        month = '0' + str(month)
    expense = Expense.objects.values('ExpenseID', 'date', 'purpose', 'paymentmode', 'comment', 'amount').filter(shopID=shop_id, date__contains=str(year) + "-" + str(month)).order_by('date')
    # for expense_obj in expense:
        # if expense_obj['date'] is not None:
        #     expense_obj['date'] = convert_date_yyyy_mm_dd_to_dd_mm_yyyy(str(expense_obj['date']))
    # print('I am in expense')
    # print(expense)
    return expense


def profit_of_the_month(shop_id, month, year, total_online_amount_of_the_month,
                                 total_cash_amount_of_the_month):
    if int(month) <= 9:
        month = '0' + str(month)
    expense = Expense.objects.values('paymentmode', 'amount').filter(shopID=shop_id,
                                     date__contains=str(year) + "-" + str(month)).order_by('date')
    remaining_cash = total_cash_amount_of_the_month
    remaining_online = total_online_amount_of_the_month
    print('In the profit')
    print(expense)
    for expenseobj in expense:
        if expenseobj['paymentmode'] == 'Cash':
            remaining_cash = remaining_cash + expenseobj['amount']
        if expenseobj['paymentmode'] == 'Online':
            remaining_online = remaining_online + expenseobj['amount']
    remaining_balance = [['', 'Remaining Online', 'Profit', 'Online', remaining_online],
                         ['', 'Remaining Cash', 'Profit', 'Cash', remaining_cash],
                         ['', 'Remaining Amount', 'Profit', 'NA', remaining_cash + remaining_online]]
    return remaining_balance


class ExpenseReport(APIView):
    def get(self):
        pass

    def post(self, request):
        month = request.data['month']
        year = request.data['year']
        total_online_amount_of_the_month = get_total_online_amount_of_the_month(request.data['shop_id'], month, year)
        total_cash_amount_of_the_month = get_total_cash_amount_of_the_month(request.data['shop_id'], month, year)
        return Response({'current_date': date.today(),
                         'expense': expense_of_the_month(request.data['shop_id'], month, year),
                         'remaining_balance': profit_of_the_month(request.data['shop_id'], month, year,
                                                    total_online_amount_of_the_month,
                                                    total_cash_amount_of_the_month),
                         'total_online_amount_of_the_Month': total_online_amount_of_the_month,
                         'total_cash_amount_of_the_month': total_cash_amount_of_the_month,
                         'revenue': total_online_amount_of_the_month + total_cash_amount_of_the_month,
                         "month_year_month_name": get_month_year_month_name_for_download()})
