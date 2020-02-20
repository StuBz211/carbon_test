#!/bin/bash



WATCH_DIR="/tmp/"
# PID id FIle
PID_FILE="${WATCH_DIR}/send_cpu.pid"
# Log file
LOG="${WATCH_DIR}/send_cpu.log"

# client name
CLIENT=`hostname`
DEFAULT_HOST="127.0.0.1:8001"
HOST="${2:-$DEFAULT_HOST}"

DEFAULT_SLEEP=10
FAIL_SLEEP=60

run_job()
{
while :
do
  CORECOUNT=`grep -c ^processor /proc/cpuinfo`
  CPUUSAGE=`top -bn 1 | awk 'NR>7{s+=$9} END {print s/'$CORECOUNT'}' | awk '{print int($1+0.5)}'`
  echo "CPU load $CPUUSAGE"
  echo "connect to $HOST";
  STATUS=$(
            curl -X POST \
               -w %{http_code} -s -o /dev/null \
               -H "Content-Type: application/json" \
               -d "{\"value\":$CPUUSAGE,\"client\": \"$CLIENT\"}" \
               "$HOST/send_metric"
          )
  if [ "$STATUS" -eq 200 ];
  then
    echo "OK, $DEFAULT_SLEEP seconds sleep"
    sleep $DEFAULT_SLEEP
  else
    echo "SOMETHING WRONG, sleep $FAIL_SLEEP seconds"
    sleep $FAIL_SLEEP
  fi
done
}



# Функция запуска демона
start()
{
	# Если существует файл с pid процесса не запускаем еще одну копию демона
	if [ -e $PID_FILE ]
	then
		_pid=$(cat ${PID_FILE})
		if [ -e /proc/${_pid} ]
		then
			echo "Daemon already running with pid = $_pid"
			exit 0
		fi
	fi

	# make logs file
	touch ${LOG}
	cd /
	# redirect input
	exec > $LOG
	exec < /dev/null

	# start job
	(
		run_job
	)&

	# end work
	echo $! > ${PID_FILE}
}


stop()
{
  # check pid file
  if [ -e ${PID_FILE} ]
  then
    _pid=$(cat ${PID_FILE})
    kill $_pid
    # exit code
    rt=$?
    if [ $rt -eq 0 ]
    then
      # stop and rm pid file
      echo "Daemon stop"
      rm ${PID_FILE}
    else
      echo "Error stop daemon"
    fi
  else
    echo "Daemon is NOT running"
  fi
}


usage()
{
  echo "$0 (start|stop|restart)"
}



# command cases
case $1 in
  "start")
    start
    ;;
  "stop")
    stop
    ;;
  "restart")
    stop
    start
    ;;
  *)
    usage
    ;;
esac
exit

