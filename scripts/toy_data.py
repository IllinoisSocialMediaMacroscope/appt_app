import numpy as np
from datetime import datetime, timedelta, date, time
import csv

#RUN FIRST, TO CREATE SHIFTS.CSV
#want: 2020-07-01 8am id_number(for locations: 0 == location 0)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


hours = [i for i in np.arange(8, 18.5, .5)]
change_hours = [str(int(i)) + ':00' if float.is_integer(i) else str(int(i)) + ':30' for i in hours]
make_time = [datetime.strptime(i, '%H:%M').strftime("%I:%M %p") for i in change_hours]

shifts = []
for i in range(1, 4):
	start_date = date(2020, 7, 6)
	end_date = date(2020, 12, 31)
	for single_date in daterange(start_date, end_date):
		for single_time in make_time:
			shifts.append((single_date.strftime("%Y-%m-%d"), single_time, i))

with open('shifts.csv', 'w', newline='') as f:
     writer = csv.writer(f, delimiter=',')
     writer.writerow(['date', 'time', 'location'])
     writer.writerows(shifts)



