import requests
import json

def get_logical_pairs(verbs):
    """Finds logical verb/adj pairs using datamuse.com
        - Popular adjectives that modify the given noun (however, we are entering in a verb)
        - Use the popular adjective and find the antonym """

    result = []
    for verb in verbs:
        verb_url = "https://api.datamuse.com//words?rel_jjb=" + str(verb)
        response = list(json.loads(requests.get(verb_url).text))
        pos_word = response[0]["word"]
        adj_url = "https://api.datamuse.com//words?rel_ant=" + str(pos_word)
        ant_list = list(json.loads(requests.get(adj_url).text))
        if len(ant_list) >= 2:
            adjective = ant_list[1]["word"]
        elif len(ant_list) == 1:
            adjective = ant_list[0]["word"]
        else:
            print("No adjective pairing found for: " + str(verb) + " Skipping...")
            break
        result.append((verb, adjective))
    return result
