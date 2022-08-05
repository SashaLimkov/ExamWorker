def date_time_formater(date_time):
    date, time = date_time.strip().split(" ")
    date = date.split("-")
    date = f"{date[-1]}.{date[1]}.{date[0]}"
    print(date)
    hours, minutes, *trash = time.split(":")
    res = f"{hours}:{minutes} {date}"
    return res