🧠 What Is Stiletto?
Stiletto is a cutting-edge signal delivery and automation platform for financial traders. It combines trade signal broadcasting, real-time notifications, and optional bot-driven execution — offering a clean, modular, and secure backend system that streamlines trade workflows for both signal providers and subscribers.

It’s the engine behind The Orange Team, a platform for forex traders to receive automated and manual signals, with features for delivery control, API integration, and user-based permission management.

🚀 Tech Stack
| Layer             | Technology           | Purpose                                 |
| ----------------- | -------------------- | --------------------------------------- |
| **Backend**       | Python, Django       | Core server logic & web framework       |
| **Database**      | SQLite (default)     | Data persistence (signals, users, etc.) |
| **Task Handling** | Django Signals       | Triggering logic & event automation     |
| **Frontend**      | Django Templates     | HTML rendering for forms & UI           |
| **Styling**       | Bootstrap (assumed)  | UI/UX styling                           |
| **Trading Logic** | `.ex5`, `.mq5` files | MetaTrader 5 Expert Advisors (EAs)      |
| **APIs**          | Custom Django APIs   | Sending trade signals via HTTP calls    |
| **Email System**  | Django Email Backend | Send real-time signal alerts            |

🔑 Key Features
📩 Signal Broadcasting System
Admins can submit buy/sell signals to specific subscribers.

Supports manual signal creation or automated execution via uploaded .ex5/.mq5 bots.

Email and platform-based alerts are sent to signal recipients.

👥 Multi-user Permissions
Admin panel for managing users, emails, and access rights.

Signals can be filtered and delivered to selected users only.

🤖 Bot Integration
Uses .ex5 and .mq5 files to automate trading instructions.

Can integrate with MetaTrader 5 or similar environments for execution.

📬 Email Notification System
Signals are sent to users in real-time via email.

Logs stored in sent_emails/ folder for traceability.

🔒 Logs & Monitoring
Two main logs: general.log and lemon.log for system activity and debug messages.

Useful for audit trails, debugging, and performance review.


🧾 File/Folder Breakdown
| Path                                       | Description                                    |
| ------------------------------------------ | ---------------------------------------------- |
| `app/`                                     | Main Django app logic                          |
| `accounts/`                                | User login, authentication, and email tracking |
| `signal_api/`                              | APIs for external signal submission            |
| `templates/`                               | HTML templates for rendering views             |
| `static/`                                  | Static files (JS/CSS)                          |
| `stiletto-auto.ex5`<br>`stiletto-auto.mq5` | MetaTrader bot files                           |
| `sent_emails/`                             | Stores email logs of signal delivery           |
| `general.log`<br>`lemon.log`               | Logs for debugging, monitoring                 |



🧑‍💻 Author
Built by Allan Osei
Live at theorange.team

Screenshots![Screenshot (24)](https://github.com/user-attachments/assets/7dce78e5-113c-4db6-82ab-9d5b8eba2664)
![Screenshot (23)](https://github.com/user-attachments/assets/57cad4ed-6a5c-47fc-91be-c4cee035dcaf)
![Screenshot (22)](https://github.com/user-attachments/assets/5979ee31-ec88-4bd4-9289-2a95b8b87e23)
![Screenshot (21)](https://github.com/user-attachments/assets/5b2049db-27d1-4897-b6ee-c8d091f3ccc4)
![Screenshot (20)](https://github.com/user-attachments/assets/d53f587d-dc8a-42e4-9515-650df12cf180)
![Screenshot (19)](https://github.com/user-attachments/assets/a34fa1c6-3713-49da-b2a1-17e5809e2f2e)
![Screenshot (18)](https://github.com/user-attachments/assets/13d7c2ca-24aa-4fbf-a21a-cb52f627f0af)
![Screenshot (17)](https://github.com/user-attachments/assets/3db0b99b-baa1-4442-8a13-ce2277196af9)
![Screenshot (16)](https://github.com/user-attachments/assets/40e32a75-831f-49cb-b5ff-f80d3f570459)
![Screenshot (15)](https://github.com/user-attachments/assets/ecf9dd4d-30d9-4121-abb6-f5dbcdfd7954)
![Screenshot (14)](https://github.com/user-attachments/assets/879738bc-66e5-40e7-97a1-69d621e53649)
![Screenshot (13)](https://github.com/user-attachments/assets/6a2358ee-8ae3-404c-9a3c-e99744d44f7b)
