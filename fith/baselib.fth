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
:+ 4 op ;
:- 5 op ;
:* 6 op ;
:/ 7 op ;
:> 8 op 1 - ;
:< 9 op 1 - ;
:% temp1 ! dup temp1 @ / temp1 @ * - ;
:swap temp1 ! temp2 ! temp1 @ temp2 @ ;
:print dup 0 < if 45 . -1 * ; dup 9 > if dup 10 / print 10 % ; 48 + . ; /* print a number */
