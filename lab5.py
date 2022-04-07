#Jack Masterson / 224194
#lab 5: hashes all files in file system and compares them to past hashes

import os, hashlib, time, sys, csv
import signal
#github.com/BealeD/SY402-Spring-22/blob/main/hashit3.py helped with error handling and a few other things

class Alarm(Exception):
    pass
def alarm_handle(signum, frame):
    raise Alarm

BLOCKSIZE = 65536   #recommended for large files from pythoncentral.io/hashing-files-with-python/

entiresys = os.walk('/')
filepath = ''
dontlook = ['/dev', '/proc', '/run', '/sys', '/tmp', '/var/lib', '/var/run']
m = hashlib.sha256()
filehashes = []

#implementation of os.walk() taken from docs.python.org/3/library/os.html
for path, dirs, files in entiresys:
    if path in dontlook:    #this idea taken from linuxhint.com/python-os-walk-example
        dirs[:] = []
        files[:] = []
        continue
    for file in files:
        if ' ' in file:
            file = file.replace(' ', '\ ')
        if path != '/':
            totalpath = path + '/' + file
        if path == '/':
            totalpath = path + file
        try:
            signal.signal(signal.SIGALRM, alarm_handle)
            signal.alarm(2)
            with open(totalpath, 'rb') as f:    #file hashing learned from pythoncentral.io/hashing-files-with-python/
                buf = f.read(BLOCKSIZE)
                while len(buf) > 0:
                    m.update(buf)
                    buf = f.read(BLOCKSIZE)
                x = time.time()     #from w3schoolars.com/python/python_datetime.asp
                filehash = (totalpath, m.hexdigest(), str(x))
                filehashes.append(filehash)
            signal.alarm(0)
        except IOError:
            pass
        except Alarm:
            print("Taking too long to hash.")

with open('filehashes.txt', 'r') as f:  #read old hashes in
    oldhashes = csv.reader(f)
    oldhashes = list(oldhashes)
    for newhash in filehashes:
        newhash = list(newhash)
        if newhash[0] not in [item[0] for item in oldhashes]:   #stackoverflow.com/questions/25050311/extract-first-item-of-each-sublist helped with list comprehension
            print("New file found:", newhash)
            continue
        else:
            index = -1
            for i in range(len(oldhashes)):     #tutorialspoint.com/python-indexing-a-sublist helped with this
                if oldhashes[i][0] == newhash[0]:
                    index = i
            if index == -1:
                continue
            if oldhashes[index][1] != newhash[1]:
                print("Hashes don't match:", oldhashes[index][0], oldhashes[index][1], "vs.", newhash[1])
    for oldhash in oldhashes:
        found = False
        for i in range(len(filehashes)):
            if filehashes[i][0] == oldhash[0]:
                found = True
        if found == False:
            print("File removed:", oldhash)
with open('filehashes.txt', 'w') as f:  #wipe file first
    f.write('')
with open('filehashes.txt', 'a') as f:  #add filehashes to file, separate by comma and newlines
    for filehash in filehashes:
        towrite = filehash[0] + ',' + filehash[1] + ',' + filehash[2] + '\n'
        f.write(towrite)












