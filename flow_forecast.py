# -*- coding: utf-8 -*-
"""
version 1.1

Created on Wed Oct 19 10:35:17 2022

@author: user

Explain here what the code does:
    1.
    2.
    3.
    
    
References:
    


Issues: Load shedding
    
    
    
To Do:
    1. Add Xlookup started! not finished.
    


"""

import streamlit as st


st.write(""" # Flow Forecast
My first app """)

import requests


url = 'https://api.exchangerate.host/latest?base=USD&symbols=USD,ZMW,BWP,MZN,ZAR'
response = requests.get(url)
data = response.json()

# print(data['rates'])

BWP = data['rates']['BWP']
ZMW = data['rates']['ZMW']
MZN = data['rates']['MZN']
ZAR = data['rates']['ZAR']

#Assumptions

country = "Zambia" #Must 'toggle"

forex_rate = ZMW#15.537949 #Must be 'live'

zar_forex_rate = st.selectbox("Forex: ",
                     ['ZAR', 'ZMW', 'MZN', 'BWP'])

zar_forex_rate = data['rates'][string(zar_forex_rate)]

# zar_forex_rate = ZAR

facility_amount = 20_000_000

number_of_invoices = 20

bank_base_rate = .66 # was 0.36

bank_one_off_fee = st.text_input("Bank Fee", 0.015)

bank_one_off_fee = float(bank_one_off_fee)

# bank_one_off_fee = 0.015 # was 0

contingency_reserve = 0.2

suppliers_current_dpo = 30

extension_required_by_supplier = 30

tenor = suppliers_current_dpo + extension_required_by_supplier

bank_discount_applied = (bank_base_rate/365 + 1) ** tenor - 1 + bank_one_off_fee

flow_fee_monthly = 0.00675

total_Flow_fee = (1 + flow_fee_monthly * 12 /365) ** tenor -1

flow_fee_rate = 0.0164

invoice_commission_payment_accelerator = 3

sales_commisssion = 0.05

month_ratio = (tenor/365)*12

#Cash flow

monthly_disbursement_percentage_row_6 = [0.2, 0.2, 0.25, 0.3, 0.3, 0.5, 0.75, 0.75,1, 1,1,1]

list_of_ones = [1 for i in range(25)]

new_month = monthly_disbursement_percentage_row_6 + list_of_ones


total_amount_row_8 = []
first_payment_row_10 = []
second_payment_row_12 = []
second_payment = []
counter = 0

sec_payment_to_suppl_row_25 = []
flow_fee_payment_27 = []
supplier_net_sec_payment_row_26 = []
bank_fee_first_payment_row_21 = []

# Fixed, needs to be a formula
# sec_payment_month_14 = [2,3,4,5,6,7,8,9,10,11,12,13]
sec_payment_month_14 = []
month = []

# for 12 months
for i in range(37):
    # print(i)
    month.append(i)
    val = round((i + month_ratio))
    # print(val)
    sec_payment_month_14.append((val))

bank_monthly_cash_flow = []


print("Start for loop")

supplier_row_19 = []


for x in new_month:
       
    amount_to_be_paid_to_supplier = x * facility_amount# THIS IS WRONG!!!!!
    total_amount_row_8.append(amount_to_be_paid_to_supplier)
    second_payment_row_12.append(total_amount_row_8[-1]*0.2)
        
    bank_fee = amount_to_be_paid_to_supplier * bank_discount_applied
    
    # print(bank_fee) This works
    # first_payment_to_supplier = amount_to_be_paid_to_supplier * (1 - contingency_reserve) - bank_fee
    # first_payment_row_10.append(first_payment_to_supplier)
    
    first_payment_row_10.append(total_amount_row_8[-1]*(1-contingency_reserve))
    
    amount_recieved_from_buyer = amount_to_be_paid_to_supplier # delay for timing
    
    flow_fee = amount_to_be_paid_to_supplier * total_Flow_fee #delay timing
    # second_payment_to_supplier = amount_to_be_paid_to_supplier * contingency_reserve - flow_fee #delay timing
    # second_payment.append(second_payment_to_supplier)
    
    month_number_of_invoices = number_of_invoices * invoice_commission_payment_accelerator
    payment_accelerator_commission = invoice_commission_payment_accelerator * month_number_of_invoices * forex_rate
    
    monthly_sales_commisssion = flow_fee * sales_commisssion
    
    flow_monthly_gross_profit = flow_fee - payment_accelerator_commission - monthly_sales_commisssion
    
    usd_monthly_gross_profit = flow_monthly_gross_profit / forex_rate
    
    zar_monthly_gross_profit = usd_monthly_gross_profit * zar_forex_rate
    
    # print(f" counter = {counter} amnt: {total_amount_row_8[counter]} sec: {second_payment_row_12[counter]}" )
    
    if counter in sec_payment_month_14:
        # print(second_payment_row_12[counter])
        sec_payment_to_suppl_row_25.append(second_payment_row_12[counter-sec_payment_month_14[0]])
        flow_fee_payment_27.append(total_amount_row_8[counter-sec_payment_month_14[0]]*flow_fee_rate)
        supplier_net_sec_payment_row_26.append(sec_payment_to_suppl_row_25[-1] - flow_fee_payment_27[-1])
    else:
        # print("skipped")
        sec_payment_to_suppl_row_25.append(0)
        flow_fee_payment_27.append(0)
        supplier_net_sec_payment_row_26.append(0)
        
       
    bank_fee_first_payment_row_21.append(total_amount_row_8[-1]*bank_discount_applied)
    
    supplier_row_19.append(first_payment_row_10[-1] - bank_fee_first_payment_row_21[-1])
        
    # bank_monthly_cash_flow.append()
        
    
    # print(f"Month {counter}")
    # Counter = Month
    counter = counter + 1
    
    # print("Amount to be paid to supplier: ", amount_to_be_paid_to_supplier)
    # print("Bank fee: ", bank_fee)
    # print("First payment to supplier: ", first_payment_to_supplier)
    # print("Amount recieved from the buyer: ", amount_recieved_from_buyer)
    # print("Flow's fee: ", flow_fee)
    # print("Second payment to the supplier: ", second_payment_to_supplier)
    # print("Payment Accelerator commission: ", payment_accelerator_commission)
    # print("Monthly sales commisssion: ", monthly_sales_commisssion)
    # print("Flow's gross profit: ", flow_monthly_gross_profit)
    # print("USD monthly gross profit: ", usd_monthly_gross_profit)
    # print("SA monthly gross profit: ", zar_monthly_gross_profit)
    
    
   
import pandas as pd



forecast = {'Month' : month,
        'Percen' : new_month,
        'Total Amount' : total_amount_row_8,
        '1st Payment' : first_payment_row_10,
        '2nd Payment' : second_payment_row_12,
        '2nd Payment Month' : sec_payment_month_14,
        'Supplier' : supplier_row_19,
        'Bank Fee' : bank_fee_first_payment_row_21,
        '2nd Payment to Suppl' : sec_payment_to_suppl_row_25,
        'Supplier Net Sec Pay' : supplier_net_sec_payment_row_26,
        'Flow Fee' : flow_fee_payment_27}


pd.options.display.float_format = '{:.10f}'.format
df = pd.DataFrame(forecast)

df2 = df.transpose()

st.table(df2)


