# Getting Started with Fith

Learning Fith is very easy. The language is made to be as simple
as possible, but there are still some things even experienced
programmers may find strange.

## Installing Fith

Fith and its tools are written in Python 3. To install them,
run the following:

```
pip3 install fithlang
```

This will install the Fith suite as a python library, as well as
install the following scripts:

- fithc: the fith compiler
- 5asm: the 5ir assembler
- 5vm: the 5vm itself

## A Basic Example: Hello World

Write the following code in `hello.fth`:

```
`Hello . . . . .
```

This should print the word "Hello" when compiled and run in the 5vm.

To compile and run the code, run the following in the terminal:

```
fithc -s -o hello.bin hello.fth
5vm hello.bin
```

## Words in Fith

The fith language is based around the concept of words. Words are 
separated by any form of whitespase, and can be just about any 
non-whitespace charachters, with only a few exceptions.

The fith baselib defines some words for us, including the `.` word
used in the previous example. 
