import streamlit as st
import pycurl
import io
import shlex
import time

st.set_page_config(page_title="cURL Request Dashboard", layout="centered")
st.title("🌐 cURL Request Dashboard")

# --- Input Fields ---
curl_cmd = st.text_input("🔗 cURL Command", "curl https://example.com")
expected_text = st.text_input("✅ Expected Text in Response", "")
iterations = st.number_input("🔁 Number of Iterations", min_value=1, max_value=1000, value=10)

progress_placeholder = st.empty()
output_placeholder = st.empty()

# --- Execute Function ---
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

# --- Execution Block ---
if st.button("🚀 Execute"):
    url, method, headers, data = parse_curl_command(curl_cmd)
    if url:
        progress_bar = progress_placeholder.progress(0)
        output_lines = []

        for i in range(iterations):
            try:
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

                status = "✅ OK" if expected_text in response else "❌ FAIL"
                output_lines.append(f"Iteration {i+1}/{iterations}: {status} (Status Code: {status_code})")

            except Exception as e:
                output_lines.append(f"Iteration {i+1}/{iterations}: ❌ Error - {str(e)}")

            progress_bar.progress((i + 1) / iterations)
            time.sleep(0.1)

        output_placeholder.text_area("📋 Output", value="\n".join(output_lines), height=300)

# --- Show Code Snippet ---
with st.expander("📄 Show Code Snippet"):
    code = '''
import pycurl
import io
import shlex

def execute_curl(curl_cmd, expected_text, iterations):
    try:
        args = shlex.split(curl_cmd)
        if args[0].lower() != "curl":
            raise ValueError("Command must start with 'curl'")

        url, method, headers, data = None, "GET", {}, None
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
            print(f"Iteration {i+1}/{iterations}: {status} (Status Code: {status_code})")
    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage
execute_curl("curl https://example.com", "Example Domain", 50)
    '''
    st.code(code, language="python")













# # === File 1: logic_module.py ===
# import pycurl
# import io
# import shlex
#
# def parse_curl_command(curl_cmd):
#     args = shlex.split(curl_cmd)
#     if args[0].lower() != "curl":
#         raise ValueError("Command must start with 'curl'")
#
#     url = None
#     headers = {}
#     method = "GET"
#     data = None
#     i = 1
#     while i < len(args):
#         if args[i].startswith("http"):
#             url = args[i]
#         elif args[i] in ["-X", "--request"]:
#             i += 1
#             method = args[i].upper()
#         elif args[i] in ["-H", "--header"]:
#             i += 1
#             header = args[i].split(":", 1)
#             if len(header) == 2:
#                 headers[header[0].strip()] = header[1].strip()
#         elif args[i] in ["-d", "--data"]:
#             i += 1
#             data = args[i]
#         i += 1
#
#     if not url:
#         raise ValueError("No URL found in cURL command")
#     return url, method, headers, data
#
# def execute_curl_command(curl_cmd, expected_text, iterations, callback=None):
#     url, method, headers, data = parse_curl_command(curl_cmd)
#     result_list = []
#
#     for i in range(iterations):
#         buffer = io.BytesIO()
#         c = pycurl.Curl()
#         c.setopt(c.URL, url)
#         c.setopt(c.WRITEDATA, buffer)
#         c.setopt(c.FOLLOWLOCATION, True)
#
#         if method == "POST":
#             c.setopt(c.POST, 1)
#             if data:
#                 c.setopt(c.POSTFIELDS, data)
#         elif method != "GET":
#             c.setopt(c.CUSTOMREQUEST, method)
#
#         if headers:
#             c.setopt(c.HTTPHEADER, [f"{k}: {v}" for k, v in headers.items()])
#
#         c.perform()
#         status_code = c.getinfo(c.RESPONSE_CODE)
#         response = buffer.getvalue().decode("utf-8")
#         c.close()
#
#         status = "OK" if expected_text in response else "FAIL"
#         result = f"Iteration {i + 1}/{iterations}: {status} (Status Code: {status_code})"
#         if callback:
#             callback(result, i + 1)
#         result_list.append(result)
#
#     return result_list
# if __name__ == "__main__":
#     curl_cmd = "curl https://example.com"
#     expected_text = "Example Domain"
#     iterations = 5
#
#     results = execute_curl_command(curl_cmd, expected_text, iterations)
#
#     for line in results:
#         print(line)