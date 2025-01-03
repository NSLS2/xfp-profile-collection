#Define metadata for user, proposal, and SAF
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
    #Current proposal/SAF valid for CY2024
    inp_choice = input("Are you sure you want to clear metadata (y/n)? ")
    if inp_choice=='y' or inp_choice=='yes':
        RE.md['proposal'] = '317793'
        RE.md['SAF'] = '315353'
        RE.md['PI'] = 'Farquhar'
        RE.md['experimenter'] = 'Farquhar'
        print("Reset metadata keys to commissioning proposal.")
    else:
        print("\nNo change made! Current persistant metadata is:")
        print(RE.md)

#yaml config file read-in function
def load_yamlfile_config(file_path):
    with open(file_path, 'r') as config_file:
        pos_config = yaml.safe_load(config_file)
    return pos_config

#print out a short statement of user metadata during bluesky startup
user_persistant_dict_data = RE.md
print("\nCurrent user metadata values are:")
for key, value in user_persistant_dict_data.items():
    print(f'{key}: {value}')
print("\nNow loading the rest of the startup profile.")

def check_user_md():
    '''Check user metadata dynamically'''
    user_persistant_dict_check = RE.md
    print("Current persistant user metadata values:")
    for key, value in user_persistant_dict_check.items():
        if key != 'scan_id':
            print(f'{key}: {value}')
    print("\nUse set_user_md() to change these values.")


