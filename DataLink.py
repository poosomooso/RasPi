import threading
import queue
import PhysicalLayer
import MorseCode
import time

ID = 'B'
PROTOCOL = 'B'
parityQ = queue.Queue()

def transmit(q):
	while True:
		msgDict = q.get()
		msg = ' '+msgDict['message']

		packet = msgDict['recipient']+' '+ID+' '
		
		parity = getHash(packet+msg)
		
		PhysicalLayer.physicalTransmit(packet+parity+msg)
		
		start = time.time()
		while True:
			try:
				ok = parityQ.get_nowait()
				if ok['recipient'] == msgDict['recipient'] and ok['source'] == ID:
					#recieved ok message
					break
			except QueueEmpty:
				pass
			
			if time.time() - start >= 15: #waiting for 15 seconds
				PhysicalLayer.physicalTransmit(packet+parity+msg)
				start = time.time()



def readMessage(q, networkq):
	""" q is the queue to push messages to """
	def extractHeader(m):
		msgSplit = m.split()
        print(msgSplit)

        recip = msgSplit[0]
        src = msgSplit[1]

        if len(msgSplit)==2:
        	parityQ.put({'recipient':recip,
        		'source':src})
        else:
	        parity = msgSplit[2]
	        msg = ' '.join(msgSplit[3:])

	        return {
	            'recipient': recip, 
	            'source':src, 
	            'parity':parity, 
	            'message':msg }

	messageProgress = {}
	while True:
		msg = q.get()
		data = extractHeader(msg)
		if len(data) == 2:
			parityQ.put(data)
		else:
			src = data['source']
			if data['recipient'] == ID:
				parityMsg = ' 'join(data['recipient'], src, '', data['message'])
				if data['parity'] == getHash(parityMsg):
					PhysicalLayer.physicalTransmit('{} {}'.format(src, data['recipient']))
				else:
					break;
				networkq.put(data['message'])
			

def getHash(msg):
    s = 0
    for c in msg:
        s += ord(c.upper())
    return chr(65 + s % 26)
	

		


