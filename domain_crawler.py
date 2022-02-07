import requests

target_url = "www.vulnweb.com/"


def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

# Open file as reading only
with open("domain_crawler/domain_wordlist.txt", "r") as domain_wordlist:
    for line in domain_wordlist:
        word = line.strip()  # remove \n new line
        test_url = target_url + "/" + word
        response = request(test_url)
        if response:
            print("[+] Url found --> " + test_url)



