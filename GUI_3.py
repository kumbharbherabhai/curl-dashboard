import streamlit as st
import requests
import shlex
import time

st.set_page_config(page_title="cURL Dashboard", layout="centered")
st.title("🌐 cURL Request Dashboard")

# User inputs
curl_cmd = st.text_input("Enter cURL Command", "curl https://example.com")
expected_text = st.text_input("Expected Text in Response")
iterations = st.number_input("Number of Iterations", min_value=1, max_value=1000, value=50)

run_button = st.button("🚀 Execute")

# Function to parse cURL command
def parse_curl_command(curl_cmd):
    try:
        args = shlex.split(curl_cmd)
        if args[0].lower() != "curl":
            st.error("Command must start with 'curl'")
            return None, None, None, None

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
            st.error("No URL found in cURL command")
            return None, None, None, None

        return url, method, headers, data
    except Exception as e:
        st.error(f"Parsing Error: {str(e)}")
        return None, None, None, None

# Execute logic
if run_button:
    url, method, headers, data = parse_curl_command(curl_cmd)
    if url:
        progress_bar = st.progress(0)
        output_log = ""

        for i in range(iterations):
            try:
                response = requests.request(method, url, headers=headers, data=data)
                status_code = response.status_code
                response_text = response.text
                status = "✅ OK" if expected_text in response_text else "❌ FAIL"
                output_log += f"Iteration {i+1}/{iterations}: {status} (Status Code: {status_code})\n"
            except Exception as e:
                output_log += f"Iteration {i+1}/{iterations}: Error - {str(e)}\n"

            progress_bar.progress((i + 1) / iterations)
            time.sleep(0.1)

        st.text_area("Output Log", output_log, height=300)

# Code snippet section
with st.expander("📄 Show Python Code Snippet"):
    code_snippet = f'''import requests
import shlex

def execute_curl(curl_cmd="{curl_cmd}", expected_text="{expected_text}", iterations={iterations}):
    args = shlex.split(curl_cmd)
    if args[0].lower() != "curl":
        raise ValueError("Command must start with 'curl'")

    url, method, headers, data = None, "GET", {{}}, None
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

    for i in range(iterations):
        response = requests.request(method, url, headers=headers, data=data)
        status_code = response.status_code
        status = "OK" if expected_text in response.text else "FAIL"
        print(f"Iteration {{i+1}}/{{iterations}}: {{status}} (Status Code: {{status_code}})")

# Example usage
execute_curl()
'''
    st.code(code_snippet, language="python")