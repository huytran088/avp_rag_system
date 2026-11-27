[^1]: Last updated: Nov. 27, 2026. Checked against the AVP app's grammar (`app/hooks/interpreter/Pseudocode.g4`) and trace interpreter, which are the source of truth.
## Purpose

This page[^1] describes the syntax of our custom pseudocode language, AVP. It's designed to be intuitive for students who already have experience in a common language such as Python or JavaScript. Therefore, you may be familiar with many parts of AVP, however there are still significant differences.

If you were looking for details on the AVP metadata syntax or information on the interpreter, they are covered [here](https://gitlab.csi.miamioh.edu/2026-senior-design-projects/algorithm-visualization-project/algorithm-visualization-project/-/wikis/Product-Documentation/Product-Designs/Metadata-Syntax) and [here](https://github.com/huytran088/algorithm-visualization-project/blob/main/docs/ARCHITECTURE.md) respectively. A short summary of the metadata directives is under [Visual directives](#visual-directives) below.

## Formatting
By convention, variables and functions are written in `snake_case`, and function names start with a capital letter (`Bubble_Sort`). Other formats such as `camelCase` are acceptable, but for the purposes of these reference materials, `snake_case` is used. Also by convention, `bagel` and `toast` are used in place of `foo` and `bar`. When more names are required for a demonstration, more bread types are used as variable names.

To write a comment inside of your program, use the familiar `//` (or `#`) to denote the start of your comment. This disregards anything else written after it for that line of code. Remember this if word wrapping is enabled.

Each statement goes on its own line; newlines separate statements. You can also put several statements on one line with `;` in between (`bagel = 1; toast = 2`).

By convention, indentation is 4 spaces. Unlike Python, the interpreter ignores indentation (spaces and tabs are skipped), because every block ends with an `end` keyword, but keep to 4 spaces so code stays readable.

AVP files are saved with the extension `.avp`. The **first line must be a title comment** followed by a blank line (`// Bubble Sort`): the app shows it as the page title and strips it before running the code. Strings may contain any characters (`"brötchen"` is fine), but names must be ASCII: a non-ASCII letter in a name is a syntax error ("token recognition error").

## Variables
Variables are used to store and manage data in your script. In AVP, variables are created dynamically, so you don't have to assign types manually.

A name starts with an English letter (`A-z`) or an underscore (`_`), followed by any letters, arabic numerals (`0-9`) and underscores. Symbols other than these are not accepted. [Reserved words](#glossary-of-reserved-words) cannot be used as names.

### Assignment
To assign a variable to a value, use the familiar `=` operator. In the example below, the variable `bagel` is set to a value of `8`
```
bagel = 8
```
As detailed below, assignments are performed dynamically and can occur several times for the same variable. This way, the value of any variable reflects its most recent assignment:
```
bagel = 8        // set value of bagel to 8
bagel = "pizza"  // set value of bagel to "pizza"
```

To add to or subtract from a variable, use `+=` and `-=`. There are no `*=`, `/=`, `%=`, `++` or `--` operators:
```
bagel = 8
bagel += 2       // bagel is now 10
bagel -= 1       // bagel is now 9
bagel = bagel * 2  // use the long form for other operators
```

If you are unsure or do not need to assign a variable to anything, variables can be assigned to `Null`. Null variables indicate the absence of any data for that reference.

### Types
In AVP, variables are one of three types at any given time: `Number`, `Boolean`, or `String`, or they are `Null`.

+ **Number**: an integer (e.g., `19`) or a floating-point number (e.g, `2.71`)
+ **Boolean**: A binary value, which must be either `False` or `True` (`false` and `true` also work)
+ **String**: a sequence of characters enclosed in double quotes (ex: "hello")
+ **Null**: `Null` (or `null`), the absence of a value

AVP will **not** check types for you. Operations on values of different types don't give an error; they follow JavaScript's rules and usually give a meaningless result, so keep the types the same:

```
bagel = 1.9
toast = True

if (bagel <= toast):  // no error, but the result (False) is meaningless
    ...
end if
```

To make a string, simply assign a variable to your desired string of characters encased in quotes. `+` joins two strings:
```
bagel = "abc"
toast = bagel + "123"   // toast = "abc123"
```

### Arrays
There is another special kind of a variable called an array. This allows you to have one name that stores multiple values that can be retrieved later. Think of them how you might a List in Python:
```
bagel = arr[2, 5, 3, 9, 10]  // assign 'bagel' to an array of numbers
```

Arrays can only be created on the right side of an assignment, as above. An array literal can't be passed to a function, returned or used in an expression directly: assign it to a variable first, then use the variable.
```
Sort(arr[3, 1, 2])         // Invalid!
toast = arr[3, 1, 2]
Sort(toast)                // valid
```

Array literals hold **numbers**. Any other entry (a Boolean, a string, `Null`) is turned into an invalid number and shows as `null`:
```
toast = arr[42, 2.71, True, "brot"]   // toast = [42, 2.71, null, null]
```

For every entry entered into an array, a **copy** of what it represents is created at the specified location. So if you were to insert a variable `toast` into an array `bagel`:
```
toast = 10
bagel = arr[9, toast, 11]  // set bagel to [9, 10, 11]
toast = True               // bagel[1] would still be equal to 10, whereas toast is now of boolean value True
```

An array itself is not copied, though. Passing an array to a function, or assigning it to another name, shares the same array, so a change made through one name shows through the other:
```
bagel = arr[1, 2, 3]
toast = bagel
toast[0] = 9               // bagel is now [9, 2, 3] too
```

Read and write entries with `bagel[i]`. Indices start at 0 and are rounded down, so `bagel[1.7]` is `bagel[1]`.
<br>

Creating large arrays of sequential numbers can be quite tedious. This can be simplified by referencing the sequential set of whole Numbers between two Numbers. In AVP this is performed using `to`:
```
toast = arr[1, 2, 3, 4, 5]
bagel = arr[1 to 5]            // bagel = [1, 2, 3, 4, 5]
```

You can also use a variable to do this:
```
bagel = 6
toast = arr[3 to bagel]    // toast = [3, 4, 5, 6]
```

Both ends are rounded down to whole numbers:
```
biscuit = arr[2.27 to 4]       // biscuit = [2, 3, 4]
```

<br>

If a specific array size is needed, you can create an array by its size. It is filled with `0`:
```
bagel = arr(5)    // bagel = [0, 0, 0, 0, 0]
```

You can also specify what value to fill it with (any type works here):
```
toast = arr(4, "jam")    // toast = ["jam", "jam", "jam", "jam"]
bagel = arr(2, False)    // bagel = [False, False]
```

An empty array is written `arr[]` (requires an app version with empty array support):
```
crumb = arr[]            // crumb = []
```

The built-in functions for arrays are `length(bagel)` (or `size(bagel)`), the number of entries, and `swap(bagel[i], bagel[j])`, which exchanges two entries (and animates the swap in the visualizer). There is no built-in to append to an array, slice it (`bagel[1:3]` does not exist) or find its minimum or maximum: write a function with `fun` instead.

## Operations
Operations are the fundamental steps taken to compare variables or modify their data.

There are two kinds of operations in AVP: arithmetic and comparative.

### Arithmetic
These are your familiar `+`, `-`, `*`, `/` operators, use them as you would in Python/JS. `/` is real division (`7 / 2` is `3.5`); to get a whole number, for example for an array index, use the built-in `floor()`: `floor(7 / 2)` is `3`. `%` gives the remainder (`7 % 3` is `1`).

There's also `**`, which may look strange if you're unfamiliar with Python. This is the "power of" operator, that will produce the exponent of a base to a given power. Sort of like the Math.Pow() method you may be familiar with but as a primitive operator.
```
bagel = 5 ** 2  // set bagel to 25
```
Arithmetic operations are performed using the standard [Order of Operations](https://en.wikipedia.org/wiki/Order_of_operations): `**` first, then `*`, `/` and `%`, then `+` and `-` (`2 + 3 * 4 ** 2` is `50`). One difference from Python: a leading minus binds tighter than `**`, so `-2 ** 2` is `4`. Write `-(2 ** 2)` if you mean `-4`.

### Comparative
To compare data with each other, you can use one of the following: `==`, `!=`, `<`, `<=`, `>`, `>=`, `and`, `or`.
As expected, these can be used in the format `a x b` where `x` is any operator previously listed.
Also notice how both the `and` and `or` operators are spelled out instead of a c-style syntax you might be used to. There is no `not` operator: compare with `== False` instead.

Compare pieces of data (i.e. variables) of the same type. Types are not checked, so the example below runs, but its result is meaningless:
```
bagel = True
toast = "butter"
if (bagel or toast):
    ...
end if
```

Use `and` and `or` only on Booleans (the results of comparisons). On other values they follow JavaScript's rules and return one of the values, not `True` or `False`: here `bagel or toast` is `2`.
```
bagel = 2
toast = 1
if (bagel or toast):
    ...
end if
```

You can chain these operations together using parentheses, which will evaluate from the inside out.

```
// using the same defs from last example
bagel = 2
toast = 1
biscuit = 2
if ((bagel < toast) or (bagel <= biscuit)):
    ...
end if
```
In the above example: bagel will be compared to toast before biscuit, then the results of that will be compared.

## Blocks
In order to perform complex branching or iteration, it's helpful to utilize AVP's Block structure. Conceptually, "blocks" are a set of predefined instructions that allow a variety of operations given specific conditions and settings. You can create branches through `if` and `else` statements, and repeat code using loops and functions, all of which are covered soon.

### Structure
Fundamentally, blocks consist of three parts: declaration, body, and terminator (the `end` line that closes the block).

Blocks are created through a declaration, which identifies the operation and its arguments. Declarations[^2] begin with a statement, then parameters/condition encased in parentheses, finished by a colon. The body contains the set of instructions that are performed, written on the lines directly under the declaration (indented by convention). Lastly, the block is terminated with an `end`, which just signifies the end.
```
some_declaration (argument_1):
    ...
end some_declaration
```
[^2]: For illustrative purposes, assume "some_declaration ()" is a valid AVP block declaration; it does not exist otherwise.

Using this structure, you can see how it can be turned into valid AVP:
```
while (bagel < 5):
    bagel = bagel + 1
end while
```

The parentheses around a condition are optional for `if` and `while` (`if bagel < 5:`), but required for the regular `for` loop and the `while` of a do-while loop.

### What is scope?
Scope is the area where your data's identifier (i.e. variable name) can be recognized. In AVP, scope is per **function call**, not per block:

+ Variables assigned outside of any function are in the main scope.
+ Each function call has its own scope, holding its parameters and the variables it assigns. They disappear when the call returns.
+ `if` blocks and loops do **not** create a scope: a variable assigned inside them can be used after the block, in the same function (or in the main scope).
+ A function can **not** read variables from the main scope. Pass what it needs as parameters, and get results back with `return`.

```
bagel = 10

if (bagel == 10):
    toast = 4
end if

biscuit = toast            // valid: if-blocks share the surrounding scope

fun some_fn():
    return bagel           // bagel isn't visible inside the function: returns Null
end fun

fun better_fn(bagel):
    return bagel           // pass it in instead
end fun
```

### Exiting a Scope
If needed, you can forcefully exit a loop by using `break`. When used, the process will "break out" of the innermost loop it's inside of, skipping the remainder of that loop. Used directly in a function body (outside any loop), `break` ends the function, which then returns `Null`.

To skip only the rest of the current iteration and continue with the next one, use `continue`.

Exiting a function via `return` is detailed separately below.

## Declarations
Now that you have learned the structure of blocks and declarations, this section provides detail on some that we've built into the language.

### if
Simplest condition operator. When the boolean value is satisfied, the block is entered and executed.
```
if (<condition>):
    ...
end if
```

if-blocks can also be "chained" together via `else if` (or `elseif`) to act on different conditions accordingly:
```
if (bagel < toast):
    ...
else if (bagel == toast):
    ...
else:
    ...
end if      // only a single 'end if' is needed
```

### while
These loops will repeat until their condition is no longer true.
```
while (bagel):
    ...
end while
```

A do-while loop runs its body first and checks the condition afterwards, so the body always runs at least once. It ends with the `while` line instead of an `end` keyword:
```
do:
    bagel += 1
while (bagel < 5)
```

### for
In many cases when a for-loop is necessary (such as iterating through an array), you would want to use the "for-each" style:
```
toast = arr[1, 2, 3, 4, 5]
for bagel in toast:
    ...
end for
```
In this example, `bagel` is set to each **value** of the array in turn: `1`, then `2`, and so on.

There is also a "regular" for-loop for extended algorithms. Separate its three parts with `;` or `,`:
```
for (bagel = 1; bagel < 10; bagel += 1):
    ...
end for
```

So that a mistake can't freeze the page, every loop stops after 1000 iterations.

## Functions
The backbone of AVP! Such as in other languages, functions allow you to re-use parts of your code with a simple call:

```
fun Some_Fn():        // declare a function Some_Fn()
    bagel = 1
end fun

Some_Fn()
```

A program only runs what is called, so every program needs a call outside of any function, usually saving the result: `result = Some_Fn()`.

Functions return `Null` unless a `return <some value>` is explicitly used. To illustrate, consider the example below:
```
fun Some_Fn(bagel):
    if (bagel < 3):
        return True
    end if

    // if bagel isn't less than three, return Null implicitly
end fun
```
A function that changes an array it was given (like an in-place sort) usually ends with `return` of that array, so the call's result is the array.
<br>

Define functions in the main scope. A `fun` inside another function also works (it is defined once the outer function runs), but it is harder to read:
```
fun Some_Fn():          // define functions at the top level
    ...
end fun
```
<br>

There is no "overloading" feature in AVP: if two functions have the same name, the one defined last replaces the other.

Only these built-in functions exist: `length(a)` and `size(a)` (number of entries), `floor(x)` (round down) and `swap(a[i], a[j])` (exchange two entries). Calling any other function that isn't defined with `fun`, such as `print`, `len`, `min` or `max`, is an error.

## Visual directives
Directives tell the visualizer what to draw. They have the form `@name<param, ...>` and are placed **at the start of a line, before the statement** they annotate, or before a function parameter. Several can be chained on one line (`@a<..> @b<..> bagel = 1`), but a directive cannot sit on a line by itself.

Each parameter must be a single number, `"string"`, bare word, or variable name (resolved to the variable's current numeric value). Expressions are not allowed: write `k = i + 1` on the line before, then `@mark<k, ...>`.

| Directive | Parameters | Effect |
| --- | --- | --- |
| `@init<table>` | `table` | Show this array parameter as a table |
| `@mark<index, kind, color>` | kind: `outline` (default) / `highlight` / `text`; color: e.g. `yellow` (default), `green`, `red` | Mark a cell |
| `@log<level, "text">` or `@log<"text">` | level: `info` (default), `warn`, `error` | Show a message |
| `@insert<index, value>` | | Insert a cell |
| `@delete<index>` | | Remove a cell |
| `@update<index, value>` | | Change a cell value |
| `@swap<i, j>` | | Animate a swap |
| `@sort<name>` | | Show the array as sorted |

The table shows one array. The call that first shows it keeps it until that call returns, so `@init` on another array (for example a temporary copy) during that call is ignored. Writes, swaps and marks are only drawn for the array in the table; other arrays update only in the variables list. Work in place on the shown array (pass it with low/high indices) for the clearest visualization.

```
fun Linear_Search(@init<table> bagel, toast):
    for (i = 0; i < length(bagel); i += 1):
        @mark<i, outline, yellow> if (bagel[i] == toast):
            return i
        end if
    end for
    return -1
end fun
```

## Glossary of Reserved Words
AVP has a set of "reserved words" such that they cannot be used in any capacity other than as determined by the language design. In other words: functions and variables cannot--under any circumstances--use these words alone as names. For your convenience, these words and their meanings are detailed below.

| Word    | Definition |
| ------- | ---------- |
| `Null` / `null` | A special value that marks an absence of usable data. |
| `True` / `true` | Constant Boolean value. |
| `False` / `false` | Constant Boolean value. |
| `or`    | Logic operator that combines two Boolean expressions. Results in `True` if *at least one* expression is true, otherwise it resolves as `False`. |
| `and`   | Logic operator which combines two Boolean expressions. Results in `True` if *both* expressions are true, `False` otherwise. |
| `if`    | Evaluates a boolean condition, executes the provided block when True, otherwise the block is skipped. |
| `else`  | Branches from a prior if-statement when the condition provided is False. `else if` (or `elseif`) adds another condition. |
| `while` | Loop which is executed given a single boolean condition. Will continue looping until that condition is false. Also ends a do-while loop. |
| `do`    | Starts a do-while loop, whose body runs before its condition is checked. |
| `for`   | Loop that directly iterates over the values of an array. Or set a start variable with a condition, then update that variable every iteration. |
| `in`    | Separates the loop variable from the array in a for-each loop (`for bagel in toast:`). |
| `to`    | Iteratively select whole numbers between values provided. These can either be constants or the value of a Number variable. |
| `arr`   | Creates an array: `arr[...]`, `arr[a to b]` or `arr(size, fill)`. |
| `fun`   | Function declaration. Allows you to write reusable code and call through a provided name and arguments. |
| `break` | Exit the innermost loop, skipping the rest of it. Directly in a function body, it ends the function. |
| `continue` | Skip the rest of the current loop iteration and start the next one. |
| `return` | Return a specified variable or constant as the result of a function, which is then terminated. |
| `end`   | Marks the end of a block. Must be followed by the type of declaration which it is ending (`end if`, `end while`, `end for`, `end fun`). |
