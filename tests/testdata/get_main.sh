#! /bin/bash
base=A6021250_main
url=$(<${base}.url)
curl -o ${base}.html $url
