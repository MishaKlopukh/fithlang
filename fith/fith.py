def fithc(fith, *includes, locoffset=0):
    """Compiles a fith program for the 5vm"""
    fith = '\n'.join(includes+(fith,))
    words = {'_start': []} # Dictionary of fith words
    fvars = {} # List of variables
    def call(word): # Call a fith word
        return ['\n'
            ':fp','+2','+2',-1,'+11','+10', # Push return address to function stack
            ':1',2,':fp',1,4,':fp', # increment the function stack pointer
            '+2',0,':'+word, # Jump to word
            f'/* call({word}) */'
        ]
    def call_cond(word1, word2): # Call one of two fith words based on condition on the stack
        return ['\n'
            ':fp','+2','+2',-1,'+26','+25', # Push return address to function stack
            ':1',2,':fp',1,4,':fp', # increment the function stack pointer
            ':sp','+11', # Grab condition
            ':1',2,':sp',1,5,':sp', # decrement the stack pointer
            '+8',1,'+7',2,-1,3,15,0,':'+word1,':'+word2, # execute conditional jump to word 1 or 2
            f'/* call_cond({word1},{word2}) */'
        ]
    def push(word): # Push a value to the stack
        nonlocal fvars
        try:
            word = int(word)
        except:
            if word.startswith("`"):
                if len(word)>=3:
                    return sum((push(ord(char)) for char in word.replace('_',' ').replace('\\_','_').replace('\\\\n','\n')[-1:0:-1]),push(0))
                else:
                    return push(ord(word[1]))
            try:
                offset = int(word.split('+')[1])
                baseword = word.split('+')[0]
            except:
                offset = 0
                baseword = word
            if word.startswith("@"):
                word = word[1:]
            elif not baseword in fvars:
                fvars[baseword] = offset+1
            elif fvars[baseword] <= offset:
                fvars[baseword] = offset+1
            word = ':'+word
        return ['\n'
            ':1',2,':sp',1,4,':sp', # increment the stack pointer
            ':sp','+2','+2',-1,word,word, # Push word to stack
            f'/* push({word}) */'
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
            literal = ['\n']
        elif word == ';': # Pop definition
            defining[-1] += ['\n:1 2 :fp 1 5 :fp :fp +1 -1 0 /* return */'] # return from function
            defining.pop()
        elif word.lower() == 'if': # Special word: IF
            locix += 1
            defining[-1] += call_cond(f'loc{locix}',f'loc{locix}.else')
            words[f'loc{locix}'], words[f'loc{locix}.else'] = [], []
            defining.append(words[f'loc{locix}'])
        elif word.lower() == 'else': # Special word: ELSE
            defining[-1] += ['\n:1 2 :fp 1 5 :fp :fp +1 -1 0 /* return */'] # return from function
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
    words['_start'] += ['\n''+4',1,'+2',0,0,'/* Halt */'] # Halt machine
    fir = ""
    for var in fvars: # Add variables to machine
        data = ' '.join(['0']*fvars[var])
        fir += f'.{var} /* mem({fvars[var]}) */\n{data}\n\n'
    for word in words: # Add word definitions to machine
        sdword = ' '.join(map(str,words[word])) if words[word] != [] else '\n:1 2 :fp 1 5 :fp :fp +1 -1 0 /* nop return */'
        fir += f'.{word}\n{sdword}\n\n'
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
