import AzureQueue
import settings
import sensitive
import time

qs:AzureQueue.QueueService = AzureQueue.QueueService(sensitive.azure_queue_url_recv, sensitive.azure_queue_sas)

while True:
    msg = qs.receive()
    if msg != None:
        print("Msg received: " + str(msg))
        qs.delete(msg.MessageId, msg.PopReceipt)
        print("Deleted!")
    else:
        print("None!")
    print("Waiting...")
    time.sleep(3.0)
