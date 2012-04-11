import threading, time, urllib, sys, signal, math

# HANDLE STARTUP
link2curl = ''
threads2create = 0
maxCounter = -1
if len(sys.argv) != 3:
	if len(sys.argv) == 4:
		maxCounter = int(sys.argv[3])
	else:
		print "Usage: %s <url to site> <number of threads> [number of clicks]" % (sys.argv[0])
		sys.exit()
link2curl = str(sys.argv[1])
if not "http" in link2curl:
	link2curl = "http://" + link2curl
threads2create = int(sys.argv[2])
ID = 1
counter = 0
running = True
times = []

def sighandler(signum, frame):
	global running, endT
	running = False
	endT = time.time()
	showStats()
	sys.exit()
for i in [x for x in dir(signal) if x.startswith("SIG")]:
	try:
		signum = getattr(signal, i)
		signal.signal(signum, sighandler)
	except:
		pass

# NEEDED FUNCTIONS
def genMDEV():
	avg = sum(times)/len(times)
	res = []
	for i in times:
		res.append(pow(i - avg, 2))
	mdev = math.sqrt(sum(res)/len(res))
	return mdev
def showStats():
	print "--- Curled \"%s\" with %i threads statistics ---" % (link2curl, threads2create)
	print "%i clicks generated, time %ims" % (
		counter,
		(endT - startT) * 1000
	)
	if maxCounter != -1 and maxCounter <= len(t):
		print "Just flooding your resource..."
		sys.exit()
	print "cdt min/avg/max/mdev = %.3f/%.3f/%.3f/%.3f ms" % (
		min(times),
		sum(times)/len(times),
		max(times),
		genMDEV()
	)
	sys.exit()

# NEEDED CLASSES
class curli(threading.Thread):
	def run(self):
		global ID, counter, running, times
		myID = ID
		myCounter = 0
		ID += 1
		while running:
			myCounter += 1
			counter += 1
			print "[%i] : %i" % (myID, myCounter)
			first = time.time()
			urllib.urlopen(link2curl)
			second = time.time()
			times.append((second - first) * 1000)

#signal.signal(signal.SIGINT, showStats)
#signal.signal(signal.SIGTERM, showStats)
#signal.signal(signal.SIGQUIT, showStats)

# START THREADS
t = []
startT = time.time()
for i in range(threads2create):
	t.append(curli())
	if maxCounter != -1 and i >= maxCounter:
		break
for i in t:
	i.start()

# HANDLE DEAD THREADS
while running:
	allDead = True
	for i in t:
		if i.isAlive():
			allDead = False
	if allDead:
		showStats()
		sys.exit()

	if maxCounter != -1 and counter >= maxCounter:
		endT = time.time()
		running = False

showStats()
