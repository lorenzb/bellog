# BelLog

Tools for the four-valued logic programming language BelLog.

For details of the language see: http://dx.doi.org/10.3929/ethz-a-010045530

## INSTALL

To use the BelLog interpreter you need to install:
- pexpect: http://pexpect.readthedocs.org/en/latest/
- XSB: http://xsb.sourceforge.net/

Configure the BelLog interpreter with the correct path to your XSB
binary. Edit the file src/config and edit the line
```
'XSB_PATH' : 'path to xsb'
```
where you change **path to xsb** with the path to XSB.

## BELLOG SYNTAX

A **BelLog policy file** is a file that contains one **rule** per line. 
The syntax of policy rules is given below:

```
<rule>      := <atom> :- <query>
<query>     := <value> | <atom> | !<query> | ~<query> | (<query> ^ ... ^ <query>) 
               | (<query> <binary op> <query>)
<binary-op> := -plus- | -times- | -<value>-> 
<atom>      := <pred>[(<arg>, ... , <arg>)]
<pred>      := [a-z][a-z|A-Z|0-9]*
<arg>       := <const> | <var>
<const>     := [a-z][a-z|A-Z|0-9]*
<var>       := [A-Z][a-z|A-Z|0-9]*
<value>     := true | false | bot | top
```

An example of a BelLog policy file is:

```
p(X) :- ( (q(X) -plus- r(X)) -top-> t(X) )
q(a) :- true
r(a) :- false
s(a) :- bot
```


## USAGE

To run the BelLog interpreter type:
```
$ ./src/run.py -i bellog_file -q query
```
where **bellog_file** is a BelLog policy file and **query** is written
using the syntax of query elements; see syntax above.

##### EXAMPLE

```
$ ./src/run.py -i examples/simple.blg -q "p(a)"
```
