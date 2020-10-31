import twitter
import json
import networkx as nx
import matplotlib.pyplot as plt
import sys

import sys
import time
from urllib.error import URLError
from http.client import BadStatusLine


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# Borrowed from Twitter Cookbook... modified to sort by followers
def get_user_profile(twitter_api, screen_names=None, user_ids=None):
    # Must have either screen_name or user_id (logical xor)
    assert (screen_names != None) != (user_ids != None), \
    "Must have screen_names or user_ids, but not both"
    items_to_info = {}
    items = screen_names or user_ids
    while len(items) > 0:
        # Process 100 items at a time per the API specifications for /users/lookup.
        # See http://bit.ly/2Gcjfzr for details.
        items_str = ','.join([str(item) for item in items[:100]])
        items = items[100:]
        if screen_names:
            response = twitter_api.users.lookup(screen_name=items_str)
        else: # user_ids
            response = twitter_api.users.lookup(user_id=items_str)
        for user_info in response:
            items_to_info[user_info['screen_name']] = user_info #changed it to only use screen_name as key
    return sorted(items_to_info, key=lambda user: items_to_info[user]["followers_count"]) #my code, sorted by follower count

# Borrowed from Twitter Cookbook.py
def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw): 
    
    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
    
        if wait_period > 3600: # Seconds
            print('Too many retries. Quitting.', file=sys.stderr)
            raise e
    
        # See https://developer.twitter.com/en/docs/basics/response-codes
        # for common codes
    
        if e.e.code == 401:
            print('Encountered 401 Error (Not Authorized)', file=sys.stderr)
            return None
        elif e.e.code == 404:
            print('Encountered 404 Error (Not Found)', file=sys.stderr)
            return None
        elif e.e.code == 429: 
            print('Encountered 429 Error (Rate Limit Exceeded)', file=sys.stderr)
            if sleep_when_rate_limited:
                print("Retrying in 15 minutes...ZzZ...", file=sys.stderr)
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print('...ZzZ...Awake now and trying again.', file=sys.stderr)
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print('Encountered {0} Error. Retrying in {1} seconds'.format(e.e.code, wait_period), file=sys.stderr)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function
    
    wait_period = 2 
    error_count = 0 

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError as e:
            error_count = 0 
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("URLError encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise
        except BadStatusLine as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("BadStatusLine encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise

def main():
    # Main function
    depth = 0
    pre_graph = {}

    # Step 1: Starting point
    screen_name = 'edmundyu1001' 
    starting_point = twitter_api.users.search(q=screen_name)[0]
    next_queue = [starting_point["screen_name"]] 
    total_nodes = 1
    #crawler taken from slides, adjusted accordingly to get reciprocal friends
    while total_nodes < 100:
        queue, next_queue = next_queue, []
        for handle in queue:
            their_friends = []
            # Step 2: Retrieve his/her friends and followers
            friends, followers = make_twitter_request(twitter_api.friends.ids, screen_name=handle), \
                                    make_twitter_request(twitter_api.followers.ids, screen_name=handle)

            if followers and friends:
                # Step 3: Find reciprocal friends
                friends_ids, followers_ids = friends["ids"], followers["ids"]
                reciprocal_friends = list(set(friends_ids) & set(followers_ids))

                # Step 4: Select 5 most popular friends by followers_count
                users = get_user_profile(twitter_api, user_ids=reciprocal_friends)
                # My code, pops from friends starting from the top of the list
                while users and len(their_friends) < 5:
                    user = users.pop()
                    if user not in pre_graph and user not in next_queue and user not in their_friends:
                        next_queue.append(user)
                        their_friends.append(user)
                        total_nodes += 1
                pre_graph[handle] = their_friends
        # Step 5: Repeat the process until you get 100 friends
        depth += 1
    
    print("At least 100 nodes have been gathered!")
    # Step 6: Create a social network based on the results using Networkx
    G = nx.Graph()
    for user in pre_graph:
        G.add_edges_from([(user, friend) for friend in pre_graph[user]])
    

    # Step 7: Calculate the diameter and average distance of your network
    diameter = nx.diameter(G)
    shortest_paths = nx.shortest_path_length(G)
    distances = 0
    pairs = set()
    for node, neighbors in shortest_paths:
        for neighbor in neighbors:
            pair = tuple(sorted([node, neighbor]))
            if pair not in pairs:
                distances += neighbors[neighbor]
                pairs.add(pair)

    # Get needed network information from G.
    avg_dist = distances / len(pairs)

    num_nodes_msg = "Number of Nodes = {0}\n".format(G.number_of_nodes())
    num_edges_msg = "Number of Edges = {0}\n".format(G.number_of_edges())

    node_lst_msg = "Node list = {0}\n".format(G.nodes()) + "\n"
    edge_lst_msg = "Edge list = {0}\n".format(G.edges()) + "\n"

    diameter_msg = "The diameter of this graph is " + str(diameter) + "\n"
    avg_dst_msg = "The average distance of this graph is " + str(avg_dist) + "\n"

    messages = [num_nodes_msg, num_edges_msg, node_lst_msg, edge_lst_msg, diameter_msg, avg_dst_msg]

    # Write to file "output.txt"
    f = open('output.txt', 'w')
    f.writelines(messages)
    f.close()

    # Plot graph
    import matplotlib.pyplot as pyplot
    nx.draw(G, node_color='orange', with_labels=True)
    plt.savefig("mygraph.png")
    plt.show()

if __name__ == "__main__":
    main() 




