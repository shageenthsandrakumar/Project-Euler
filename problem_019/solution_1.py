from datetime import date,timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

start_dt = date(1901, 1, 1)
end_dt = date(2000, 12, 31)
count = 0
print(f"Dates between {start_dt} and {end_dt}:")
for dt in daterange(start_dt, end_dt):
    if not (dt.day-1+(dt.weekday()+1)%7):
        count += 1
print(count)
