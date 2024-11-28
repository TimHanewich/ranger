using System;
using Spectre.Console;
using Azure;
using Azure.Storage;
using Azure.Storage.Queues;
using Azure.Storage.Queues.Models;
using System.Threading.Tasks;

namespace RangerCommand
{
    public class Program
    {
        public static void Main(string[] args)
        {
            MainAsync().Wait();
        }

        public static async Task MainAsync()
        {
            //Ask what to do
            SelectionPrompt<string> sp = new SelectionPrompt<string>();
            sp.Title("What do you want to do?");
            sp.AddChoice("Monitor, receive, and show incoming messages in the queue");
            sp.AddChoice("Send commands to Ranger");
            string selected = AnsiConsole.Prompt<string>(sp);

            //Handle what to do
            if (selected == "Monitor, receive, and show incoming messages in the queue")
            {
                
                //Authenticate to Azure Queue Storage
                QueueClient qc = new QueueClient(GetAzureConnectionString(), "c2r");
                AnsiConsole.Markup("Checking if queue '[blue]" + "c2r" + "[/]' exists... ");
                if (await qc.ExistsAsync())
                {
                    AnsiConsole.MarkupLine("[green]it exists![/]");
                }
                else
                {
                    AnsiConsole.MarkupLine("[yellow]it does not exist![/]");
                    AnsiConsole.Markup("Creating queue '[blue]c2r[/]'... ");
                    await qc.ExistsAsync();
                    AnsiConsole.MarkupLine("[green]created[/]!");
                }

                //Clear messages
                AnsiConsole.Markup("Clearing messages in queue... ");
                await qc.ClearMessagesAsync();
                AnsiConsole.MarkupLine("[green]cleared![/]");
                
            }
            else if (selected == "Send commands to Ranger")
            {
                Console.WriteLine("Not done yet.");
            }
            else
            {
                Console.WriteLine("I'm sorry, I do not know how to handle that!");
            }
        }




        private static string GetAzureConnectionString()
        {
            string PathToTxtFile = Path.Combine(Directory.GetCurrentDirectory(), "..", "azure_connection_string.txt");
            if (System.IO.File.Exists(PathToTxtFile) == false)
            {
                throw new Exception("Unable to get Azure Storage Connection String! azure_connection_string.txt does not exist!");
            }
            string ToReturn = System.IO.File.ReadAllText(PathToTxtFile);
            return ToReturn;
        }
    }
}