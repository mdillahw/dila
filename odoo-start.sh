#!/bin/sh
# Better OS/400 detection: see Bugzilla 31132
os400=false
case "`uname`" in
OS400*) os400=true;;
esac

# resolve links - $0 may be a softlink
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

# set parameter
loc=`dirname "$PRG"`
exe_file=odoo.py
pid_file=my-odoo.pid

# execute commands
# Check that target executable exists
if $os400; then
  # -x will Only work on the os400 if the files are:
  # 1. owned by the user
  # 2. owned by the PRIMARY group of the user
  # this will not work if the user belongs in secondary groups
  eval
else
  if [ ! -x "$loc"/"$exe_file" ]; then
    echo "Cannot find $loc/$exe_file"
    echo "The file is absent or does not have execute permission"
    echo "This file is needed to run this program"
    exit 1
  fi
fi

if [ ! -f "$loc"/"$pid_file" ]; then
	echo "Starting odoo-server..."
	if [ -f "$loc"/"$exe_file" ]; then
		my_pid=""
		exec python "$loc/$exe_file" & echo $! >"$loc/$pid_file"
		rc=$?
		echo "$rc"
    	if [ $rc != 0 ]; then
			sleep 1
			echo "Error when starting odoo-server"
			echo "Odoo-server not started."
			if [ -f "$loc"/"$pid_file" ]; then
				rm "$loc"/"$pid_file"
			fi
		else
			sleep 1
			echo "Odoo-server started."
		fi
	else
		echo "Cannot found odoo.py"
		echo "Odoo-server not started."
	fi
else
	read pid < "$loc"/"$pid_file"
	echo $pid
	ps -p $pid > /dev/null
	r=$?
	if [ $r -eq 0 ]; then
    	echo "Odoo-server is currently running, not executing twice, exiting now..."
    	exit 1
	else
		echo "My-odoo.pid file exist, but odoo-server is not running."
		echo "Deleting my-odoo.pid file..."
		rm "$loc"/"$pid_file"
		sleep 1
		echo "My-odoo.pid file was deleted."
	fi
fi

exit 1
