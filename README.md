BelLog
======

Tools for the four-valued logic programming language BelLog.

For details of the language see: http://dx.doi.org/10.3929/ethz-a-010045530

Syntax

```
<rule>    := <atom> :- <query>
<query>   := <value> | <atom> | !(<query>) | ~(<query>) | (<query> ^ ... ^ <query>])
<atom>    := <pred>[(<arg> ^ ... <arg>)]?
<pred>    := [a-z][a-z|A-Z|0-9]*
<arg>     := <const> | <var>
<const>   := [a-z][a-z|A-Z|0-9]*
<var>     := [A-Z][a-z|A-Z|0-9]*
<value>   := true | false | bot | top
```
