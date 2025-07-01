# === File 1: logic_module.py ===
import pycurl
import io
import shlex

def parse_curl_command(curl_cmd):
    args = shlex.split(curl_cmd)
    if args[0].lower() != "curl":
        raise ValueError("Command must start with 'curl'")

    url = None
    headers = {}
    method = "GET"
    data = None
    i = 1
    while i < len(args):
        if args[i].startswith("http"):
            url = args[i]
        elif args[i] in ["-X", "--request"]:
            i += 1
            method = args[i].upper()
        elif args[i] in ["-H", "--header"]:
            i += 1
            header = args[i].split(":", 1)
            if len(header) == 2:
                headers[header[0].strip()] = header[1].strip()
        elif args[i] in ["-d", "--data"]:
            i += 1
            data = args[i]
        i += 1

    if not url:
        raise ValueError("No URL found in cURL command")
    return url, method, headers, data

def execute_curl_command(curl_cmd, expected_text, iterations, callback=None):
    url, method, headers, data = parse_curl_command(curl_cmd)
    result_list = []

    for i in range(iterations):
        buffer = io.BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.FOLLOWLOCATION, True)

        if method == "POST":
            c.setopt(c.POST, 1)
            if data:
                c.setopt(c.POSTFIELDS, data)
        elif method != "GET":
            c.setopt(c.CUSTOMREQUEST, method)

        if headers:
            c.setopt(c.HTTPHEADER, [f"{k}: {v}" for k, v in headers.items()])

        c.perform()
        status_code = c.getinfo(c.RESPONSE_CODE)
        response = buffer.getvalue().decode("utf-8")
        c.close()

        status = "OK" if expected_text in response else "FAIL"
        result = f"Iteration {i + 1}/{iterations}: {status} (Status Code: {status_code})"
        if callback:
            callback(result, i + 1)
        result_list.append(result)

    return result_list
if __name__ == "__main__":
    curl_cmd = "curl https://example.com"
    expected_text = "Example Domain"
    iterations = 5

    results = execute_curl_command(curl_cmd, expected_text, iterations)

    for line in results:
        print(line)