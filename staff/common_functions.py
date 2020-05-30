from django.db.models import Sum
import datetime
from customer.models import BharatPe, Paytm, client


def get_total_online_amount_of_the_month(shop_id, month, year):
    bardate = datetime.date(day=1, month=month, year=year).strftime('%Y-%m-%d')
    total_paytm_amount_of_the_month = Paytm.objects.filter(ShopID=shop_id, bardate=bardate).aggregate(Sum('amount'))
    total_bharatpe_amount_of_the_month = BharatPe.objects.filter(ShopID=shop_id, bardate=bardate).aggregate(
        Sum('amount'))
    if total_paytm_amount_of_the_month['amount__sum'] is None:
        total_paytm_amount_of_the_month['amount__sum'] = 0
    if total_bharatpe_amount_of_the_month['amount__sum'] is None:
        total_bharatpe_amount_of_the_month['amount__sum'] = 0
    total_online_amount_of_the_month = total_paytm_amount_of_the_month['amount__sum'] + \
                                       total_bharatpe_amount_of_the_month['amount__sum']
    return total_online_amount_of_the_month


def get_total_cash_amount_of_the_month(shop_id, month, year):
    bardate = datetime.date(day=1, month=month, year=year).strftime('%Y-%m-%d')
    total_cash_amount_of_the_month = client.objects.filter(ShopID=shop_id, bardate=bardate).aggregate(Sum('amount'))
    if total_cash_amount_of_the_month['amount__sum'] is None:
        return 0
    else:
        return total_cash_amount_of_the_month['amount__sum']