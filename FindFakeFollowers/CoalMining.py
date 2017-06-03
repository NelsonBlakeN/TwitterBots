from pprint import pprint
import time
from InstagramAPI import InstagramAPI

import insta_creds as ic

FILENAME = "insta_token.txt"

insta = ic.insta
insta.login()

def coal_mining():

    # Store all users following the person
    followers = get_all_followers()
    num_found = len(followers)
    if num_found < 1:
        print "No followers were found."
    else:
        print "Finished collecting all", len(followers), "followers"

    # Check if any are following less than 5 people
    # (and that one is the target, for redundancy)
    count = 0;
    for u in followers:
        # print u['username']
        try:
            insta.searchUsername(u['username']) # Rate limit caps at 100 / hr
            if insta.LastResponse.status_code == 429:
                print "Hit rate limit when searching usernames."
                return
            user = insta.LastJson['user']
            count += 1
            print(str(count) + ": " + str(user['username']))
            if user['following_count'] < 5:
                # If a suspicious account is found, report/block it
                # insta.block(user['pk'])
                print "\tSuspicious account found"
        except Exception, e:
            print(e)
            pass
        time.sleep(90);  # Space out API hits to avoid rate limiting

# Return a list of all followers
def get_all_followers():
    insta.searchUsername("egcarlin")
    insta_id = insta.LastJson['user']['pk']

    insta.getUserFollowers(insta_id)
    followers = insta.LastJson['users']
    max_id = insta.LastJson['next_max_id']
    while insta.LastResponse.status_code != 429:
        try:
            insta.getUserFollowers(insta_id, max_id)
            followers += insta.LastJson['users']
            max_id = insta.LastJson['next_max_id']
        except KeyError, e:
            break
    if insta.LastResponse.status_code == 429:
        print "Hit rate limit when collection followers."
        return []
    return followers

if __name__ == "__main__":
    coal_mining()

