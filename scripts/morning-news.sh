#!/bin/zsh
# يحدّث ملخص أخبار «يومي» كل صباح: Claude يكتب src/news.json فقط، والسكربت يتحقق ثم يدفع، وGitHub Actions ينشر إلى GitHub Pages
set -u
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
cd "$(dirname "$0")/.."
LOG=logs/news.log; mkdir -p logs
exec >>"$LOG" 2>&1
TODAY=$(TZ=Asia/Riyadh date +%F)
echo "===== $(date '+%F %T') · $TODAY ====="

# لا تكرّر العمل إن كان ملخص اليوم منشوراً (مثلاً عند استيقاظ الجهاز بعد تشغيل سابق)
git pull -q --rebase || { echo "✗ فشل git pull"; exit 1; }
if python3 -c "import json,sys;sys.exit(0 if json.load(open('src/news.json'))['date']=='$TODAY' else 1)"; then
  echo "ملخص اليوم موجود مسبقاً"; exit 0
fi

cp src/news.json /tmp/yawmi-news.bak
claude -p "$(cat scripts/news-prompt.md)

Today's date in Riyadh: $TODAY ($(TZ=Asia/Riyadh LC_ALL=en_US.UTF-8 date +%A))" \
  --model sonnet --allowedTools "WebSearch" "WebFetch" "Read" "Edit" "Write" --permission-mode acceptEdits
echo

# التحقق: JSON صالح، وتاريخ اليوم، والبنية كاملة، ولم يتغيّر أي ملف آخر
if ! python3 - "$TODAY" <<'PY'
import json,sys
d=json.load(open("src/news.json"))
assert d["date"]==sys.argv[1], "date"
assert [m["k"] for m in d["markets"]]==["sa","us","crypto"], "markets"
for m in d["markets"]: assert m["points"] and m["sources"] and m["headline"], m["k"]
assert len(d["ai"]["items"])>=4 and d["ai"]["sources"], "ai"
PY
then echo "✗ الملف غير صالح، أُعيدت النسخة السابقة"; cp /tmp/yawmi-news.bak src/news.json; exit 1; fi
OTHER=$(git status --porcelain | grep -v " src/news.json$" | grep -v "^?? logs/")
if [ -n "$OTHER" ]; then echo "✗ تغيّرت ملفات أخرى:"; echo "$OTHER"; git checkout -- . ; exit 1; fi

git add src/news.json && git commit -q -m "أخبار $TODAY" && git push -q && echo "✓ دُفع ملخص $TODAY — سيُنشر خلال دقيقة"
