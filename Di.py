# === File 2: dashboard_ui.py ===
import tkinter as tk
from tkinter import ttk, scrolledtext, Toplevel, messagebox
import time
from logic_code import execute_curl_command

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
        self.iterations_entry.insert(0, "50")

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

        self.execute_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.progress["maximum"] = iterations
        self.progress["value"] = 0

        def update_ui(result, iteration):
            if self.stop_flag:
                self.output_text.insert(tk.END, "Execution stopped by user\n")
                return
            self.output_text.insert(tk.END, result + "\n")
            self.output_text.see(tk.END)
            self.progress["value"] = iteration
            self.root.update()
            time.sleep(0.1)

        execute_curl_command(curl_cmd, expected_text, iterations, callback=update_ui)
        self.execute_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def stop_execution(self):
        self.stop_flag = True

    def show_code_snippet(self):
        code = 'from logic_module import execute_curl_command\nexecute_curl_command("curl https://example.com", "Example Domain", 50)'  # placeholder
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
