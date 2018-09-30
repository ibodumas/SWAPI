import requests
import json


class HttpError(Exception):
    pass


def status_checker(req: requests.get):
    if req.status_code == requests.status_codes.codes.ok:
        return True
    elif 400 <= req.status_code <= 599:
        # raise the error if there is a bad response - 4XX or 5XX codes
        req.raise_for_status()
    else:
        raise HttpError(req.status_code)


url = "https://swapi.co/api/people"
results = []
count = 0

if __name__ == "__main__":
    # loop through all the pages
    while url:
        req = requests.get(url=url, allow_redirects=True)
        if status_checker(req):
            data = req.json()
            results.extend(data["results"])
            count += data["count"]
            # get the url of the next page
            url = data["next"]

    if results:
        with open("SWAP_data.txt", "w") as f:
            f.write(json.dumps({"count": count, "results": results}))
