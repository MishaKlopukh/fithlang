def fithc(fith, *includes, locoffset=0):
    """Compiles a fith program for the 5vm"""
    fith = '\n'.join(includes+(fith,))
    words = {'_start': []} # Dictionary of fith words
    fvars = [] # List of variables
    def call(word): # Call a fith word
        return [
            ':fp','+2','+2',-1,'+11','+10', # Push return address to function stack
            ':1',2,':fp',1,4,':fp', # increment the function stack pointer
            '+2',0,':'+word # Jump to word
        ]
    def call_cond(word1, word2): # Call one of two fith words based on condition on the stack
        return [
            ':fp','+2','+2',-1,'+40','+39', # Push return address to function stack
            ':1',2,':fp',1,4,':fp', # increment the function stack pointer
            ':sp','+1',-1,'+19', # Grab condition
            ':1',2,':sp',1,5,':sp', # decrement the stack pointer
            0,1,'+2',2,14,14,4,1,'+2',2,'+9','+8',-1,3,15,0, # execute conditional jump over call to else
            '+2',0,':'+word1, # Jump to word1
            '+2',0,':'+word2 # Jump to word2
        ]
    def push(word): # Push a value to the stack
        nonlocal fvars
        try:
            word = int(word)
        except:
            if word.startswith("`"):
                return sum((push(ord(char)) for char in word[-1:0:-1]),[])
            if not word in fvars:
                fvars += [word]
            word = ':'+word
        return [
            ':1',2,':sp',1,4,':sp', # increment the stack pointer
            ':sp','+2','+2',-1,word,word # Push word to stack
        ]
    locix = locoffset-1 # Lambda (conditional) index
    literal = None # Machine code definition
    commenting = False
    defining = [words['_start']] # stack of word definitions: start at the main loop
    for word in fith.split(): # fith processes words separately, loop through each word
        if commenting:
            if word == '*/':
                commenting = False
        elif word == '/*':
            commenting = True
        elif literal is not None: # literal 5vm code insertion
            if word == ']':
                defining[-1] += literal
                literal = None
            else:
                literal += [word]
        elif word == '[': # Literal insertion
            literal = []
        elif word == ';': # Pop definition
            defining.pop()
        elif word.lower() == 'if': # Special word: IF
            locix += 1
            defining[-1] += call_cond(f'loc{locix}',f'loc{locix}.else')
            words[f'loc{locix}'], words[f'loc{locix}.else'] = [], []
            defining.append(words[f'loc{locix}'])
        elif word.lower() == 'else': # Special word: ELSE
            defining[-1] = words[f'loc{locix}.else']
        elif word.lower() == 'do': # Special word: DO (lambda)
            locix += 1
            defining[-1] += call(f'loc{locix}')
            words[f'loc{locix}'] = []
            defining.append(words[f'loc{locix}'])
        elif word.lower() == 'cloop': # Special word: CLOOP (repeat if)
            if not f'loc{locix}.else' in words:
                words[f'loc{locix}.else'] = []
            defining[-1] += call_cond(f'loc{locix}',f'loc{locix}.else')
        elif word.startswith(':'): # New word definition
            words[word[1:].lower()] = []
            defining.append(words[word[1:].lower()])
        elif word.lower() in words: # Call a function word
            defining[-1] += call(word.lower())
        else: # Push a value to the stack
           defining[-1] += push(word)
    words['_start'] += ['+4',1,'+2',0,0] # Halt machine
    fir = ""
    for var in fvars: # Add variables to machine
        fir += f'.{var}\n0\n'
    for word in words: # Add word definitions to machine
        wval = ''.join(str(ins)+('\n' if idx%30==29 else ' ') for idx,ins in enumerate(words[word]))
        fir += f'.{word}\n{wval}\n:1 2 :fp 1 5 :fp :fp +1 -1 0\n'
    return fir
def main():
    import os
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Compile a fith program.')
    parser.add_argument("--include", '-i', action="extend", nargs="+", type=argparse.FileType('r'), default=[],
            help='Include a fith file')
    parser.add_argument("--output", '-o', type=argparse.FileType('wb'), default=sys.stdout.buffer,
            help='Output file (default: stdout)')
    parser.add_argument("--no-include-baselib", '--nostd', dest='include_baselib', action='store_false',
            help='Do not include the fith baselib')
    parser.add_argument("--assemble", '-s', action='store_true',
            help='Assemble the code into a 5vm binary')
    parser.add_argument("file", type=argparse.FileType('r'), default='-', nargs='?',
            help='Input file (default: stdin)')
    args = parser.parse_args()
    includes = []
    for file in ([open(os.path.join(os.path.dirname(__file__),'baselib.fth'))] if args.include_baselib else []) + args.include:
        includes += [file.read()]
    out = fithc(args.file.read(), *includes)
    if args.assemble:
        from fith import assemble
        args.output.write(assemble(out))
    else:
        args.output.write(out.encode())
if __name__=='__main__':
    main()
