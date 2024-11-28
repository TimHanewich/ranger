using System;
using Spectre.Console;

namespace RangerCommand
{
    public class Program
    {
        public static void Main(string[] args)
        {
            while (true)
            {
                Console.Write("What is your name? > ");
                string? input = Console.ReadLine();
                if (input != null)
                {
                    Console.WriteLine("Hello, " + input + "!");
                }
                else
                {
                    Console.WriteLine("Hey, give me your name!");
                }
            }
        }
    }
}