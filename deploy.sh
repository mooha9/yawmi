#!/bin/zsh
# يبني «يومي» وينشره على Netlify عبر الـAPI، وينتظر حتى يصير النشر جاهزًا
set -e
cd "$(dirname "$0")"
python3 build.py
rm -f deploy.zip
(cd public && zip -q -r -X ../deploy.zip . -x '.DS_Store')
TOKEN=$(python3 -c "import json;d=json.load(open('$HOME/Library/Preferences/netlify/config.json'));print(d['users'][d['userId']]['auth']['token'])")
SITE=$(cat .site_id); NAME=$(cat .site_name)
ID=$(curl -sf -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/zip" \
  --data-binary @deploy.zip "https://api.netlify.com/api/v1/sites/$SITE/deploys" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['id'])")
for i in $(seq 1 30); do
  STATE=$(curl -sf -H "Authorization: Bearer $TOKEN" "https://api.netlify.com/api/v1/sites/$SITE/deploys/$ID" \
    | python3 -c "import sys,json;print(json.load(sys.stdin).get('state',''))")
  case "$STATE" in
    ready) echo "✓ النشر جاهز: https://$NAME.netlify.app"; exit 0 ;;
    error) echo "✗ فشل النشر ($ID)"; exit 1 ;;
  esac
  sleep 2
done
echo "✗ انتهت المهلة والحالة: $STATE"; exit 1
