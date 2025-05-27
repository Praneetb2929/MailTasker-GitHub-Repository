# MailTasker-GitHub-Repository

# 📧 MailTasker

**MailTasker** is a simple, lightweight task management web app built with **Python Flask**. It allows users to manage tasks derived from emails — view them, mark as done, delete them, and filter based on task status.  

This project was created as a submission for the [Postmark Challenge: Inbox Innovators](https://dev.to/challenges/postmark).

---

## 🚀 Features

- 📥 View all incoming tasks fetched from emails.
- ✅ Mark tasks as **Done**.
- 🗑️ Delete unwanted tasks.
- 🔍 Search tasks by subject or body.
- 🔃 Filter tasks by status: **Pending** or **Done**.
- 📱 Clean, responsive interface using Bootstrap 5.

---

## 🖥️ Demo

Currently runs on local development server:


python logic.py

Then open:
http://127.0.0.1:5000/view-tasks

Screenshots:
![Image](https://github.com/user-attachments/assets/196cb70b-2e39-4722-af4c-16dc346df5ce)

# 📦 Tech Stack

Python (Flask)

SQLite (Local database)

Bootstrap 5 (UI)

Jinja2 (Templates)

(Postmark integration planned in future updates)

# 📂 Project Structure

csharp

Copy

Edit

MailTasker/
│
├── static/
│   └── (CSS, JS files)
│
├── templates/
│   ├── base.html
│   └── view_tasks.html
│
├── logic.py
├── database.db
└── README.md

 # 🛠️ How to Run
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/mailtasker.git
cd mailtasker
Install dependencies:

bash
Copy
Edit
pip install flask
Run the app:

bash
Copy
Edit
python logic.py
Open your browser and navigate to:
http://127.0.0.1:5000/view-tasks

 # 🎯 Future Improvements

📧 Integrate Postmark API to automatically parse and add tasks from incoming emails.
📱 Add mobile responsiveness improvements.
📊 Implement task analytics (number of tasks done, pending, per day/week).
📝 Add user authentication.

 # 📃 License
This project is open-source and available under the MIT License.

 # ✨ Acknowledgements
Special thanks to the Postmark Challenge: Inbox Innovators community for the inspiration.





