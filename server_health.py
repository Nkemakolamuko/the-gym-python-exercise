import subprocess
import json

# Solution to question 1
def load_list_of_servers():
    with open("servers.json", "r") as f:
        config = json.load(f)
    print(f"Loaded {len(config["servers"])} servers")


# Solution to question 2
def send_request_to_one_server():
    url = "https://httpbin.org/status/200"
    result = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', "%{http_code}", url], capture_output=True, text=True)

    output = {
        "url": url,
        "status_code" : result.stdout.strip()
    }

    print(f"{output}")

# result = subprocess.run(['curl', '-l', 'https://httpbin.org/status/200'])
# print(result.returncode)

if __name__ == "__main__":
    print()
    load_list_of_servers()
    print()
    send_request_to_one_server()

