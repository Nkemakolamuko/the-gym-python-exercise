import subprocess
import json
import time
import requests
import os

# Solution to question 1
def load_list_of_servers():
    with open("servers.json", "r") as f:
        config = json.load(f)
    print(f"Loaded {len(config["servers"])} servers")


# Solution to question 2
def send_request_to_one_server():
    url = "https://httpbin.org/status/200"
    # url = "https://httpbin.org/status/500" # uncomment to test for failing server
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
    status_code = int(result.stdout.strip())
    if((status_code >= 200) and (status_code <= 299)):
        print(f"Service is healthy.")
    elif status_code >= 400:
        print(f"Service is down")


# result = subprocess.run(['curl', '-l', 'https://httpbin.org/status/200'])
# print(result.returncode)

# Solution to question 5
def validate_json_body():
    # response = subprocess.run(['curl', '-I', 'https://httpbin.org/json'], capture_output=True, text=True)
    # if "content-type: application/json" in response.stdout.lower():
    #     print(f"Response type: JSON")
    # else:
    #     print("Response type is not JSON")
    url = 'https://httpbin.org/json'
    response = requests.get(url)
    status_code = response.status_code
    if status_code != 200:
        print(f"Status code is not 200, returned {status_code}")
        return

    content_type = response.headers['Content-Type']
    if content_type != 'application/json':
        print(f"Unhealthy response - not JSON: {content_type}")
        return
    
    data = response.json()
    if data.get('status') == 'ok':
        print(f'Healthy -- status is ok')
    else:
        print(f"Unhealthy -- response has no body of status - ok")
        print(f"Received: {data}")


# Solution to 6
def detect_slow_service():
    start = time.perf_counter()
    response = requests.get('https://httpbin.org/delay/2')
    # print(f"Delayed response: {response.json()}")
    end = time.perf_counter()

    delay = end - start
    if delay > 2100 * 1000:
        print(f"slow response - {delay:.2f}ms")
    else:
        print(f"fast response - {delay:.2f}ms")


# Solution to 7
def print_result_per_service():
    try:
        start = time.perf_counter()
        response = requests.get('https://httpbin.org/delay/2', timeout=5)
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000
        status_code = response.status_code
        slow_tag = " [slow]" if elapsed_ms > 500 else ""

        if 200 <= status_code <= 299:
            print(f"{'https://httpbin.org/delay/2'} - OK ({status_code}) - {elapsed_ms:.0f}ms{slow_tag}")
        else:
            print(f"{'https://httpbin.org/delay/2'} - DOWN ({status_code})")

    except requests.Timeout:
        print(f"{'https://httpbin.org/delay/2'} - TIMEOUT")


# Solution to 8
def save_failed_services():
    failed_services = []
    response = requests.get('https://httpbin.org/delay/2')
    status_code = response.status_code

    if status_code < 200 or status_code > 299:
        failed_services.append('https://httpbin.org/delay/2')

    if failed_services:
        print(f"Failed services: {', '.join(failed_services)}")
    else:
        print("All services healthy.")


# Solution to 9
def load_servers():
    env_path = os.environ.get("SERVERS_CONFIG")
    file_path = env_path if env_path else "servers.json"

    if not os.path.exists(file_path):
        print("Error: No config file found and SERVERS_CONFIG env variable not set")
        return []

    with open(file_path, "r") as f:
        config = json.load(f)
    return config["servers"]

# Solution to 10
def check_server(url):
    start = time.perf_counter()
    response = requests.get(url)
    end = time.perf_counter()

    return {
        "url": url,
        "status": response.status_code,
        "elapsed_ms": (end - start) * 1000
    }

def format_result(result):
    url = result["url"]
    status = result["status"]
    elapsed_ms = result["elapsed_ms"]
    slow_tag = " [slow]" if elapsed_ms > 500 else ""

    if 200 <= status <= 299:
        return f"{url} — OK ({status}) — {elapsed_ms:.0f}ms{slow_tag}"
    else:
        return f"{url} — DOWN ({status})"

def check_all_servers():
    servers  = load_servers()
    results  = []

    for url in servers:
        result = check_server(url)
        results.append(result)
        print(format_result(result))

    return results
        

if __name__ == "__main__":
    print()
    load_list_of_servers()
    print()
    send_request_to_one_server()
    print()
    validate_json_body()
    print()
    detect_slow_service()
    print()
    print_result_per_service()
    print()
    save_failed_services()
    print()
    load_servers()

