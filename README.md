# calculate_daily_hours
### ▶️ 開機時執行

1. 按下 `Win + R`，輸入 `shell:startup`，按 Enter。
2. 這會打開「啟動資料夾」。
3. 建立一個 `.bat` 批次檔，內容如下：
    
    (py)
    
    ```powershell
    @echo off
    python "C:\路徑\到\你的\calculate_daily_hours.py boot"
    
    ```
    
    > 📝 如果你是用虛擬環境（venv），記得要先啟用它再跑 script。
    > 
    
    (exe)
    
    ```powershell
    @echo off
    calculate_daily_hours.exe boot
    
    ```
    
4. 把這個 `.bat` 檔放進剛剛那個「啟動資料夾」裡就好了。

---

### ⏹️ 關機時執行

1. 打開「本機群組原則編輯器」（`gpedit.msc`）
2. 到 `使用者設定 > Windows 設定 > 指令碼（啟動/關機） > 關機 > 內容`
3. 新增關機前的指令碼
    
    (py)
    
    ```powershell
    python "C:\路徑\到\你的\calculate_daily_hours.py shutdown"
    python "C:\路徑\到\你的\calculate_daily_hours.py calculate"
    ```
    
    (exe)
    
    ```powershell
    calculate_daily_hours.exe shutdown
    calculate_daily_hours.exe calculate
    ```
