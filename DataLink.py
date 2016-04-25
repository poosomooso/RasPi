import threading
import queue
import PhysicalLayer
import MorseCode

ID = 'B'
PROTOCOL = 'B'

def transmit(q):
	while True:
		msg = ' '+q.get()

		packet = recipient+' '+ID+' '
		
		parity = getHash(packet+msg)
		
		PhysicalLayer.physicalTransmit(packet+parity+msg)


def readMessage(q):
	""" q is the queue to push messages to """
	def extractHeader(m):
		msgSplit = m.split()
        print(msgSplit)

        recip = msgSplit[0]
        src = msgSplit[1]
        parity = msgSplit[2]
        msg = ' '.join(msgSplit[3:])

	messageProgress = {}
	while True:
		msg = q.get()
		data = extractHeader(msg)
		src = data['source']
		if data['recipient'] == ID:
			if data['remainingMsgs'] > 1:
				message = data['message']
				messageProgress[src] = messageProgress.get(src, '')+message
				# for i in range(data['remainingMsgs'], 0, -1):
				# 	pass #iterate through the next messages and concat string
			else:
				firstPart =  messageProgress.get(src, '')
				try: 
					del messageProgress[src]
				except KeyError as e: 
					print(e)
				print(firstPart+data['message'])

def getHash(msg):
    s = 0
    for c in msg:
        s += ord(c.upper())
    return chr(65 + s % 26)

if __name__ == "__main__":
	tx=threading.Thread(target=transmit,name="TRANSMIT")
	tx.start()
	q = queue.Queue()
	rx=threading.Thread(target=readMessage, name="DATALINKRECIEVER",args=(q,))
	rx.start()
	PhysicalLayer.reciever(q)
	#how to pull from physical layer's strings?
	tx.join()
	rx.join()

		


