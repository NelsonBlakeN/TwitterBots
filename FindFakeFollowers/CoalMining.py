from InstagramAPI import InstagramAPI
from pprint import pprint

import insta_creds as ic

FILENAME = "insta_token.txt"

def main():
    follower_list()

def follower_list():
    insta = ic.insta
    insta.login()

    # Get a list of all followers
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
        return

    print "Finished collecting all", len(followers), "followers"

    # Check if any are following less than 5 people
    # (and that one is the target, for redundancy)
    for u in followers:
        print u['username']
        insta.searchUsername(u['username']) # Rate limit caps at 100 / hr
        if insta.LastResponse.status_code == 429:
            print "Hit rate limit when searching usernames."
            return
        user = insta.LastJson['user']
        if user['following_count'] < 5:
            # If a suspicious account is found, report/block it
            # insta.block(user['pk'])
            print "Suspicious account found"

# def get_creds(test=False):
#     if False:
#         file = open(FILENAME, 'r')
#         return file.readline()
#         # return "4307299325.7efde7b.58681b38682641d589a4f49872b8aa45"
#     else:
#         return "blakenelson19", "Tamu2019"

if __name__ == "__main__":
    main()

