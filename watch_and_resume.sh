#!/usr/bin/env bash
# NIM watchdog: deepseek-v4-pro gelince benchmark resume'ü otomatik başlatır.
# Kullanım: bash watch_and_resume.sh

set -euo pipefail

REPO="$HOME/Projects/outside-in-alignment"
RUN_DIR="$REPO/benchmark/runs/20260518T202504Z"
LOG="/tmp/oia_resume.log"
CHECK_INTERVAL=120  # saniye

NIM_URL="https://integrate.api.nvidia.com/v1/chat/completions"
MODEL="deepseek-ai/deepseek-v4-pro"
PAYLOAD='{"model":"deepseek-ai/deepseek-v4-pro","messages":[{"role":"user","content":"ok"}],"max_tokens":3}'

echo "[watchdog] Başlıyor. Her ${CHECK_INTERVAL}s'de deepseek-v4-pro kontrol edilecek."
echo "[watchdog] Resume log: $LOG"
echo "[watchdog] $(date)"

check_nim() {
  HTTP=$(curl -s -m 30 -o /dev/null -w "%{http_code}" \
    -X POST "$NIM_URL" \
    -H "Authorization: Bearer $NVIDIA_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" 2>/dev/null || echo "000")
  echo "$HTTP"
}

while true; do
  STATUS=$(check_nim)
  echo "[watchdog] $(date +%H:%M:%S) deepseek-v4-pro HTTP $STATUS"

  if [[ "$STATUS" == "200" ]]; then
    echo "[watchdog] API hazır! Resume başlatılıyor..."
    echo "--- RESUME BAŞLADI: $(date) ---" >> "$LOG"

    cd "$REPO"
    caffeinate -disu python3 -u kit/run_benchmark.py \
      --resume "$RUN_DIR" \
      --no-v01 --with-v03 \
      --n 3 --workers 2 \
      >> "$LOG" 2>&1

    echo "[watchdog] Benchmark tamamlandı. Çıkıyorum."
    exit 0
  fi

  echo "[watchdog] Bekliyorum ${CHECK_INTERVAL}s..."
  sleep "$CHECK_INTERVAL"
done
