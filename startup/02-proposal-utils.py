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
def get_usernames_from_proposal(proposal_id):
    return set(get_from_api(f"proposal/{proposal_id}/usernames")['usernames'])
def get_users_from_proposal(proposal_id):
    return get_from_api(f"proposal/{proposal_id}/users")
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