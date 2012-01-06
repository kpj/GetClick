import popen2, sys, url2load, os


class tester(object):
	def __init__(self):
		if len(sys.argv) != 3:
			print "Usage: <how many clicks> <how many threads at maximum>"
			sys.exit()

		self.COUNTER = int(sys.argv[1])
		self.THREADMAX = int(sys.argv[2])

		self.URL = url2load.URL

		self.smooth = True if self.THREADMAX >= 4 else False

		self.data_dir = 'plainData'
		self.data_name = 'data_%i-%i' % (self.COUNTER, self.THREADMAX)

		self.test_command = 'resources/elapsedTime.sh "python2.7 resources/multiThreadLinker.py %s %i %i"'
		self.draw_command = 'gnuplot %s'

		self.plotter_dir = 'plotter'
		self.plotter_name = 'makePlot_%i-%i' % (self.COUNTER, self.THREADMAX)
		self.plotter_name_smooth = 'makePlot_%i-%i%s' % (self.COUNTER, self.THREADMAX, "_smooth")
		self.plotter_content = '''# auto generated plotter
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
# hope you enjoy'''
		self.plotter_content_smooth = '''# auto generated plotter
set autoscale
unset log
unset label
set term png
set output 'graphs/%i-%i_smooth.png'
set xtic auto
set ytic auto
set title "Thread-Amount and Time Relation (%i clicks)"
set xlabel "Amount of Threads"
set ylabel "Elapsed Time"
set xr [0:%i]
set yr [0:%i]
plot 'plainData/data_%i-%i' using 1:2 smooth csplines title 'Developement of Time' with linespoints
# hope you enjoy'''

	def execCurl(self, threadNum):
		r, w, e = popen2.popen3( self.test_command % ( self.URL, threadNum, self.COUNTER ) )
		output = r.readlines()
		r.close()
		w.close()
		e.close()
		return output

	def genMaxtime(self):
		l = [int(v) for v in self.dats.values()]
		m = max(l)
		return round(int(m) + 5 * pow(10, len(str(m))-2) , -(len(str(m))-1))

	def print2file(self, f, t):
		fd = open(f, 'a+')
		print >> fd, t
		fd.flush()
		fd.close()

	def doesExist(self):
		if self.data_name in os.listdir(self.data_dir):
			return True
		return False

	def gainData(self):
		self.dats = {}
		for i in range(1, self.THREADMAX + 1):
			print ">> Running with %i thread(s)..." % i
			self.dats[i] = self.execCurl(i)[0].strip()
			key = int(i)
			val = int(self.dats[i])
			self.print2file(os.path.join(self.data_dir, self.data_name), "%i   %i" % (key, val))

	def genPlotter(self):
		self.print2file(os.path.join(self.plotter_dir, self.plotter_name), self.plotter_content % (
			self.COUNTER, 
			self.THREADMAX, 
			self.COUNTER, 
			self.THREADMAX, 
			self.genMaxtime(), 
			self.COUNTER, 
			self.THREADMAX, 
		))
		if self.smooth:
			self.print2file(os.path.join(self.plotter_dir, self.plotter_name_smooth), self.plotter_content_smooth % (
			self.COUNTER, 
			self.THREADMAX, 
			self.COUNTER, 
			self.THREADMAX, 
			self.genMaxtime(), 
			self.COUNTER, 
			self.THREADMAX, 
		))

	def drawGraphs(self):
		popen2.popen3(self.draw_command % os.path.join(self.plotter_dir, self.plotter_name))
		if self.smooth:
			popen2.popen3(self.draw_command % os.path.join(self.plotter_dir, self.plotter_name_smooth))

t = tester()
print "Executing command to gain %i clicks with up to %i threads." % (t.COUNTER, t.THREADMAX)
if t.doesExist():
	print ">>> Note: This data-set does already exist; to recreate it, delete it..."
t.gainData()
print ">> Generating corresponding plotter..."
t.genPlotter()
print ">> Drawing graphs..." if t.smooth else ">> Just drawing normal graph (need at least 4 points)..."
t.drawGraphs()
