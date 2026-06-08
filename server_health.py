import subprocess
import json
import time

# Solution to question 1
def load_list_of_servers():
    with open("servers.json", "r") as f:
        config = json.load(f)
    print(f"Loaded {len(config["servers"])} servers")


# Solution to question 2
def send_request_to_one_server():
    url = "https://httpbin.org/status/200"
    start_time = time.perf_counter()
    result = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', "%{http_code}", url], capture_output=True, text=True)
    end_time = time.perf_counter()
    output = {
        "url": url,
        "status_code" : result.stdout.strip()
    }

    elapsed_time = (end_time - start_time)

    print(f"{output}")
    print(f"Elapsed time: {elapsed_time:.2f}ms")
    # Solution to question 4
    status_code = result.stdout.strip()
    if((status_code >= 200) and (status_code <= 299)):
        print(f"Service is healthy.")
    elif status_code >= 400:
        print(f"Service is down")


# result = subprocess.run(['curl', '-l', 'https://httpbin.org/status/200'])
# print(result.returncode)

if __name__ == "__main__":
    print()
    load_list_of_servers()
    print()
    send_request_to_one_server()

