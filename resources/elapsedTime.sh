echo "`$1`" | grep "time" | cut -d' ' -f5 | sed 's/ms//g'
