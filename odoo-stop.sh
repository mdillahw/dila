#!/bin/sh
PRG="$0"

while [ -h "$PRG" ] ; do
  ls=`ls -ld "$PRG"`
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    PRG="$link"
  else
    PRG=`dirname "$PRG"`/"$link"
  fi
done

loc=`dirname "$PRG"`
pid_file=my-odoo.pid

if [ -f "$loc"/"$pid_file" ]; then
  echo "Stopping odoo-server..."
  cat "$loc"/"$pid_file" | xargs kill -9
  rm "$loc"/"$pid_file"
  sleep 1
  echo "Odoo-server stoped."
  exit 0
else
  echo "Odoo-server is curently stoped."
  exit 1
fi

exit 0
