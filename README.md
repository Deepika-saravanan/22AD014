# URL Shortener Backend

A lightweight URL shortener service built with **Flask**.  
This project supports generating short links with expiration, click tracking, authentication using an API key, and request logging middleware.

---

## 🚀 Features
- Generate short URLs with custom or auto-generated codes.
- Set expiration time (default: 30 minutes).
- Track clicks with timestamp, IP, referrer, and user-agent.
- API key–based authentication for secure endpoints.
- Centralized request logging to file and via `/logs` API.

---

🛠️ Setup & Run
1. Clone the Repository
git clone https://github.com/yourusername/url-shortener-backend.git
cd url-shortener-backend

📄Workflow
Create a short URL with /shorturls.
Access the shortened link (/<shortcode>).
Fetch stats with /shorturls/<shortcode>.
Review all request logs using /logs.
