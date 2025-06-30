# Project Name: cURL Request Dashboard GUI

# Description:

       The cURL Request Dashboard is a Python-based desktop GUI application built with Tkinter and powered by pycurl, designed to repeatedly execute cURL commands, validate responses, and display the progress interactively.

It’s useful for developers, testers, or network engineers who want to automate repeated API/URL requests and monitor whether expected content appears in the response.

# Features:
✅ Accepts full curl command input (with headers, method, data)

🔁 Runs request multiple times (looped iterations)

🔍 Matches expected text in each response

📊 Shows real-time progress bar

📝 Displays response status codes and results in a scrollable text area

✋ Stop button to cancel execution mid-loop

📋 Built-in code snippet viewer with copy-to-clipboard option

🛠 Technologies Used:
Python 3

Tkinter – For GUI components

pycurl – For making HTTP requests (like curl)

shlex – To safely parse command-line strings

io.BytesIO – To buffer responses in memory

🖥️ GUI Overview:
Input:

cURL Command

Expected Text in Response

Number of Iterations

Buttons:

Execute

Stop

Show Code Snippet

Output Area:

Scrollable log of each request's result

Progress Bar:

Visual feedback of test progress
