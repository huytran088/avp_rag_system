## Purpose
[^1]: Last updated: 11/4/2025 

This page[^1] describes the syntax of our custom pseudocode language, AVP. It's designed to be intuitive for students who already have experience in a common language such as Python or JavaScript. Therefore, you may be familiar with many parts of AVP, however there are still significant differences.
 
If you were looking for details on the AVP metadata syntax or information on the interpreter, they are covered [here](https://gitlab.csi.miamioh.edu/2026-senior-design-projects/algorithm-visualization-project/algorithm-visualization-project/-/wikis/Product-Documentation/Product-Designs/Metadata-Syntax) and [here]() respectively.

## Formatting
By convention, variables and functions are written in `snake_case`. Other formats such as `camelCase` are acceptable, but for the purposes of these reference materials, `snake_case` is used. Also by convention, `bagel` and `toast` are used in place of `foo` and `bar`. When more names are required for a demoonstration, more bread types are used as variable names.

To write a comment inside of your program, use the familiar `//` to denote the start of your comment. This disregards anything else written after it for that line of code.. Remember this if word wrapping is enabled. 

Like CPython, indentations in AVP are strictly 4-spaced. Tab characters are not acceptable under any circumstances; otherwise, this will lead to parse errors.

AVP files are saved in ASCII format with the extention `.avp`. The interpreter *can* work with UTF-8, but will only recognize ASCII characters; Non-ASCII characters will cause a `ParseError` **(TODO: VERIFY)**.

## Variables
Variables are used to store and manage data in your script. In AVP, variables are created dynamically, so you don't have to assign types manually.

At a minimum, variable names must contain at least one English letter (`A-z`). Once this requirement is satisfied, an acceptable name can include arabic numerals (`0-9)` and underscores (`_`). Symbols other than these are ignored **(TODO: 'ignored' is vague)**. 

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

If you are unsure or do not need to assign a variable to anything, variables can be assigned to `Null`. This is particularly useful in [scoping](), but can also be used in other ways. Null variables indicate the absense of any data for that reference.

### Types
In AVP, variables are one of three types at any given time: `Number`, `Boolean`, or `String`.

+ **Number**: considered to be an integer (e.g., `19`) or a floating-point number (e.g, `2.71`)
+ **Boolean**: A binary value, which must be either `False` or `True`.
+ **String**: a sequence of characters enclosed in double quotes (ex: "hello")

While AVP is intended to be flexible, it will **not** automatically convert types for you. When performing operations (such as comparisons), variables **must be of the same type**.

```
bagel = 1.9
toast = True

if (bagel <= toast):  // Invalid comparison!
    ...
end if
```

To make a string, simply assign a variable to your desired string of characters encased in quotes:
```
bagel = "abc"
toast = "abc123"
```

### Arrays
There is another special kind of a variable called an array. This allows you to have one name that stores multiple values that can be retrieved later. Think of them how you might a List in Python:
```
bagel = [2, 5, 3, 9, 10]  // assign 'bagel' to an array of numbers
```

Like variables, arrays are flexible with their types. What this means is that not every entry in an array is required to be of the same type:
```
toast = [42, 2.71, True, "brot"]
bagel = [64, True]
```

For every entry entered into an array, a **copy** of what it represents is created at the specified location. So if you were to insert a variable `bagel` into an array `toast`:
```
toast = 10
bagel = [9, toast, 11]  // set bagel to [9, 10, 11]
toast = True            // bagel[1] would still be equal to 10, whereas toast is now of boolean value True
```
<br>

Creating large arrays of sequential numbers can be quite tedious. This can be simplified by referencing the sequential set of whole Numbers between two Numbers. In AVP this is performed using `to`:
```
toast = [1, 2, 3, 4, 5]
bagel = [1 to 5]            // bagel = [1, 2, 3, 4, 5]
```
You can also use a variable to do this, provided it's a non-floating point Number:
```
bagel = 6
toast = [3 to bagel]    // toast = [3, 4, 5, 6]
```
<br>

**TODO: Creating a array by specifing the size of it. How it's filled isn't specified well!**
<!-- MUST CLARIFY with DESIGN TEAM
ISSUE is lack of detail for this section on design doc! The existing section:
- specifies how to create empty arrays of specified size
- does not say how to fill an array of a size with the same value at each index
- gives bad syntax:
    - `a1 = arr(100)`
        - this implies that there is a FUNCTION that creates this array. CONCERN: may confuse user?
        - why use arr to preface it?
    - `a2 = arr[1 to 5]`
        - if this is a function creating an array, why use brackets to specify args?? Parentheses have been decided on for specifying arguments in functions previously, why is this different?

How this can be resolved:
- use `bagel = [1 to 5]` for dynamically assigning indices
- remove arr() syntax
- To create an array filled with a single value, use braces. The first argument specifies how many spaces to make, the second specifies what to fill them with:
    ```
    bagel = {5, 1}      // bagel = [1, 1, 1, 1, 1]
    toast = {5}         // toast = [Null, Null, Null, Null, Null]
    ``` 
-->

## Operations
Operations are the fundamental steps taken to compare variables or modify their data. 

There are two kinds of operations in AVP: arithmetic and comparative.

### Arithmetic 
These are your familiar `+`, `-`, `*`, `/` operators, use them as you would in Python/JS.

There's also `**`, which may look strange if you're unfamiliar with Python. This is the "power of" operator, that will produce the exponent of a base to a given power. Sort of like the Math.Pow() method you may be familiar with but as a primitive operator.
```
bagel = 5 ** 2  // set bagel to 25
```
Arithmetic operations are performed using the standard [Order of Operations](https://en.wikipedia.org/wiki/Order_of_operations) **TODO: verify**

### Comparative
To compare data with each other, you can use one of the following: `==`, `<`, `<=`, `>`, `>=`, `and`, `or`. 
As expected, these can be used in the format `a x b` where `x` is any operator previously listed.
Also notice how both the `and` and `or` operators are spelled out instead of a c-style syntax you might be used to.

To compare pieces of data (i.e. variables) with each other, they must be of the same type. So performing operations like below are invalid:
```
bagel = True
toast = "butter"
if (bagel or toast):
    ...
end if
```

Each comparison will return a boolean value of `True` or `False`, so operations like the following are invalid:
```
bagel = 2
toast = 1
if (bagel or toast):
    ...
end if
```

Since the comparison operators can only compare two data points at once, you can chain these operations together using parentheses, which will evaluate from the inside out.

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
In order to perform complex branching or iteration, it's helpful to utilize AVP's Block structure. Conceptually, "blocks" are a set of predefined instructions that allow a variety of operations given specific conditions and settings. You can create branches through `if` and `else` statments, and repeat code using loops and functions, all of which are covered soon. 

### Structure
<!-- TODO: WTF is terminator? -->
Fundamentally, blocks consist of three parts: declaration, body, terminator.

Blocks are created through a declaration, which identifies the operation and its arguments. Declarations[^2] begin with a statement, then parameters/condition encased in parentheses, finished by a colon. The body contains the set of instructions that are performed, denoted by indented lines directly under the declaration. Lastly, the block is terminated with an `end`, which just signifies the end.
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

### What is scope?
Like many languages, a significant quantity of AVP relies on the concept of "scoping". Simply, scope is the area where your data's identifier (i.e. variable name) can be recognized. **(TODO: EXPAND)**. Each block has its own scope where variables can be assigned and modified, be it inside that one or in a child scope.

Data assigned outside of any block (i.e. global) are considered to be in the main scope, and can be accessed from anywhere in the program. In the example below, _bagel_ can be accessed from anywhere, but _toast_ cannot as it was declared in a different block:
```
bagel = 10

if (bagel == 10):
    toast = 4
    if (bagel < toast):
        toast = toast + 10  // toast was defined in a parent scope, so this is valid
    end if
end fun

if (bagel < 15):
    if (bagel < toast):  // toast isn't defined in this scope, so an error will occur
        ... 
    end if
end fun
```

### Exiting a Scope
<!-- add a reference to this section in loop/function sections -->
If needed, you can forcefully exit a scope by using `break`. When used, the process wil "break out" of whatever function or loop it's inside of, returning to the previous position in the parent scope. Using this will skip the remainder of that loop or function.

Exiting a function via `return` is  detailed separately below.

## Declarations
Now that you have learned the structure of blocks and declarations, this section provides detail on some that we've built into the language.

### if
Simplest condition operator. When the boolean value is satisfied, the block is entered and executed.
```
if (<condition>):
    ...
end if
```

if-blocks can also be "chained" together via `else if` to act on different conditions accordingly:
```
if (bagel < toast):
    ...
else if (bagel == toast):
    ...
else:
    ...
end if
```
Notice how only one `end if` is necessary in this case.

### while
These loops will repeat until their condition is no longer true.
```
while (bagel):
    ...
end while
```

### for
In many cases when a for-loop is necessary (such as iterating through an array), you would want to use the "for-each" style:
```
toast = [1, 2, 3, 4, 5]
for bagel in toast: 
    ...
end for
```
In this example, we are initializing `bagel` to represent the index at the start of the array, for every iteration, bagel increases by one.

There is also a "regular" for-loop for extended algorithms:
```
for bagel = 1, bagel < 10, bagel += 1:
    ...
end for
```

## Functions
The backbone of AVP! Such as in other languages, functions allow you to re-use parts of your code with a simple call:

```
fun some_fn():        // declare a function some_function()
    bagel = 1
end fun

some_fn()
```

By default, functions return `Null`. <!-- TODO: was this ever clarified??? should they be void? --> 
That is, unless a `return <some value>` is explicitly used, a function will *implicitly* return `Null` <!-- conflicting wording? -->.
To illustrate, consider the example below:
```
fun some_fn(bagel):
    if bagel < 3:
        return True
    end if

    // if bagel isn't less than three return Null implicitly
end fun 
```
<br>

<!-- TODO: expand on this basic ahh description? -->
Functions can only be defined in the Main scope.
```
fun some_fn():          // valid function declaration
    fun invalid_fn():   // invalid!
        ...
    end fun
end fun
```
<br>

<!-- TODO: provide example? -->
It should also be mentioned that there is no "overloading" feature in AVP; No two functions can have the same name.


## Glossary of Reserved Words
AVP has a set of "reserved words" such that they cannot be used in any capacity other than as determined by the language design. In other words: functions and variables cannot--under any circumstances--use these words alone as names. For your convenience, these words and their meanings are detailed below.

| Word    | Definition |  | 
| ------- | ---------- | - |
| `Null`  | A special value that marks an absense of usable data. |
| `True`  | Constant Boolean value. |
| `False` | Constant Boolean value.|
| `or`    | Logic operator that combines two Boolean expressions. Results to `True` if *at least one* expression is true, otherwise it resvolves as `False`. |
| `and`   | Logic operator which combines two Boolean expressions. Results to `True` if *both* expressions are true, `False` otherwise. |
| `if`    | Evaluates a boolean condition, executes the provided block when True, otherwise the block is skipped. |
| `else`  | Branches from a prior if-statement when the condition provided is False. |
| `while` | Loop which is executed given a single boolean condition. Will continue looping until that condition is false. |
| `for`   | Loop that directly iterates over an array. Or set a start variable with a condition, then update that variable every iteration. |
| `in`    | used for mark a shared variable when utilizing for-each loops | **TODO: DEFINE THIS PRIOR**// **UPDATE: I think I have?** |
| `to`    | Iteratively select whole numbers between values provided. These can either be constants or the value of a Number variable. |  |
| `fun`   | Function declaration. Allows you to write reusable code and call through a provided name and arguments. | 
| `break` | Terminate the process of a function or loop and return to the parent scope, skipping the remainder of that iteration or call. | **TODO: DEFINE THIS PRIOR BETTER** // **UPDATE: I think I have?**|
| `return` | Return a specified variable or constant as the result of a function, which is then terminated. | 
| `end`   | Marks the end of a block. Must be followed by the type of declaration which it is ending at the same indentation level as that declaration |


