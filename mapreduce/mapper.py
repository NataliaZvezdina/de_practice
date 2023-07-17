#!/usr/bin/env python

from datetime import datetime
import sys


for line in sys.stdin:
    data = line.strip().split(',')
    if len(data) == 18 and data[0] != 'VendorID':
        pickup_datetime = datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S')
        payment_type = data[9]
        tip_amount = float(data[13])

        if pickup_datetime.year == 2020 and payment_type and tip_amount >= 0:
            month = pickup_datetime.strftime('%Y-%m')
            print('{0},{1}\t{2}'.format(payment_type, month, tip_amount))
