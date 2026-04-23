#!/bin/bash

# MIJ Digital Threads Bot Manager
# Usage: ./manage_bot.sh [start|stop|restart|logs|status]

BOT_PATH="/home/ilham/botthreads/mij-bot/mesin_jadwal.py"
LOG_FILE="/home/ilham/botthreads/schedule.log"
PYTHON_CMD="python3 -u"

case "$1" in
    start)
        if pgrep -f "$BOT_PATH" > /dev/null; then
            echo "Bot sudah berjalan."
        else
            echo "Memulai Bot MIJ Digital..."
            nohup $PYTHON_CMD "$BOT_PATH" > "$LOG_FILE" 2>&1 &
            echo "Bot berhasil dijalankan di latar belakang."
            echo "Gunakan './manage_bot.sh logs' untuk melihat aktivitas."
        fi
        ;;
    stop)
        if pgrep -f "$BOT_PATH" > /dev/null; then
            echo "Menghentikan Bot..."
            pkill -f "$BOT_PATH"
            echo "Bot telah dihentikan."
        else
            echo "Bot tidak sedang berjalan."
        fi
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    logs)
        echo "Menampilkan log aktivitas (Tekan Ctrl+C untuk keluar):"
        tail -f "$LOG_FILE"
        ;;
    status)
        if pgrep -f "$BOT_PATH" > /dev/null; then
            echo "Status: Bot sedang AKTIF."
            pgrep -a -f "$BOT_PATH"
        else
            echo "Status: Bot MATI."
        fi
        ;;
    *)
        echo "Penggunaan: $0 {start|stop|restart|logs|status}"
        exit 1
esac

exit 0
