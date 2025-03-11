# /usr/bin/bash
base=A6021250_active_players
url=$(<${base}.url)
curl -o ${base}.html $url
