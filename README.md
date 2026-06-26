# C# OOP Fundamentals Study Notes

This repository contains a very small C# console project built as a study exercise for Object-Oriented Programming (OOP).

The idea is simple:

- keep the code short
- keep the example easy to understand
- connect each OOP concept to a real piece of code
- make the project useful for interview preparation

The project uses a Dragon Ball theme so the example feels more memorable and less abstract.

## Project Goal

This project is not meant to be a production application.

It is meant to teach, in one small example, these core ideas:

- class
- object
- instance
- method
- field
- property
- encapsulation
- abstraction
- interface
- inheritance
- polymorphism
- composition
- dependency
- dependency injection

## Project Story

The program models a tiny battle scene:

- `Fighter` is the general base concept
- `Saiyan` and `Namekian` are specific fighter types
- `Technique` represents a move such as `Kamehameha`
- `BattleArena` coordinates what happens
- `IMessageWriter` defines how messages are written
- `ConsoleMessageWriter` writes those messages to the terminal

When the program runs, it creates fighters, applies damage to one of them, and then prints each fighter's turn.

## High-Level Design

At a conceptual level, the project works like this:

1. The program starts in `Main`.
2. It creates a message writer.
3. It creates two fighters: one `Saiyan` and one `Namekian`.
4. It creates a `BattleArena`.
5. The `BattleArena` receives the writer through its constructor.
6. The arena asks each fighter to introduce itself and attack.
7. The result is printed to the console.

This small flow is enough to demonstrate multiple OOP concepts in a realistic way.

## The Main Classes

### `IMessageWriter`

This is an interface.

Its job is to define a contract:

"Any class that implements me must know how to write a message."

It does not say how the message is written.
It only says that the behavior must exist.

### `ConsoleMessageWriter`

This is a concrete class that implements `IMessageWriter`.

Its job is simple:

- receive a string
- print it using `Console.WriteLine`

This is useful because the rest of the program depends on the interface, not directly on the console.

### `Fighter`

This is an abstract base class.

It represents the common idea of a fighter:

- a fighter has a `Name`
- a fighter has a `PowerLevel`
- a fighter has internal `energy`
- a fighter can take damage
- a fighter can introduce itself
- a fighter must have some kind of attack

It is abstract because it is not meant to represent one exact fighter type by itself.

### `Saiyan`

This class inherits from `Fighter`.

It adds its own identity and behavior:

- it is a fighter
- it has a favorite technique
- it overrides how it introduces itself
- it provides its own implementation of `Attack`

### `Namekian`

This is another class that inherits from `Fighter`.

It shares the common `Fighter` structure, but has a different attack behavior.

### `Technique`

This is a small support class.

It represents data about a combat technique:

- the technique name
- the damage value

This class is important because it helps demonstrate composition.

### `BattleArena`

This class coordinates the interaction.

It does not care whether the fighter is a `Saiyan` or a `Namekian`.
It only cares that it receives a `Fighter`.

It also depends on `IMessageWriter` so it can display messages.

This makes the design more flexible and easier to explain in an interview.

## OOP Concepts Explained

### 1. Class

A class is a blueprint.

It describes what an object will have and what it can do.

Examples in this project:

- `Fighter`
- `Saiyan`
- `Namekian`
- `Technique`
- `BattleArena`

### 2. Object

An object is a real thing created from a class.

Examples:

- `goku`
- `piccolo`
- `arena`
- `writer`

### 3. Instance

An instance is another word for object.

If you say:

"`goku` is an instance of `Saiyan`"

that means:

"`goku` is an object created from the `Saiyan` class"

### 4. Method

A method is an action.

Examples:

- `TakeDamage()`
- `GetEnergy()`
- `Introduce()`
- `Attack()`
- `ShowTurn()`
- `Write()`

### 5. Field

A field is internal stored data inside a class.

Example:

- `private int energy;`

This is the fighter's internal energy value.

### 6. Property

A property is a controlled way to expose data.

Examples:

- `Name`
- `PowerLevel`
- `FavoriteTechnique`
- `Damage`

Properties are common in C# because they allow controlled access to data.

### 7. Encapsulation

Encapsulation means protecting internal state and controlling access to it.

Example in this project:

- `energy` is private
- outside code cannot directly set `energy`
- instead, the object exposes methods like `TakeDamage()` and `GetEnergy()`

This prevents invalid or careless changes from outside the class.

### 8. Abstraction

Abstraction means focusing on the important idea and hiding unnecessary details.

`Fighter` is a good example:

- every fighter has shared characteristics
- every fighter must be able to attack
- but the exact attack is left to child classes

This lets us model the general concept first and the specific details later.

### 9. Interface

An interface is a contract.

`IMessageWriter` says:

- there must be a `Write(string message)` method

It does not contain the actual console logic.
The implementation is provided by `ConsoleMessageWriter`.

### 10. Inheritance

Inheritance means one class builds on another class.

Examples:

- `Saiyan : Fighter`
- `Namekian : Fighter`

This means:

- a `Saiyan` is a `Fighter`
- a `Namekian` is a `Fighter`

They inherit shared logic from the base class.

### 11. Polymorphism

Polymorphism means one base type can refer to different concrete objects, and each object can behave differently.

