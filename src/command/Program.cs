using System;
using Spectre.Console;
using Azure;
using Azure.Storage;
using Azure.Storage.Queues;
using Azure.Storage.Queues.Models;
using System.Threading.Tasks;
using System.Drawing;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

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
            sp.AddChoice("TEST");
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

                        //Read text and parse as JSON
                        string text = qm.Body.ToString();
                        Console.WriteLine("Received body of length " + text.Length.ToString("#,##0") + " characters.");

                        //Parse as JSON
                        JObject? msg = null;
                        try
                        {
                            msg = JObject.Parse(text);
                        }
                        catch
                        {
                            msg = null;
                        }
                        
                        //If it was JSON, work with it. If not, show an error
                        if (msg != null) //It was JSON! Work with it!
                        {
                            
                            //Is there an "image" property?
                            JProperty? prop_image = msg.Property("image");
                            if (prop_image != null)
                            {
                                AnsiConsole.Markup("Reconstructing image... ");

                                JObject image = (JObject)prop_image.Value;

                                //Get base64
                                string base64 = "";
                                JProperty? prop_base64 = image.Property("base64");
                                if (prop_base64 != null)
                                {
                                    base64 = prop_base64.Value.ToString();
                                }

                                //Get width
                                int width = 0;
                                JProperty? prop_width = image.Property("width");
                                if (prop_width != null)
                                {
                                    width = Convert.ToInt32(prop_width.Value.ToString());
                                }

                                //Get height
                                int height = 0;
                                JProperty? prop_height = image.Property("height");
                                if (prop_height != null)
                                {
                                    height = Convert.ToInt32(prop_height.Value.ToString());
                                }

                                //Reconstruct
                                byte[] bytes = Convert.FromBase64String(base64);
                                Bitmap bm = new Bitmap(width, height);
                                int OnPixel = 0;
                                for (int y = 0; y < 120; y++)
                                {
                                    for (int x = 0; x < 160; x++)
                                    {
                                        System.Drawing.Color c = System.Drawing.Color.FromArgb(255, bytes[OnPixel], bytes[OnPixel], bytes[OnPixel]);
                                        bm.SetPixel(x, y, c);
                                        OnPixel = OnPixel + 1;
                                    }
                                }

                                //Save the image
                                bm.Save(@"C:\Users\timh\Downloads\tah\ranger\image.jpg");

                                //Print that there was an image
                                AnsiConsole.MarkupLine("[green]image unpacked![/]");
                            }

                        }
                        else //It did not parse into JSON correctly.
                        {
                            AnsiConsole.MarkupLine("[red]The message that was received was not successfully parsed into a JSON object.[/] Msg: " + text);
                        }
                        
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
            else if (selected == "TEST")
            {
                //Read base64 and convert
                string b64 = System.IO.File.ReadAllText(@"C:\Users\timh\Downloads\tah\ranger\b64.txt");
                byte[] bytes = Convert.FromBase64String(b64);

                //Reconstruct
                Bitmap bm = new Bitmap(160, 120);
                int OnPixel = 0;
                for (int y = 0; y < 120; y++)
                {
                    for (int x = 0; x < 160; x++)
                    {
                        System.Drawing.Color c = System.Drawing.Color.FromArgb(255, bytes[OnPixel], bytes[OnPixel], bytes[OnPixel]);
                        bm.SetPixel(x, y, c);
                        OnPixel = OnPixel + 1;
                    }
                }

                //Save
                bm.Save(@"C:\Users\timh\Downloads\tah\ranger\image.jpg");
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