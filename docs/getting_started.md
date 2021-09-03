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
`Hello,_World! prints
```

This should print the famous "Hello, World!" when compiled and run in the 5vm.

To compile and run the code, run the following in the terminal:

```
fithc -s -o hello.bin hello.fth
5vm hello.bin
```

## Words in Fith

The fith language is based around the concept of words. Words are 
separated by any form of whitespase, and can be just about any 
non-whitespace charachters, with only a few exceptions.

The fith baselib defines some words for us, including the `prints`
word used in the previous example. We can also define our own
words like this:

```
:newword `This_is_a_word prints ;
newword
```

The definition is started with a colon and the word we are defining.
We then give the words to execute, and end the definition with a
semicolon.

## The Stack

Fith words generally perform operations on something called the stack.
The stack is a space in memory where we can push data to the top or
pull data off the top. To push a value onto the stack, we just give
that value. For example:

```
1 2 3 print cr print cr print
```

The word `print` pops the top value off the stack and prints it as a
number. The word `cr` prints a new line. When we run this code, we
should see the following output:

```
3
2
1
```

The numbers are printed in reverse, because the last number to be
pushed is the first to be popped off the top.

## Memory

It is not enough to deal with the stack. We also need to be able to
store things in memory. For that, we have the words `!` and `@`.
The following code stores a value in a variable and prints it out:

```
42 answer !
answer @ print
```

## Arithmetic

The baselib provides us with some arithmetic operations as well.
Here are some examples:

```
1 2 + print
6 2 - print
12 3 / print
3 4 * print
1 2 < boolprint
3 4 > boolprint
5 5 = boolprint
```

## Flow control

The last important aspect of fith is flow control. Fith has the
special words `if` and `else`, but they may act differently from
other languages you may have used. An example is below:

```
1 2 > if `1>2 else `1!>2 ; prints
1 2 < if `1<2 else `1!<2 ; prints
```

As you can see, the condition comes before the word `if` and the
statement is closed with a semicolon.

## Comments

Comments in fith start with the word `/*` and end with the word `*/`.
These must be written with space on both sides.
