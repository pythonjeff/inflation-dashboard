📊 Inflation & Policy Dashboard
🚀 A dynamic and interactive dashboard tracking key U.S. economic indicators across presidential terms.
Built using Dash, Plotly, and FRED API, this tool allows users to analyze inflation trends, government deficit, gas prices, and more—all in one place.

📌 Features
✔ Presidential Economic Overview – View economic indicators for each president’s term.
✔ Interactive Flip Cards – Click to reveal detailed economic charts.
✔ Consistent Y-Axis Scaling – Ensures fair comparisons across terms.
✔ Annual Bar Charts for Key Metrics – Government deficit, spending, and mortgage-backed securities (MBS) volume.
✔ Line Charts for Continuous Data – CPI, PPI, Unemployment Rate, and Fed Funds Rate.
✔ Real-time Data from FRED API – Always up-to-date with the latest economic data.

📂 Project Structure
bash
Copy
Edit
inflation_dashboard/
│── data/                     # CSV files for inflation & policy data
│── src/
│   ├── dashboard.py           # Main Dash application
│   ├── policy_tracker.py      # Fetches policy data from FRED API
│── jeffenv/                   # Virtual environment (not tracked)
│── requirements.txt           # Required Python packages
│── README.md                  # Project documentation
│── .gitignore                 # Ignores unnecessary files
📥 Installation
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/pythonjeff/inflation-dashboard.git
cd inflation-dashboard
2️⃣ Set Up a Virtual Environment
bash
Copy
Edit
python -m venv jeffenv
source jeffenv/bin/activate  # macOS/Linux
jeffenv\Scripts\activate     # Windows
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Set Up Your FRED API Key
You'll need a FRED API key to fetch real-time economic data.

Get your API key: FRED API Registration
Store it securely:
bash
Copy
Edit
export FRED_API_KEY="your_api_key_here"   # macOS/Linux
setx FRED_API_KEY "your_api_key_here"     # Windows
▶️ Running the Dashboard
bash
Copy
Edit
python src/dashboard.py
Then open http://127.0.0.1:8050/ in your browser.

📊 Economic Indicators Tracked
Indicator	Description	Data Source
CPI (Inflation)	Consumer Price Index	FRED (CPIAUCSL)
PPI (Producer Prices)	Producer Price Index	FRED (PPIACO)
Unemployment Rate	Percentage of the workforce unemployed	FRED (UNRATE)
Fed Funds Rate	Interest rate set by the Federal Reserve	FRED (FEDFUNDS)
30-Year Mortgage Rate	Average U.S. mortgage rate	FRED (MORTGAGE30US)
Government Spending	Total federal spending	FRED (GFDEBTN)
Government Deficit	Federal surplus/deficit per year	FRED (FYFSD)
Gas Prices	U.S. Regular Gasoline Prices	FRED (GASREGW)
MBS Volume	Mortgage-backed securities held by the Fed	FRED (MBST)
🎨 Dashboard Design
Each president has a flip-card → Click to see detailed data.
Bar charts for yearly metrics (Deficit, Spending, MBS Volume).
Line charts for continuous data (Inflation, Unemployment, Fed Funds Rate).
Consistent Y-axis across all charts for fair comparisons.
🛠️ How to Customize
Want to add new economic indicators?

Find a new FRED series ID (Search FRED)
Modify policy_tracker.py to fetch the new series.
Update dashboard.py to include the new metric.
🚀 Deployment
To deploy using Gunicorn:

bash
Copy
Edit
gunicorn src.dashboard:server
For Heroku or AWS, modify Procfile:

less
Copy
Edit
web: gunicorn src.dashboard:server
📜 License
This project is licensed under the MIT License.

👨‍💻 Author
📌 Developed by: Jeffrey Larson
🌎 GitHub Repo: Inflation Dashboard

⭐ If you find this project useful, give it a star on GitHub! ⭐