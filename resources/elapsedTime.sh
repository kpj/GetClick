# Example: [resources/.]/elapsedTime.sh "python2.7 multiThreadLinker.py http://www.gleis9-disco.de/pics/picture/4297/#picture 1 10"

echo "`$1`" | grep "time" | cut -d' ' -f5 | sed 's/ms//g'
