:! [ /* Pops address, value off of stack, stores value in address */
    :sp +1 -1 +8 /* Grab address */
    :1 2 :sp 1 /* Subtract 1 from stack pointer */
    5 +1 -1 -1 /* put value */
    5 1 5 :sp /* decrement the stack pointer */
] ;
:@ [ /* Pops address off of stack, pushes memory contents at that address */
    :sp +6 :sp +1 -1 +1 -1 -1
] ;
:. 12 ! ; /* output a charachter */
:, 11 @ ; /* input a charachter */
:dup [ /* duplicate top stack item */
    :sp +1 -1 +16 :sp +1 -1 +11
    :1 2 :sp 1 4 :sp
    :sp +2 +2 -1 -1 -1
] ;
:op [ /* perform memop: pop inst, operand a, operand b, push result */
    :sp +1 -1 +35 :sp +1 -1 +31  /* Grab operation */
    :1 2 :sp 1 5 :sp  /* decrement the stack pointer */
    :sp +1 -1 +17 :sp +1 -1 +14  /* Grab operand */
    :1 2 :sp 1 5 :sp  /* decrement the stack pointer */
    :sp +1 -1 1  /* Grab operand */
    +2 2 -1 -1 :sp +2 -1 -1  /* perform operation and push */
] ;
:call [
    :fp +2 +2 -1 +11 +10 /* Push return address to function stack */
    :1 2 :fp 1 4 :fp /* increment the function stack pointer */
    :sp +1 -1 +9 /* Get word addr from stack */
    :1 2 :sp 1 5 :sp /* decrement the stack pointer */
    +2 0 -1 /* Jump to word */
] ;
:pop [
    :1 2 :sp 1 5 :sp /* decrement stack pointer */
] ;
:+ 4 op ;
:- 5 op ;
:* 6 op ;
:/ 7 op ;
:> 8 op ;
:< 9 op ;
:= 10 op ;
:not if -1 else 0 ; ;
:% _temp1 ! dup _temp1 @ / _temp1 @ * - ;
:swap _temp1 ! _temp2 ! _temp1 @ _temp2 @ ;
:print dup 0 < if 45 . -1 * ; dup 9 > if dup 10 / print 10 % ; 48 + . ; /* print a number */
:boolprint if `T else `F ; . ; /* Print a boolean */
:prints dup 0 > if . prints else pop ; ; /* Print a string ending in 0 */
:input , dup 47 > if 48 - 10 * input + else pop 10 / ; ; /* Input a number */
