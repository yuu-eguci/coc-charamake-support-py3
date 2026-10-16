#!/bin/sh
# 仮想ディスプレイ (TigerVNC) にアプリを表示し、 noVNC でブラウザから見られるようにします。
set -eu

# 前回 docker compose stop したときのロックが残っていると起動しないので消します。
rm -f /tmp/.X0-lock /tmp/.X11-unix/X0

# ほかの Web ページから勝手に接続されないよう、起動ごとにパスワードを作ります。
password=$(python -c 'import secrets; print(secrets.token_hex(4))')
printf '%s\n' "$password" | vncpasswd -f > /tmp/vncpasswd

Xtigervnc :0 -geometry 1400x1000 -depth 24 -localhost -rfbport 5900 \
    -SecurityTypes VncAuth -PasswordFile /tmp/vncpasswd -AlwaysShared &
vnc_pid=$!
while [ ! -e /tmp/.X11-unix/X0 ]; do
    kill -0 "$vnc_pid" 2>/dev/null || { echo "Xtigervnc の起動に失敗しました" >&2; exit 1; }
    sleep 0.1
done

websockify --web /usr/share/novnc 6080 localhost:5900 &

echo "ブラウザで開いてね: http://127.0.0.1:6080/vnc.html#autoconnect=true&resize=scale&password=$password"

export DISPLAY=:0
exec python /app/CocCharamakeSupport.py
