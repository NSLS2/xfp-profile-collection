# Function to run BestEffortCallback to print a table and show a live plot
def start_bec():
    bec = BestEffortCallback()
    RE.subscribe(bec)
    print("BestEffortCallback enabled!")

def set_user_md():
    '''
    Function to define user / experiment values as persistant metadata
    Collect using input at the prompt.
    '''
    proposal_num = input("Enter the proposal number: ")
    saf_num = input("Enter the SAF number: ")
    pi_name = input("Enter last name of the PI: ")
    user_name = input("Enter last name of the lead experimenter: ")
    RE.md['proposal'] = proposal_num
    RE.md['SAF'] = saf_num
    RE.md['PI'] = pi_name
    RE.md['experimenter'] = user_name
    print(f"\nSet proposal number to {proposal_num} and SAF number to {saf_num}.")
    print(f"Set the PI to {pi_name} and lead experimenter to {user_name}.")

def clear_user_md():
    '''Clear user metadata and set to setup/commissioning values'''
    #Current proposal/SAF valid for CY2023
    inp_choice = input("Are you sure you want to clear metadata (y/n)? ")
    if inp_choice=='y' or inp_choice=='yes':
        RE.md['proposal'] = '311955'
        RE.md['SAF'] = '310464'
        RE.md['PI'] = 'Farquhar'
        RE.md['experimenter'] = 'Farquhar'
        print("Reset metadata keys to commissioning proposal.")
    else:
        print("\nNo change made! Current persistant metadata is:")
        print(RE.md)
