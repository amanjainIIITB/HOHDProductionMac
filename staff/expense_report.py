from .views import get_month_year_month_name_for_download
from .analysis import get_total_online_amount_of_the_month
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Expense


def get_all_expense_of_the_month(shop_id, month, year, total_online_amount_Of_The_Month):
    print('I am in all expense')
    if int(month) <= 9:
        month = '0' + str(month)
    expense = Expense.objects.filter(shopID=shop_id,
                                     date__contains=str(year) + "-" + str(month)).order_by('date')
    expense_list = []
    remaining_amount = total_online_amount_Of_The_Month
    print(expense)
    for expenseobj in expense:
        remaining_amount = remaining_amount + expenseobj.amount
        expense_list.append(
            [expenseobj.date, expenseobj.purpose, expenseobj.comment, expenseobj.paymentmode, expenseobj.amount])
    expense_list.append(['', 'Remaining Amount', 'Profit', '', remaining_amount])
    return expense_list


class ExpenseReport(APIView):
    def get(self):
        pass

    def post(self, request):
        print('im in expense')
        month = request.data['month']
        print('year')
        year = request.data['year']
        print('before total amount')
        total_online_amount_of_the_month = get_total_online_amount_of_the_month(request.data['shop_id'], month, year)
        print('after total amount', total_online_amount_of_the_month)
        month_year_month_name = get_month_year_month_name_for_download()
        return Response({'expense': get_all_expense_of_the_month(request.data['shop_id'], month, year,
                                                                 total_online_amount_of_the_month),
                         'total_online_amount_Of_The_Month': total_online_amount_of_the_month,
                         "month_list": month_year_month_name[0], "year_list": month_year_month_name[2],
                         "month_name": month_year_month_name[1]})