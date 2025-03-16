#! /bin/bash
player1=12910923
player2=13214962
ofile=hth_${player1}_vs_${player2}
url="https://www.uschess.org/datapage/gamestats.php?memid=${player1}&ptype=O&rs=R&drill=${player2}"
curl -o ${ofile}.html $url
