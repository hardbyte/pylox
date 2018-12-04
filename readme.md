This is my attempt to create a compliant lox implementation using the 
[rpython translation toolchain](https://rpython.readthedocs.io) to get
a native & hopefully JIT compiled lox interpreter.

This isn't anywhere done but is rather my journey following the low level C 
guide from Bob Nystrom ([@munificentbob](https://twitter.com/munificentbob)) on 
[craftinginterpreters.com](https://www.craftinginterpreters.com/chunks-of-bytecode.html)


## Running under python

This lox should be runnable using `python2` or `pypy` (with `rpython` as the only dependency):

    python2 -m lox [program.lox]

### Example

    pypy -m lox examples/simple_add.lox
    debug: runFile called with: examples/simple_add.lox
    232.0
    debug: INTERPRET_OK

Note you will be dropped into a _repl_ session if you don't provide a lox script to
execute.


## Translation using the rpython toolchain

The real fun is asking `rpython` to compile to an executable:

    rpython --opt=2 lox/target.py

Now run `targetpylox-c`:

    ./targetpylox-c [program.lox]

Example:

    $ ./lox-c examples/lots_of_basic_calculations.lox 
    3.191743


### A tracing JIT

I've added the most basic annotation required for rpython to add its tracing JIT. 
However this is pretty untested and takes a couple of minutes to compile.

    rpython --opt=jit lox/targetpylox.py


## Current State

Currently an over-engineered basic calculator.

    ./lox-c
    Welcome to pylox
    https://github.com/hardbyte/pylox
    > 3 + 4 * ((1/(2 * 3 * 4)) + (1/(4 * 5 * 6)) - (1/(6 * 7 * 8)))
    3.188095
    > (1/256 + 2/512) > 2/128
    false
    > "hello" + " world"
    hello world

