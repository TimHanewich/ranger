# put any keys/secrets here

azure_queue_url_send:str = "https://rangercomms.queue.core.windows.net/r2c" # the queue that ranger should use to transmit messages to command ("r2c"), i.e. "https://rangercomms.queue.core.windows.net/r2c"
azure_queue_url_recv:str = "https://rangercomms.queue.core.windows.net/c2r" # the queue that ranger should use to receive messages from command ("c2r"), i.e. "https://rangercomms.queue.core.windows.net/c2r"
azure_queue_sas:str = "" # SAS token to the azure storage account with sufficient privileges