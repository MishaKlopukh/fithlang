# 5vm Docs
The 5vm has only one native instruction, move.
Other instructions can be performed using memory mapping
and special memory locations.

## Default Memory Mapped Functions
Memory 0 to 15 is reserved for special purposes as follows:
*   0: The instruction pointer. Increments by 2 at every step unless overwritten.
*   1: Register A
*   2: Register B
*   3: Register C
*   4: A + B
*   5: A - B
*   6: A * B
*   7: A // B
*   8: A > B
*   9: A < B
*   10: A == B
*   11: Input Register, Not currently implemented in the reference 5vm.
*   12: Output Register. Outputs ascii when nonzero, clears every step.
*   13: logical not C
*   14: A bitwise xor B
*   15: A if C!=0 else B

## Execution
Execution of code begins at memory location 16. 
At every step, the memory at the location pointed to by the current instruction 
(whose address is pointed to by the instruction pointer) is placed in the memory 
pointed to by the memory location after the current instruction. Memory mapped
functions are performed if necessary, and the instruction pointer is incremented
by 2. To halt machine execution, 0 is placed in memory location 1, and the
instruction pointer is set to 0.
