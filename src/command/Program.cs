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
                QueueClient qc = new QueueClient(GetAzureConnectionString(), "r2c");
                AnsiConsole.Markup("Checking if queue '[blue]" + "r2c" + "[/]' exists... ");
                if (await qc.ExistsAsync())
                {
                    AnsiConsole.MarkupLine("[green]it exists![/]");
                }
                else
                {
                    AnsiConsole.MarkupLine("[yellow]it does not exist![/]");
                    AnsiConsole.Markup("Creating queue '[blue]r2c[/]'... ");
                    await qc.CreateAsync();
                    AnsiConsole.MarkupLine("[green]created[/]!");
                }

                //Clear messages
                AnsiConsole.Markup("Clearing messages in queue... ");
                await qc.ClearMessagesAsync();
                AnsiConsole.MarkupLine("[green]cleared![/]");

                //Infinitely read and show
                Console.WriteLine();
                while (true)
                {
                    QueueMessage qm = await qc.ReceiveMessageAsync(); //Try to read next message
                    if (qm == null) //if there is no new message in the queue
                    {
                        DateTime TimeToCheckAgain = DateTime.UtcNow.AddSeconds(5);
                        while (DateTime.UtcNow < TimeToCheckAgain)
                        {
                            TimeSpan TimeRemainingUntilNextCheck = TimeToCheckAgain - DateTime.UtcNow;
                            Console.Write("\r" + new string(' ', Console.WindowWidth)); //clear out the line
                            AnsiConsole.Markup("\r" + "No message found on last check. Checking again in [bold][blue]" + TimeRemainingUntilNextCheck.TotalSeconds.ToString("#,##0") + " seconds[/][/]... ");
                            await Task.Delay(1000); //wait 1 second
                        }
                    }
                    else //There is a message in the queue! Read it!
                    {
                        Console.WriteLine(); //Go to next line
                        Console.WriteLine(); //Make an empty line

                        string text = qm.Body.ToString();

                        Console.WriteLine("Received: " + text);


                        
                        //Now that we processed the message, delete it
                        AnsiConsole.Markup("Deleting message... ");
                        await qc.DeleteMessageAsync(qm.MessageId, qm.PopReceipt);
                        AnsiConsole.MarkupLine("[green]deleted![/]");
                    }
                }
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
            string PathToTxtFile = Path.Combine(Directory.GetCurrentDirectory(), "azure_connection_string.txt");
            if (System.IO.File.Exists(PathToTxtFile) == false)
            {
                throw new Exception("Unable to get Azure Storage Connection String! azure_connection_string.txt does not exist!");
            }
            string ToReturn = System.IO.File.ReadAllText(PathToTxtFile);
            return ToReturn;
        }
    }
}