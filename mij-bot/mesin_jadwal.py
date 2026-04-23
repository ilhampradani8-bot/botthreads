import time
import random
import sys
import os
from datetime import datetime, timedelta

# Import the bot logic
sys.path.append(os.path.abspath("/home/ilham/botthreads/mij-bot"))
import bot

def get_peak_hour_schedule():
    """Generate 5 posting times based on Malaysia peak hours (FYP)."""
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Malaysia Peak Windows (Waktu FYP Malaysia)
    windows = [
        (8, 10),   # Window 1: Breakfast / Commute (08:00 - 10:00)
        (12, 14),  # Window 2: Lunch Break (12:00 - 14:00)
        (17, 19),  # Window 3: After Work / Commute (17:00 - 19:00)
        (20, 22),  # Window 4: Prime Time (20:00 - 22:00)
        (23, 24)   # Window 5: Late Night (23:00 - 00:00)
    ]
    
    schedules = []
    for start, end in windows:
        # Pick a random minute within the window
        random_minutes = random.randint(0, (end - start) * 60 - 1)
        target_time = today + timedelta(hours=start, minutes=random_minutes)
        
        # If the target time is in the past for today, schedule it for the next window check
        # The main loop will handle picking new schedules every day
        if target_time > now:
            schedules.append(target_time)
            
    schedules.sort()
    return schedules

def run_scheduler():
    bot.log_message("=== MESIN JADWAL MIJ DIGITAL DIMULAKAN (WAKTU PEAK MALAYSIA) ===")
    
    current_day = datetime.now().date()
    daily_schedules = get_peak_hour_schedule()
    
    if not daily_schedules:
        # If all windows for today are passed, wait for tomorrow
        bot.log_message("Semua window posting hari ini sudah berlalu. Menunggu hari esok...")
    else:
        bot.log_message(f"Jadual posting untuk baki hari ini ({current_day}):")
        for s in daily_schedules:
            bot.log_message(f" - Post dirancang pada: {s.strftime('%H:%M:%S')}")

    while True:
        now = datetime.now()
        
        # Reset schedules at the start of a new day (00:00)
        if now.date() > current_day:
            current_day = now.date()
            daily_schedules = get_peak_hour_schedule()
            bot.log_message(f"--- Hari Baru Dikesan: {current_day} ---")
            bot.log_message("Menjana jadual posting baru (FYP Malaysia):")
            for s in daily_schedules:
                bot.log_message(f" - Post dirancang pada: {s.strftime('%H:%M:%S')}")

        # Check if it's time to post
        for i, scheduled_time in enumerate(daily_schedules):
            if now >= scheduled_time:
                bot.log_message(f"!!! MASA POSTING PEAK HOUR ({scheduled_time.strftime('%H:%M')}) !!!")
                
                # Retry logic: Jika gagal, cuba lagi setiap 5 minit sehingga berjaya
                success = False
                retry_count = 0
                while not success:
                    success = bot.run_job()
                    if success:
                        # Remove the finished job from the list
                        daily_schedules.pop(i)
                        break
                    else:
                        retry_count += 1
                        bot.log_message(f"Cubaan ke-{retry_count} gagal. Menunggu 5 minit sebelum cuba lagi...")
                        time.sleep(300) # Tunggu 5 minit
                        
                break
        
        # Sleep for 30 seconds before checking again
        time.sleep(30)

if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        bot.log_message("Mesin Jadwal dihentikan secara manual.")
    except Exception as e:
        bot.log_message(f"KRITIKAL: Mesin Jadwal terhenti akibat ralat: {e}")
