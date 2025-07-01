import streamlit as st
import requests
import shlex
import time


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


def main():
    st.title("🌐 cURL Request Dashboard")
    curl_cmd = st.text_input("Enter cURL Command", "curl https://example.com")
    expected_text = st.text_input("Expected Text in Response", "Example Domain")
    iterations = st.number_input("Number of Iterations", min_value=1, value=5)

    run_button = st.button("▶ Execute cURL")

    if run_button:
        url, method, headers, data = parse_curl_command(curl_cmd)
        if not url:
            return

        progress_bar = st.progress(0)
        output = ""

        for i in range(iterations):
            try:
                response = requests.request(method, url, headers=headers, data=data)
                status_code = response.status_code
                text = response.text
                status = "✅ OK" if expected_text in text else "❌ FAIL"
                result = f"Iteration {i+1}/{iterations}: {status} (Status Code: {status_code})"
                output += result + "\n"
            except Exception as e:
                output += f"Iteration {i+1}/{iterations}: Error - {str(e)}\n"
            progress_bar.progress((i + 1) / iterations)
            time.sleep(0.1)

        st.text_area("Response Summary", output, height=300)


if __name__ == "__main__":
    main()
