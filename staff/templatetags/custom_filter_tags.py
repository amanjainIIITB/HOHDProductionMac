from django import template
from HOHDProductionMac.common_function import convert_date_yyyy_mm_dd_to_dd_mm_yyyy
import datetime

register = template.Library()

@register.filter
def getMonth(date):
    monthlist = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return monthlist[int(str(date).split('-')[1])-1]


@register.filter
def total_amount_of_the_day(date, datewisedata):
    i = 0
    flag = False
    while i < len(datewisedata):
        # print(date + " " + str(datewisedata[i].get('date')))
        if str(date) == str(datewisedata[i].get('date')):
            return datewisedata[i].get('Amount')
        i = i + 1
    if flag == False:
        return 0


@register.filter
def total_numberofcustomer_of_the_day(date, datewisedata):
    i = 0
    flag = False
    while i < len(datewisedata):
        # print(date + " " + str(datewisedata[i].get('date')))
        if str(date) == str(datewisedata[i].get('date')):
            return datewisedata[i].get('numberOfCustomer')
        i = i + 1
    if flag == False:
        return 0

@register.filter
def add(value1, value2):
    return int(value1)+int(value2)


@register.filter
def finalAmount(total_online, expense_list):
    amount_to_employees = total_online
    for obj in expense_list:
        amount_to_employees = amount_to_employees + obj[4]
    return amount_to_employees

@register.filter
def tag_convert_date_yyyy_mm_dd_to_dd_mm_yyyy(date):
    date_str = convert_date_yyyy_mm_dd_to_dd_mm_yyyy(date)
    format_str = '%d-%b-%Y'
    datetime_obj = datetime.datetime.strptime(date_str, format_str)
    return datetime_obj.date()

