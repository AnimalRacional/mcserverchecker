import schedule

def job():
    for i in range(0, 100):
        print("JOB:", i, i * i)

schedule.every(10).seconds.do(job)