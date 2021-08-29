def kh32decode(bitstr):
    assert bitstr[:4] == b'kh32', "Missing magic number"
    values = []
    for i in range(4,len(bitstr),4):
        values.append(int.from_bytes(bitstr[i:i+4],'little',signed=True))
    return values
def sim5(mem, stdin=0):
    output=''
    mem[0] += 2
    mem[4]=mem[1]+mem[2]
    mem[5]=mem[1]-mem[2]
    mem[6]=mem[1]*mem[2]
    mem[7]=mem[1]//mem[2] if mem[2]!=0 else 0
    mem[8]=int(mem[1]>mem[2])
    mem[9]=int(mem[1]<mem[2])
    mem[10]=int(mem[1]==mem[2])
    mem[11]=stdin
    mem[12]=0
    mem[13]=int(not mem[3])
    mem[14]=mem[1]^mem[2]
    mem[15]=mem[1] if mem[3] else mem[2]
    while True:
        try:
            movfrom = mem[mem[0]-2]
            movto = mem[mem[0]-1]
            if movfrom!=movto:
                mem[movto]=mem[movfrom]
        except IndexError:
            mem += [0]*64
            continue
        break
    if mem[12]!=0:
        try:
            output=chr(mem[12])
        except:
            pass
    return mem, output
def vm5(mem, runlimit=0, verbose=True):
    stdout=''
    if runlimit==0:
        runlimit=float('inf')
    steps = 0
    while steps<runlimit:
        try:
            mem, output = sim5(mem)
            stdout += output
            if mem[0]==0:
                break
            steps += 1
        except KeyboardInterrupt:
            if verbose:
                print(f"Killed after {steps} steps")
            return stdout
    else:
        if verbose:
            print("Timed Out")
        return stdout
    if verbose:
        print(f"Finished in {steps} steps")
    return stdout
def main():
    import os
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Run a program on the 5vm.')
    parser.add_argument("--max-steps", type=int, default=0,
            help='Maximum run steps (default: 0 = no limit)')
    parser.add_argument("--verbose", '-v', action='store_true')
    parser.add_argument("program", type=argparse.FileType('rb'), default=sys.stdin.buffer, nargs='?',
            help='Program file (default: stdin)')
    args = parser.parse_args()
    print(vm5(kh32decode(args.program.read()),runlimit=args.max_steps,verbose=args.verbose))
if __name__=='__main__':
    main()
