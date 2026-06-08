import subprocess
import json

# Solution to question 1
def load_list_of_servers():
    with open("servers.json", "r") as f:
        config = json.load(f)
    print(f"Loaded {len(config["servers"])} servers")

# result = subprocess.run(['curl', '-l', 'https://httpbin.org/status/200'])
# print(result.returncode)

if __name__ == "__main__":
    print()
    load_list_of_servers()

