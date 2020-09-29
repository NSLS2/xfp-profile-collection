# Function to run BestEffortCallback to print a table and show a live plot
def start_bec():
    bec = BestEffortCallback()
    RE.subscribe(bec)
    print("BestEffortCallback enabled!")
