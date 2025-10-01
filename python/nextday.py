import datetime
now = input().strip()
next_time = datetime.datetime.strptime(now, '%d/%m/%Y') + datetime.timedelta(days=1)
day = str(next_time.day)
month = str(next_time.month)
year = str(next_time.year)
print(f"{day}/{month}/{year}")