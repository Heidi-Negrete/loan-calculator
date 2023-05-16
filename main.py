from math import ceil, log 
import argparse

parser = argparse.ArgumentParser(description='Loan Calculator: find differentiated or annuity monthly payment amount. You can also determine one of either loan principal, period for repayment, or interest  if you have payment amount.')
parser.add_argument('--periods', type=int, help='Enter the number of periods.')
parser.add_argument('--type', choices=['annuity', 'diff'], help='Enter whether payment type is annuity or differentiated')
parser.add_argument('--payment', type=float, help='Enter the annuity payment')
parser.add_argument('--interest', type=float, help='Enter the loan interest')
parser.add_argument('--principal', type=int, help='Enter the loan principal')
args = parser.parse_args()

def get_interest():
    # take annual interest percentage from user and convert to nominal interest rate
    try:
        if args.interest:
          return args.interest / 1200
    except:
        return args.interest


def get_usr_choice():
  if args.type == 'diff':
    # going to be calculating differential payment, and interest, periods, and principal must be given.abs
    if not args.periods or not args.interest or not args.principal:
      print('Incorrect parameters')
    else:
      if args.periods < 0 or args.interest < 0 or args.principal < 0:
        print('Incorrect parameters')
      else:
        calculate_diff_payment()
  elif args.type == 'annuity':
    # going to be calculating the payment. Check if all other arguments are provided.
    # whatever parameter is missing is the one we are looking for. error if we're missng more than one.
    if not args.principal:
      if args.payment and args.interest and args.periods:
        if args.payment < 0 or args.interest < 0 or args.periods < 0:
          print('Incorrect parameters')
        else:
          calculate_principal()
      else:
         print('Incorrect parameters')
    elif not args.payment:
      if args.principal and args.interest and args.periods:
        if args.principal < 0 or args.interest < 0 or args.periods < 0:
          print('Incorrect parameters')
        else:
          calculate_payment()
      else:
        print('Incorrect parameters')
    elif not args.periods:
      if args.principal and args.interest and args.payment:
        if args.principal < 0 or args.interest < 0 or args.payment < 0:
          print('Incorrect parameters')
        else:
          calculate_num_of_months()
      else:
        print('Incorrect parameters')
    else:
      print('Incorrect parameters')
  else:
    print('Incorrect parameters')
    

def calculate_num_of_months():
    # the period (num of months) = log(1 + i) * (payment / payment - i * P)
    # rewrite to say "It will take x years and 2 months to repay this loan!" (but no mention of years if n/a)
    interest = get_interest()
    months = ceil(log((args.payment / (args.payment - (interest * args.principal))), 1 + interest))
    total_months = months % 12
    years = months // 12
    if years > 0:
      if years == 1:
        if total_months == 1:
          print(f'It will take {years} year and {total_months:.0f} month to repay the loan')
        elif total_months == 0:
          print(f'It will take {years} year to repay the loan')
        else:
          print(f'It will take {years} year {total_months:.0f} months to repay the loan')
      else:
        if months == 1:
          print(f'It will take {years} years and {total_months:.0f} month to repay the loan')
        elif months == 0:
          print(f'It will take {years} years to repay the loan')
        else:
          print(f'It will take {years} years {total_months:.0f} months to repay the loan')
    else:
      if months == 1:
        print(f'It will take {months:.0f} month to repay the loan')
      else:
        print(f'It will take {months:.0f} months to repay the loan')
    print(f'Overpayment = {args.payment * months - args.principal}')

def calculate_payment():
    interest = get_interest()
    payment = ceil(args.principal * (interest * pow((1 + interest), args.periods)) / (pow((1 + interest), args.periods) - 1))
    print(f'Your monthly payment = {payment}!')

def calculate_diff_payment():
  interest = get_interest()
  total = 0
  for month in range(args.periods):
    payment = ceil((args.principal / args.periods) + interest * (args.principal - args.principal * (month) / args.periods))
    total += payment
    print(f'Month {month + 1}: payment is {payment}')
  print()
  print(f'Overpayment = {total - args.principal}')

def calculate_principal():
    interest = get_interest()
    principal = args.payment / ((interest * pow((1 + interest), args.periods)) / (pow((1 + interest), args.periods) - 1))
    print(f'Your loan principal = {principal}!')

# Main
get_usr_choice()