# Module MorseTX
from MorseCode import MorseCode
from options import *

def MorseTX(M):
    print('sending')
    for W in M.split(" "):
        for L in W:
            for Dd in MorseCode[L]:
                yield (1, DIT_TIME) if Dd == "." else (1 , DIT_TIME * 3.0) #dot or dash
                yield (0, DIT_TIME) #end of dot or dash
            yield(0, DIT_TIME * 2) #end of letter
        yield (0, DIT_TIME * 4) #end of word
    yield (1, DIT_TIME * 8) #end of message
    yield(0,DIT_TIME)

if __name__ == "__main__":
    print("AN ACE")
    for OOKtuple in MorseTX("AN ACE"):
        print(OOKtuple)
    print("OOK AT ME")
    for OOKtuple in MorseTX("OOK AT ME"):
        print(OOKtuple)
             