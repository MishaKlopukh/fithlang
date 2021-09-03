# Baselib Reference

The Fith Baselib defines many useful and even essential words to
be used in fith programs. The source code can be found 
[here](https://github.com/MishaKlopukh/fithlang/blob/main/fith/baselib.fth).

## `!` - Memory Store

Pops an address off the stack, then pops a value off the stack.
Stores the value in memory at the address.

Example:
```
10 place ! /* Stores value 10 in place */
```

## `@` - Memory Retrieve

Pops an address off the stack. Pushes the value of memory
at that address.

Example:
```
place @ /* Retrieves the value of place */
```

## `.` - Output

Pops a value off the stack. Outputs it as a charachter.

Example:
```
65 . /* Outputs capital A */
```

## `cr` - Carriage Return

Outputs a newline.

Example:
```
`line prints
cr
`break prints
```

## `,` - Input

Inputs a single charachter.

Example:
```
, . /* Inputs and prints a single charachter */
```

## `dup` - Duplicate

Duplicates the top value of the stack.

Example:
```
10 dup print cr print
```

## `op` - Memory Mapped Operation

Pops an instruction address, operand a, and operand b from
the stack. Pushes the result of the operation.

Example:
```
6 2 5 op print /* Computes 6 - 2 */
```

## `call` - Call Function

Pops a memory address. Calls the function at that address.

Example:
```
99 @print call /* Prints 99 */
```

## `pop` - Pop stack

Discards the top item of the stack.

Example:
```
5 2 pop print /* prints 5 */
```

## `+`, `-`, `*`, `/`, and `%` - Arithmetic Ops

Perform arithmetic ops on the top 2 values of the stack. 
The word `/` performs floor division. 

Example:
```
1 2 + print /* 1 + 2 = 3 */
cr
5 2 - print /* 5 - 2 = 3 */
cr
5 2 * print /* 5 - 2 = 10 */
cr
5 2 / print /* 5 / 2 = 2 */
cr
7 4 % print /* 7 % 4 = 3 */
```

## `<`, `>`, and `=` - Comparison Ops

Perform comparison ops on the top 2 values of the stack.

Example:
```
1 2 > boolprint
cr
1 2 = boolprint
cr
2 3 < boolprint
```

## `swap` - Swap

Swaps the top two items on the stack.

Example:
```
1 2 swap print print
```

## `print` - Print Integer

Prints value off top of stack as positive or negative
base-10 integer.

Example:
```
15 print
cr
-120 print
```

## `boolprint` - Print Boolean

Prints whether the top value is true or false.

Example:
```
1 2 > boolprint
cr
3 3 = boolprint
```

## `prints` - Print String

Prints the stack elements as charachters until 0 appears
on the stack.

Example:
```
`Hello prints /* Print Hello */
cr
0 67 66 65 prints /* Print ABC */
```

## `input` - Input Number

Inputs a decimal number, terminated by newline.

Example:
```
input print
```
