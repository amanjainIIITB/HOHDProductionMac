from django.db.models import Sum
import datetime
from customer.models import ClientVisit


def get_total_online_amount_of_the_month(shop_id, month, year):
    bardate = datetime.date(day=1, month=month, year=year).strftime('%Y-%m-%d')
    total_online_amount_of_the_month = ClientVisit.objects.filter(payment_mode='online', ShopID=shop_id, bardate=bardate).aggregate(Sum('amount'))
    if total_online_amount_of_the_month['amount__sum'] is None:
        return 0
    return total_online_amount_of_the_month['amount__sum']


def get_total_cash_amount_of_the_month(shop_id, month, year):
    bardate = datetime.date(day=1, month=month, year=year).strftime('%Y-%m-%d')
    total_cash_amount_of_the_month = ClientVisit.objects.filter(payment_mode='cash', ShopID=shop_id, bardate=bardate).aggregate(Sum('amount'))
    if total_cash_amount_of_the_month['amount__sum'] is None:
        return 0
    else:
        return total_cash_amount_of_the_month['amount__sum']