#Borrow from  https://github.com/NSLS-II/nsls2api_for_mx/

import httpx

base_url = "https://api-staging.nsls2.bnl.gov"

def get_from_api(url):
    if url:
        response = httpx.get(f"{base_url}/{url}")
        if response.status_code == httpx.codes.OK:
            return response.json()
        raise RuntimeError(f"Failed to get value from {url}. response code: {response.status_code}")
    else:
        raise ValueError("URL cannot be empty")

def get_proposals_from_cycle(cycle):
    return get_from_api(f"proposals/{cycle}")
def get_proposal_info(proposal_id):
    return get_from_api(f"proposal/{proposal_id}")

def get_proposals_for_instrument(cycle, instrument):
    proposals_on_instrument = []
    proposals = get_proposals_from_cycle(cycle)[0]["proposals"]
    for proposal_num in proposals:
        proposal = get_proposal_info(proposal_num)
        if instrument in proposal['instruments']:
            proposals_on_instrument.append(proposal_num)
    return proposals_on_instrument

def inst_proposals_report(cycle, instrument, detail):
    '''
    Queries NSLS-II API for proposals for specified instrument and cycle.
    Detail is one of 'long', 'medium', or 'short'
    Returns report listing proposal number, title, type, and PI
    '''   
    print(f"Retrieving {instrument} proposals for the {cycle} cycle. This may take some time.")
    proposal_list = sorted(get_proposals_for_instrument(cycle, instrument), key=int)
    
    if detail == 'long':
        print(f"\nLong Report of {instrument} proposals for {cycle} cycle")
        for item in proposal_list:
            single_prop = get_proposal_info(item)
            print("\nProposal #:", single_prop['proposal_id'], " Title:", single_prop['title'])
            print("Proposal Type:", single_prop['type'])
            pi_users = [user for user in single_prop['users'] if user['is_pi']]
            for i, user in enumerate(pi_users):
                print(f"Proposal PI: {user['first_name']} {user['last_name']}", end="")
                if i < len(pi_users) - 1:
                    print(",", end=" ")
            print("\nUsers:", end=" ")
            sorted_users = sorted(single_prop['users'], key=lambda x: x['last_name'])
            for i, user in enumerate(sorted_users):
                print(f"\nName: {user['first_name']} {user['last_name']}; ID: ({user['username']} / {user['bnl_id']}); e-mail: {user['email']}", end="")
                if i < len(sorted_users) - 1:
                    print(",", end=" ")
            print(" ")
    
    if detail == 'medium':
        print(f"\nMedium Report of {instrument} proposals for {cycle} cycle")
        for item in proposal_list:
            single_prop = get_proposal_info(item)
            print("\nProposal #:", single_prop['proposal_id'], " Title:", single_prop['title'])
            print("Proposal Type:", single_prop['type'])
            #sometimes this prints out multiple entries for same PI due to data source
            pi_users = [user for user in single_prop['users'] if user['is_pi']]
            for i, user in enumerate(pi_users):
                print(f"Proposal PI: {user['first_name']} {user['last_name']}", end="")
                if i < len(pi_users) - 1:
                    print(",", end=" ")
            print(" ")
    
    if detail == 'short':
        print(f"\nShort Report of {instrument} proposals for {cycle} cycle")
        for item in proposal_list:
            single_prop = get_proposal_info(item)
            print("Proposal #:", single_prop['proposal_id'], " Title:", single_prop['title'])

def api_proposal_report(proposal_num):
    '''
    Retrieve proposal info from NSLS-II API and produce a clean report.
    Takes a single proposal ID as input.
    '''
    single_prop = get_proposal_info(proposal_num)
    print("\nNSLS-II API data for proposal #:", single_prop['proposal_id'])
    print("Proposal Type:", single_prop['type'])
    print("Proposal Title:", single_prop['title'])
    approved_saf_ids = [saf['saf_id'] for saf in single_prop['safs'] if saf['status'] == 'APPROVED']
    print("Beamlines:", single_prop['instruments'])
    print("Cycles:", single_prop['cycles'])
    print("Approved SAFs:", ", ".join(approved_saf_ids))
    sorted_users = sorted(single_prop['users'], key=lambda x: x['last_name'])
    pi_users = [user for user in single_prop['users'] if user['is_pi']]
    for i, user in enumerate(pi_users):
        print(f"Proposal PI: {user['first_name']} {user['last_name']}", end="")
        if i < len(pi_users) - 1:
            print(",", end=" ")
    print(" ")
    print("Proposal Members:")
    for i, user in enumerate(sorted_users):
        print(f"\nName: {user['first_name']} {user['last_name']}; ID: ({user['username']} / {user['bnl_id']}); e-mail: {user['email']}", end="")
        if i < len(sorted_users) - 1:
            print(",", end=" ")
    print(" ")

#Define metadata for user, proposal, and SAF while checking the API
def set_user_md_api():
    '''
    Function to define user / experiment values as persistant metadata
    Retrieve info from NSLS-II API based on collected proposal_id.
    '''
    short_report = input("Retrieve list of proposals (y/n)? ")
    if short_report == 'y':
        cycle_num = input("Which cycle (e.g. '2024-1')? ")
        inst_proposals_report(cycle=cycle_num, instrument='XFP', detail='short')
        print(" ")
    proposal_num = input("Enter the proposal number: ")
    api_proposal_report(proposal_num)
    saf_num = input("\nEnter the SAF number: ")
    pi_name = input("Enter last name of the PI: ")
    user_name = input("Enter last name of the lead experimenter: ")
    RE.md['proposal'] = proposal_num
    RE.md['SAF'] = saf_num
    RE.md['PI'] = pi_name
    RE.md['experimenter'] = user_name
    print(f"\nSet proposal number to {proposal_num} and SAF number to {saf_num}.")
    print(f"Set the PI to {pi_name} and lead experimenter to {user_name}.")