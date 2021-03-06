import popen2, sys, url2load, os

if len(sys.argv) != 3:
	print "Usage: <how many clicks> <how many threads at maximum>"
	sys.exit()

COUNTER = int(sys.argv[1])
THREADMAX = int(sys.argv[2])

URL = url2load.URL

def execCurl(threadNum):
	'''
	Returns duration of curling for given thread number
	'''
	command = 'resources/elapsedTime.sh "python2.7 resources/multiThreadLinker.py %s %i %i"' % (URL, threadNum, COUNTER)
	r, w, e = popen2.popen3(command)
	output = r.readlines()
	r.close()
	e.close()
	w.close()
	return output

print "Executing command to gain %i clicks with up to %i threads." % (COUNTER, THREADMAX)

DATANAME = 'data_%i-%i' % (COUNTER, THREADMAX)
dirs = os.listdir("plainData")
if DATANAME in dirs:
	print '>>> Note: This data-set does already exist...'

fd = open(os.path.join('plainData', DATANAME), 'a+')

r = {}
for i in range(1, THREADMAX + 1):
	print ">> Running with %i thread(s)..." % i
	# r[number of threads] = duration of requests
	r[i] = execCurl(i)
	key = int(i)
	val = int(r[i][0].strip())
	print >> fd, "%i   %i" % (key, val)
	fd.flush()
#	print ">>> Write: \"%i   %i\"..." % (key, val)

fd.close()

t = []
for i in r.values():
	t.append(int(i[0].strip()))
m = max(t)
MAXTIME = round(int(m) + 5 * pow(10, len(str(m))-2) , -(len(str(m))-1)) # Very cool expression to round up

print "Now drawing graph."
print ">> Generating corresponding plotter..."
sample = '''# auto generated plotter
set autoscale
unset log
unset label
set term png
set output 'graphs/%i-%i.png'
set xtic auto
set ytic auto
set title "Thread-Amount and Time Relation (%i clicks)"
set xlabel "Amount of Threads"
set ylabel "Elapsed Time"
set xr [0:%i]
set yr [0:%i]
plot 'plainData/data_%i-%i' using 1:2 title 'Developement of Time' with linespoints
# hope you enjoy''' % (COUNTER, THREADMAX, COUNTER, THREADMAX, MAXTIME, COUNTER, THREADMAX)
fd = open('plotter/makePlot_%i-%i' % (COUNTER, THREADMAX), 'a+')
print >> fd, sample
fd.close()
print ">> Drawing normal graph..."
r, w, e = popen2.popen3('gnuplot plotter/makePlot_%i-%i' % (COUNTER, THREADMAX))
r.close()
e.close()
w.close()

if THREADMAX >= 4:
	print ">> Generating interpolated plotter..."
	sample = '''# auto generated plotter
	set autoscale
	unset log
	unset label
	set term png
	set output 'graphs/%i-%i_smooth.png'
	set xtic auto
	set ytic auto
	set title "Thread-Amount and Time Relation (%i clicks, smooth)"
	set xlabel "Amount of Threads"
	set ylabel "Elapsed Time"
	set xr [0:%i]
	set yr [0:%i]
	plot 'plainData/data_%i-%i' using 1:2 smooth csplines title 'Developement of Time' with linespoints
	# hope you enjoy''' % (COUNTER, THREADMAX, COUNTER, THREADMAX, MAXTIME, COUNTER, THREADMAX)
	fd = open('plotter/makePlot_%i-%i_smooth' % (COUNTER, THREADMAX), 'a+')
	print >> fd, sample
	fd.close()
	print ">> Drawing interpolated graph..."
	r, w, e = popen2.popen3('gnuplot plotter/makePlot_%i-%i_smooth' % (COUNTER, THREADMAX))
	r.close()
	e.close()
	w.close()
else:
	print ">> Cannot generate interpolated graph (less than 5 points)..."
