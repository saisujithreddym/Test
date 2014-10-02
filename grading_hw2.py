"""
---------------------------------------------------------------------------
Grading script for ECEN 602 : HW2 : TFTP Server implementation

Run in the client side with command line options as follows:

python grading_hw2.py <serverIP> <serverPort>
---------------------------------------------------------------------------
Requirements:
Make sure the files small, medium and large are present in the server side. 
1. small - https://www.dropbox.com/s/vnmpwbez0d81jce/small
2. medium - https://www.dropbox.com/s/7bj15hlxg6pge6o/medium
3. large - https://www.dropbox.com/s/ezgq39efjfljgme/large

To get the files, do "wget <url>"

Run this script from a different directory/different machine than the server.


Note that you may need to download tftp-hpa which is an improved version of the tftp client
It is already present in the lab machines. To install in your own machines do: sudo apt-get install tftp-hpa
---------------------------------------------------------------------------

What script does:

Downloads the source files to compare against:
Downloads the actual files from tftp server at the given IP and port
Compares each of them and returns
---------------------------------------------------------------------------
Report bugs to:  nityendrasingh(at)tamu(dot)edu
---------------------------------------------------------------------------
"""

#!/usr/bin/python

import sys
import subprocess
import os
import threading
import filecmp

points=0

class largeio (threading.Thread):
    def __init__(self, cmd, x):
        self.cmd = cmd
        self.x = x
        threading.Thread.__init__(self)
    def run(self):
        test_large = self.cmd+ '-c get large large'+str(self.x)
        print 'Running command: '+test_large
        out = os.system(test_large)
        print out
        

def main():
    global points
    print 'Downloading source files to compare against'
    print 'Getting small'
    os.system('wget -O small https://www.dropbox.com/s/vnmpwbez0d81jce/small')
    print 'Getting medium'
    os.system('wget -O medium https://www.dropbox.com/s/7bj15hlxg6pge6o/medium')
    print 'Getting large'
    os.system('wget -O large https://www.dropbox.com/s/ezgq39efjfljgme/large')


    test_base = 'tftp -m octet '
    for arg in sys.argv[1:]:
        test_base += arg
	test_base += ' '

    test_small = test_base+' -c get small small1'
    print 'Running command: '+test_small 
    out = os.system(test_small)
    print out
    if filecmp.cmp('small', 'small1'):
        points+=20

    test_medium = test_base+' -c get medium medium1'
    print 'Running command: '+test_medium
    out = os.system(test_medium)
    print out
    if filecmp.cmp('medium', 'medium1'):
        points+=20

    test_large = test_base+' -c get large large0'
    print 'Running command: '+test_large
    out = os.system(test_large)
    print out
    if filecmp.cmp('large', 'large0'):
        points+=20

    print 'Testing file not found'    
    test_random = test_base+' -c get asdkjasdfh kuagsfbds'
    out = os.system(test_random)
    print out


def large_io_test():
    global points
    test_base = 'tftp -m octet '
    for arg in sys.argv[1:]:
        test_base += arg
        test_base += ' '
    threads = []
    thread1 = largeio(test_base,1)
    thread2 = largeio(test_base,2)
    thread1.start()
    thread2.start()
    threads.append(thread1)
    threads.append(thread2)
    for t in threads:
        t.join()
    
    if filecmp.cmp('large', 'large1') and filecmp.cmp('large', 'large2'):
        points+=20
    print "Test Complete\n"
    print "Points = "+str(points)

def delete_file(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError, e:
            print ("Error: %s - %s." % (e.filename,e.strerror))
    else:
        print("Sorry, I can not find %s file." % filename)

if __name__ == "__main__":
    main()
    large_io_test()
    delete_file('large')
    delete_file('large0')
    delete_file('large1')
    delete_file('large2')
    delete_file('small')
    delete_file('small1')
    delete_file('medium')
    delete_file('medium1')
    delete_file('kuagsfbds')
