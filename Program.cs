using System; // Allows to use Console.WriteLine

public interface IMessageWriter // public: accessible from anywhere
// interface: a contract / promise. It says: "whoever implements me must have these members
{
    void Write(string mesage);
    // void: return nothing
    // Write: method name
    // string: text
    // message: parameter name
    // This means: there must be a method called Write that receives text
}

public class ConsoleMessageWriter : IMessageWriter // class: blueprint for objects
// : means "implements" here, because ImessageWriter is an interface
{
    public void Write(string message) // This class is forced to provide this method because the interface requires it
    {
        Console.WriteLine(message); // Console.WriteLine prints message in the terminal
    }
}

public abstract class Fighter
// bastract: incomplete base class
// You cannot do "new Fighter(...) directly
// It is meant to be parent for other classess
// This is a good example of ABSTRACTION: Describe the idea of a fighter in a general way
{
    private int energy;
    // private: only this class cand directly access it
    // int: whole number
    // this is a FIELD or ATTRIBUTE
    // this is also ENCAPSULATION: the internal state is protected from outside direct access.

    public string Name { get; private set; }
    // This is a PROPERTY
    // public: other code can see it
    // string: text
    // get: other code can read it
    // private set: only this class can change it
    // this is controlled access to data

    public int PowerLevel { get; private set; }
    // Another property
    // outside code can read the power level
    // but cannot change it directly

    protected Fighter(string name, int powerlevel)
    // This is the CONSTRUCTOR of Fighter
    // A constructor builds / initializes an object
    // protected: this class and child classes can use it
    // "name" and "powerlevel": are input values
    {
        Name = name; // Save the rereceived name into the Name property
        PowerLevel = powerlevel; // Save receivded power level
        energy = 100; // Every fighter starts with 100 energy
    }

    public void TakeDamage(int amount)
    // Public method: other code can call it
    // Receives how much damage to apply
    {
        energy -= amount;
        // Same as: energy = energy - amount;
        // Reduce the internal energy

        if (energy < 0)
        // if energy goes below zero...
        {
            energy = 0;
            // keep it at 0.
            // This protects the object from invalid state
        }
    }

    public int GetEnergy()
    // METHOD that gives outside code a safe way to know the energy
    {
        return energy;
        // return: send a value back to whoever called the method        
    }

    public virtual string Introduce()
    // Virtual: Chidl classes may replace this behavior
    // returns a text string
    {
        return $"I am {Name} and my power level is {PowerLevel}.";
        // the $ is string interpolation
        // It lets us insert variables inside a string using {}
    }

    public abstract string Attack();
    // abstract method: no body here
    // This forces every child class to define its own attack
    // Again, this is ABSTRACTION
    // every fighter must attack
    // but the exact attack depends on the child class
}

//

public class Technique
// A simple class to represent a fighter technique
{
    public string Name { get; private set; } // Technique name, like "Kamehameha
    public int Damage { get; private set; } // How much damage the technique deals

    public Technique(string name, int damage)
    // Constructor for Technique objects
    {
        Name = name; // Save the name
        Damage = damage; // Save the damage
    }
}

//

public class Saiyan : Fighter
// Saiyan: inherits from Fighter
// This is INHERITANCE
// A Saiyan is a Fighter
{
    public Technique FavoriteTechnique { get; private set; }
    // A Saiyan has a Technique
    // This is COMPOSITION: A class is built using other classess as intern parts
    // A Saiyan has a Technique object

    public Saiyan(string name, int powerLevel) : base(name, powerLevel)
    // base: calls the parent constructor
    // We pass the values to Fighter so it can initialize shared data
    {
        FavoriteTechnique = new Technique("Kamehameha", 30);
        // new: create an OBJECT / INSTANCE from a class
        // Here we create a Technique object and store it inside the Saiyan object
    }

    public override string Introduce()
    // override: replace inherited virtual behavior
    {
        return base.Introduce() + " I am a Saiyan";
        // base.Introduce(): calls the parent version first
        // then we add extra text
    }

    public override string Attack()
    // Saiyan specific attack behavior
    {
        return $"{Name} uses {FavoriteTechnique.Name} and deals {FavoriteTechnique.Damage} damage";
    }
}

//

public class Namekian : Fighter
// Another child class
// A Namekian is also a FIGHTER
{
    public Namekian(string name, int powerLevel) : base(name, powerLevel) // Reuse the Fighter constructor
    {

    }

    public override string Attack()
    // Namekian specific attack behavior
    {
        return $"{Name} fires an energy blast.";
    }
}

public class BattleArena
// This class will coordinate what happens in the console
{
    private readonly IMessageWriter writer;
    // This is a FIELD storing a dependency
    // readonly: it can be assigned once
    // Usually in the constructor
    // DEPENDENCY means: BattleArena needs something else to do its job
    // Here, it needs something that can write messages

    public BattleArena(IMessageWriter writer)
    // The dependency arrives from outside
    // This is DEPENDENCY INJECTION
    // More specifically: constructor injection
    {
        this.writer = writer;
        // this: means "the current object"
        // Left side = the field inside the object
        // Right side = the parameter received by the constructor
    }

    public void ShowTurn(Fighter fighter)
    // Receives any object whose type is Fighter or any child of fighter
    {
        writer.Write(fighter.Introduce());
        // POLYMORPHISM happens here
        // figher is typed as Fighter
        // but the real object could be a Saiyan or a Namekian
        // Each one can answer differently

        writer.Write(fighter.Attack());
        // Same method call shape, different behavior depending on the real object

        writer.Write($"Current energy: {fighter.GetEnergy()}");
        // Show the current energy in a safe way through a method
    }
}

public class Program
// Main class of the application
{
    public static void Main()
    // Program entry point: execution starts here
    // public: accessible from outside
    // static: belongs to the class itself
    // void: return nothing
    // Main: special method name recognized by C#
    {
        IMessageWriter writer = new ConsoleMessageWriter();
        // Variable type = interface type
        // Real object = ConsoleMessageWriter
        // This is useful because code depends on the contract
        // not on one rigid concrete class

        Fighter goku = new Saiyan("Goku", 9000);
        // Fighter: variable type
        // new Saiyan = actual object created
        // goku: is an OBJECT / INSTANCE
        // This is also POLYMORPHISM
        // a Fighter variable can hold a Saiyan Object

        Fighter piccolo = new Namekian("Piccolo", 7000);
        // Another OBJECT / INSTANCE
        // Variable type is Fighter, real object is Namekian

        piccolo.TakeDamage(20);
        // We call a METHOD on the object
        // Piccolo loses 20 energy, going from 100 to 80

        BattleArena arena = new BattleArena(writer);
        // We create a BattleArena object
        // We INJECT its dependency ("writer") from outside

        arena.ShowTurn(goku);
        // Arena shows Goku's turn

        Console.WriteLine();
        // Blank line just to make the console output easier to read

        arena.ShowTurn(piccolo);
        // Arena shows Piccolo's turn
    }
}


