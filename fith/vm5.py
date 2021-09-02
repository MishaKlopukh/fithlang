import io
import sys
def kh32decode(bitstr):
    assert bitstr[:4] == b'kh32', "Missing magic number"
    values = []
    for i in range(4,len(bitstr),4):
        values.append(int.from_bytes(bitstr[i:i+4],'little',signed=True))
    return values
def sim5(mem, stdin=io.BytesIO()):
    while True:
        try:
            movfrom = mem[mem[0]]
            movto = mem[mem[0]+1]
            if movfrom==movto:
                mem[0] += 2
                return ''
            elif movfrom==4:
                mem[movto]=mem[1]+mem[2]
            elif movfrom==5:
                mem[movto]=mem[1]-mem[2]
            elif movfrom==6:
                mem[movto]=mem[1]*mem[2]
            elif movfrom==14:
                mem[movto]=mem[1]^mem[2]
            elif movfrom==7:
                if mem[2]==0:
                    mem[movto]=0
                else:
                    mem[movto]=mem[1]//mem[2]
            elif movfrom==8:
                mem[movto]=0 if mem[1]>mem[2] else -1
            elif movfrom==9:
                mem[movto]=0 if mem[1]<mem[2] else -1
            elif movfrom==10:
                mem[movto]=0 if mem[1]==mem[2] else -1
            elif movfrom==13:
                mem[movto]=-1 if mem[3]==0 else 0
            elif movfrom==15:
                mem[movto]=mem[1] if mem[3]==0 else mem[2]
            elif movfrom==11:
                mem[movto]=ord(stdin.read(1))
            else:
                mem[movto]=mem[movfrom]
            if movto != 0:
                mem[0] += 2
            output=chr(mem[movfrom]) if movto==12 else ''
        except IndexError:
            mem += [0]*64
            continue
        break
    return output
def vm5(mem, instream=sys.stdin.buffer, outstream=sys.stdout, runlimit=0, verbose=True, metastream=sys.stderr):
    if isinstance(instream,str):
        instream=io.BytesIO(stdin.encode())
    if runlimit==0:
        runlimit=float('inf')
    steps = 0
    while steps<runlimit:
        try:
            print(sim5(mem,instream),end='',file=outstream)
            if mem[0]==0:
                break
            steps += 1
        except KeyboardInterrupt:
            if verbose:
                print(f"Killed after {steps} steps",file=metastream)
            return
    else:
        if verbose:
            print("Timed Out", file=metastream)
        return
    if verbose:
        print(f"Finished in {steps} steps", file=metastream)
    return
def main():
    import os
    import argparse
    parser = argparse.ArgumentParser(description='Run a program on the 5vm.')
    parser.add_argument("--max-steps", type=int, default=0,
            help='Maximum run steps (default: 0 = no limit)')
    parser.add_argument("--verbose", '-v', action='store_true')
    parser.add_argument("program", type=argparse.FileType('rb'), default=sys.stdin.buffer, nargs='?',
            help='Program file (default: stdin)')
    args = parser.parse_args()
    vm5(kh32decode(args.program.read()),instream=sys.stdin.buffer,outstream=sys.stdout,runlimit=args.max_steps,verbose=args.verbose)
    print()
if __name__=='__main__':
    main()
