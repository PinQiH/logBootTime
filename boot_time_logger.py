# boot_time_logger.py

from datetime import datetime

# 指定文本檔的路徑
log_file_path = "C:/Users/User/Desktop/logfile.txt"

# 獲取當前時間
now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

# 寫入時間到文本檔
with open(log_file_path, "a") as file:
    file.write(f"開機時間: {current_time}\n")
