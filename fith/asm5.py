def kh32encode(values):
    out = b'kh32'
    for val in values:
        out += val.to_bytes(4,'little',signed=True)
    return out
def assemble(*sections, literal_section = [], extra_symbols = dict(), fs_len=100, ds_len=100):
    machine = [16,0,0,0,0,0,0,0,0,0,1,0,0,-1,0,0,18,0,':_start',1,22,22+fs_len] + (fs_len+ds_len)*[0] + literal_section
    symbols = {'0':17,'1':19,'fp': 20,'sp': 21, '_start': len(machine)}
    symbols.update(extra_symbols)
    for idx,section in enumerate(sections):
        comment = False
        for value in section.split():
            if value[1:4] == 'loc':
                value = f'{value[0]}s{idx}{value[1:]}'
            if comment:
                if value.endswith('*/'):
                    comment = False
                pass
            elif value.startswith('/*'):
                comment = True
            elif value.startswith('.'):
                symbols[value[1:]] = len(machine)
            else:
                machine.append(value)
    for ix,n in enumerate(machine):
        try:
            if isinstance(n,int):
                machine[ix] = n
            elif n.startswith('+'):
                machine[ix] = ix+int(n[1:])
            elif n.startswith(':'):
                if '+' in n and n[1:] not in symbols:
                    machine[ix] = symbols[n[1:].split('+')[0].lower()]+int(n[1:].split('+')[1])
                else:
                    machine[ix] = symbols[n[1:].lower()]
            elif n.startswith('0x'):
                machine[ix] = int(n[2:],16)
            else:
                machine[ix] = int(n)
        except:
            raise RuntimeError(f"Invalid symbol \'{n}\' at position {ix}")
    return kh32encode(machine)
def main():
    import os
    import argparse
    import sys
    parser = argparse.ArgumentParser(description='Assemble 5ir files to a 5vm binary.')
    parser.add_argument("--output", '-o', type=argparse.FileType('wb'), default=sys.stdout.buffer,
            help='Output file (default: stdout)')
    parser.add_argument("--stack-len", type=int, default=100,
            help='Stack length (default: 100)')
    parser.add_argument("--fstack-len", type=int, default=100,
            help='Function stack length (default: 100)')
    parser.add_argument("files", type=argparse.FileType('r'), default='-', nargs="+",
            help='Input file(s) (default: stdin)')
    args = parser.parse_args()
    out = assemble(*[file.read() for file in args.files], fs_len = args.fstack_len, ds_len = args.stack_len)
    args.output.write(out)
if __name__=='__main__':
    main()