Examples:

- `Fighter goku = new Saiyan("Goku", 9000);`
- `Fighter piccolo = new Namekian("Piccolo", 7000);`

Both variables are typed as `Fighter`, but the real objects are different.

So when the program calls:

- `fighter.Introduce()`
- `fighter.Attack()`

the result depends on the actual object behind the variable.

### 12. Composition

Composition means one object is built using another object as a part of itself.

Example:

- `Saiyan` has a `Technique`

This means the `Saiyan` object contains another object inside it.

This is a "has-a" relationship.

### 13. Dependency

A dependency is something a class needs in order to do its job.

Example:

- `BattleArena` needs a message writer

Without a writer, it cannot display messages.

### 14. Dependency Injection

Dependency injection means the dependency is given to the class from outside instead of being created inside the class.

Example:

- `BattleArena` receives `IMessageWriter` in its constructor

This is better than hardcoding `ConsoleMessageWriter` inside `BattleArena`, because it keeps the class more flexible and easier to test.

## Important C# Keywords Used In This Project

### `using`

Imports a namespace so we can use its types more easily.

Example:

- `using System;`

### `public`

Accessible from anywhere.

Used when something should be visible outside the class.

### `private`

Accessible only inside the same class.

Used to protect internal data.

### `protected`

Accessible inside the class and also inside child classes.

Used here for the base class constructor.

### `class`

Defines a blueprint for objects.

### `interface`

Defines a contract that classes can implement.

### `abstract`

Marks a class or method as incomplete on purpose.

- an abstract class cannot be instantiated directly
- an abstract method must be implemented by child classes

### `virtual`

Marks a method as replaceable by child classes.

### `override`

Replaces inherited behavior from a base class.

### `static`

Belongs to the class itself, not to a specific object.

`Main` is static because the program must be able to start without first creating a `Program` object.

### `void`

Means the method returns nothing.

### `string`

Represents text.

### `int`

Represents a whole number.

### `new`

Creates an object from a class.

Examples:

- `new Saiyan(...)`
- `new Namekian(...)`
- `new Technique(...)`

### `return`

Sends a value back from a method.

### `base`

Refers to the parent class part of the current object.

Examples:

- `base(name, powerLevel)` calls the parent constructor
- `base.Introduce()` calls the parent implementation of a method

### `this`

Refers to the current object.

Example:

- `this.writer = writer;`

The left side refers to the field inside the object.
The right side refers to the constructor parameter.

### `readonly`

Means a field can be assigned only once, usually in the constructor.

### `get`

Allows reading a property value.

### `set`

Allows changing a property value.

### `private set`

Means:

- outside code can read the property
- only the class itself can modify it

## Relationship Summary

These are the key relationships in the project:

- `Saiyan` is a `Fighter`
- `Namekian` is a `Fighter`
- `Saiyan` has a `Technique`
- `BattleArena` depends on `IMessageWriter`
- `ConsoleMessageWriter` implements `IMessageWriter`

This gives you strong interview language:

- inheritance = "is-a" relationship
- composition = "has-a" relationship
- dependency = "needs-a" relationship

## Why This Design Is Good For Learning

This project is useful for study because:

- it is short enough to understand in one sitting
- it uses common interview vocabulary
- it shows both theory and code
- it demonstrates base class design
- it demonstrates interfaces
- it demonstrates polymorphism in a practical way
- it introduces dependency injection without a large framework

## Interview-Friendly Explanations

You can use these short definitions in a technical interview.

### What is a class?

A class is a blueprint that defines data and behavior for objects.

### What is an object?

An object is a real instance created from a class.

### What is a method?

A method is an action an object can perform.

### What is encapsulation?

Encapsulation means protecting internal state and exposing controlled access to it.

### What is abstraction?

Abstraction means modeling the essential idea while hiding unnecessary detail.

### What is inheritance?

Inheritance allows a child class to reuse and extend a parent class.

### What is polymorphism?

Polymorphism allows one base type to represent different concrete objects, each with its own behavior.

### What is composition?

Composition means building one object using another object as a part of it.

### What is dependency injection?

Dependency injection means a class receives what it needs from outside instead of creating it internally.

## Suggested Study Routine

To learn this project well, follow this order:

1. Read the comments in `Program.cs`.
2. Retype the code yourself instead of only reading it.
3. Run the program and confirm the output.
4. Explain each class out loud in your own words.
5. Remove the comments and rewrite the program from memory.
6. Change names and attacks to prove you really understand it.
7. Add one more fighter type, such as `Human`.

## Small Practice Ideas

Try these after you understand the base version:

- change `Goku` to `Vegeta`
- change the favorite technique to `Final Flash`
- add a `Human` class for `Krillin`
- add a second message writer that prints uppercase text
- add a healing method to `Fighter`

## Final Takeaway

This project is small on purpose.

Its value is not in complexity.
Its value is that it gives you one clean place to understand the most common OOP ideas in C#:

- shared behavior through a base class
- specialized behavior through child classes
- contracts through interfaces
- flexible design through dependency injection
- safe data handling through encapsulation

If you can explain this project clearly, modify it comfortably, and rewrite it without looking too much, you will have a strong foundation for a C# OOP technical interview.
