import tkinter as tk
from tkinter import ttk, scrolledtext, Toplevel, messagebox
import requests
import shlex
import time


class CurlDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("cURL Request Dashboard")
        self.root.geometry("600x500")
        self.stop_flag = False
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="cURL Command:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.curl_entry = tk.Entry(self.root, width=60)
        self.curl_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        self.curl_entry.insert(0, "curl https://example.com")

        tk.Label(self.root, text="Expected Text in Response:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.expected_text_entry = tk.Entry(self.root, width=60)
        self.expected_text_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        tk.Label(self.root, text="Number of Iterations:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.iterations_entry = tk.Entry(self.root, width=10)
        self.iterations_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.iterations_entry.insert(0, "10")

        self.execute_button = tk.Button(self.root, text="Execute", command=self.execute_curl)
        self.execute_button.grid(row=3, column=0, padx=5, pady=10)
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_execution, state="disabled")
        self.stop_button.grid(row=3, column=1, padx=5, pady=10, sticky="w")
        tk.Button(self.root, text="Show Code Snippet", command=self.show_code_snippet).grid(row=3, column=2, padx=5, pady=10)

        tk.Label(self.root, text="Progress:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        tk.Label(self.root, text="Output:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.output_text = scrolledtext.ScrolledText(self.root, width=60, height=15, wrap=tk.WORD)
        self.output_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

    def parse_curl_command(self, curl_cmd):
        try:
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
        except Exception as e:
            messagebox.showerror("Parsing Error", str(e))
            return None, None, None, None

    def execute_curl(self):
        self.output_text.delete(1.0, tk.END)
        self.stop_flag = False
        curl_cmd = self.curl_entry.get()
        expected_text = self.expected_text_entry.get()

        try:
            iterations = int(self.iterations_entry.get())
            if iterations <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of iterations.")
            return

        url, method, headers, data = self.parse_curl_command(curl_cmd)
        if not url:
            return

        self.execute_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.progress["maximum"] = iterations
        self.progress["value"] = 0

        for i in range(iterations):
            if self.stop_flag:
                self.output_text.insert(tk.END, "Execution stopped by user\n")
                break
            try:
                response = requests.request(method, url, headers=headers, data=data)
                status_code = response.status_code
                text = response.text
                status = "OK" if expected_text in text else "FAIL"
                self.output_text.insert(tk.END, f"Iteration {i + 1}/{iterations}: {status} (Status Code: {status_code})\n")
            except Exception as e:
                self.output_text.insert(tk.END, f"Iteration {i + 1}/{iterations}: Error - {str(e)}\n")

            self.output_text.see(tk.END)
            self.progress["value"] = i + 1
            self.root.update()
            time.sleep(0.1)

        self.execute_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def stop_execution(self):
        self.stop_flag = True

    def show_code_snippet(self):
        code = '''
import requests
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
            response = requests.request(method, url, headers=headers, data=data)
            status_code = response.status_code
            status = "OK" if expected_text in response.text else "FAIL"
            print(f"Iteration {i+1}/{iterations}: {status} (Status Code: {status_code})")
    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage
execute_curl("curl https://example.com", "Example Domain", 10)
'''
        snippet_window = Toplevel(self.root)
        snippet_window.title("Code Snippet")
        snippet_window.geometry("600x400")
        text_area = scrolledtext.ScrolledText(snippet_window, width=70, height=18, wrap=tk.WORD)
        text_area.pack(padx=10, pady=10)
        text_area.insert(tk.END, code)
        text_area.config(state="disabled")
        tk.Button(snippet_window, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(code)).pack(pady=5)

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()


if __name__ == "__main__":
    root = tk.Tk()
    app = CurlDashboard(root)
    root.mainloop()
