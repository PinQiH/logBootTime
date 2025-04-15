import os
import csv
from datetime import datetime, timedelta

LOG_FILE = "C:/Users/User/Desktop/work_log.csv"

# 上班時間基準
WORK_THRESHOLD = 7.5  # 超過這個時數才算加班
LUNCH_START = datetime.strptime("12:00", "%H:%M").time()
LUNCH_END = datetime.strptime("13:30", "%H:%M").time()


def log_event(event_type):
    now = datetime.now()
    # date_str = now.strftime("%Y-%m-%d")
    date_str = now.strftime("%Y/%#m/%#d")  # Windows 系統下，月份和日期前的零不顯示
    time_str = now.strftime("%H:%M:%S")

    # 先讀取舊資料
    rows = []
    found = False
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

    # 更新或新增今天的資料列
    for row in rows:
        if row["日期"] == date_str:
            row[event_type + "時間"] = time_str
            found = True
            break

    if not found:
        row = {
            "日期": date_str,
            "開機時間": time_str if event_type == "開機" else "",
            "關機時間": time_str if event_type == "關機" else "",
            "上班時數": "",
            "是否加班": "",
            "加班時數": ""
        }
        rows.append(row)

    # 寫回資料
    with open(LOG_FILE, mode='w', newline='') as file:
        fieldnames = ["日期", "開機時間", "關機時間", "上班時數", "是否加班", "加班時數"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def calculate_daily_hours():
    if not os.path.exists(LOG_FILE):
        print("尚未有任何紀錄。")
        return

    updated_rows = []
    with open(LOG_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = row["日期"]
            start_str = row["開機時間"]
            end_str = row["關機時間"]

            if start_str and end_str:
                start = datetime.strptime(start_str, "%H:%M:%S")
                end = datetime.strptime(end_str, "%H:%M:%S")
                # 午休時間區間
                noon_start = datetime.combine(datetime.today(), LUNCH_START)
                noon_end = datetime.combine(datetime.today(), LUNCH_END)

                # 工時計算
                raw_duration = end - start
                net_duration = round(raw_duration.total_seconds() / 3600, 2)
                work_hours = net_duration - 1.5

                # 加班計算
                if work_hours > WORK_THRESHOLD and (work_hours - WORK_THRESHOLD) >= 0.5:
                    is_ot = "是"
                    overtime = round(work_hours - WORK_THRESHOLD, 2)
                else:
                    is_ot = "否"
                    if work_hours > WORK_THRESHOLD:
                        overtime = round(work_hours - WORK_THRESHOLD, 2)
                    else:
                        overtime = 0

                row["上班時數"] = work_hours
                row["是否加班"] = is_ot
                row["加班時數"] = overtime

            updated_rows.append(row)

    # 寫回更新後資料
    with open(LOG_FILE, mode='w', newline='') as file:
        fieldnames = ["日期", "開機時間", "關機時間", "上班時數", "是否加班", "加班時數"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print("✅ 已更新計算並寫入 work_log.csv！")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "calculate":
        calculate_daily_hours()
    else:
        log_event("開機" if "boot" in sys.argv else "關機")
