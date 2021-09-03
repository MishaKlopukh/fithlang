# 5ir Reference

The fith compiler uses a very simple intermediary format called
`5ir`. It is simply a text abstraction over the `5vm` binary
format which supports position names and offsets. 

In `5ir`, values are space separated and can take the following
forms:

- Positive or negative integers are literal numbers or addresses.
- Numbers begining with `+` are relative addresses, and are used relative to the current machine code address. Negative relative addresses are given by `+-`.
- Labels are symbols starting with `:` and refer to locations given by label lines.
- Labels can have offsets by adding `+` and a positive or negative offset after the label.
- Label definitions are symbols starting with `.` and are not included in the machine code.

The `5ir` format supports comments starting with `/*` and ending
in `*/`

The contents of literal insertions are also in the `5ir` format.
