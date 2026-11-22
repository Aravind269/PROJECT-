# Community Renewable Energy Awareness and Management Portal

A modern, responsive, full-stack web application designed to educate citizens, empower neighborhoods to transition toward renewable energy, model solar rooftop energy savings, track community projects, and exchange sustainable living experiences.

---

## 🌿 Project Overview

The **Community Renewable Energy Awareness and Management Portal** spreads awareness about clean energy sources including **Solar**, **Wind**, **Hydro**, and **Biomass**. It equips homeowners and neighborhood associations with tools to calculate energy consumption and bill savings, explore community microgrids, and share real-world renewable energy experiences.

---

## 🚀 Key Features

### 1. Home Page
- **Hero Section**: Modern, responsive landing page with custom vector illustrations, mission highlights, and action buttons.
- **Aggregated Community Counters**: Live metrics on registered members, clean power generated (MWh), and CO₂ offset.
- **Renewable Energy Pillars**: Highlighting Solar, Wind, Hydro, and Biomass energy with direct links to educational modules.
- **Interactive Calculator Teaser**: Fast preview of solar bill savings and environmental dividends.
- **Community Projects Showcase**: Featured neighborhood renewable initiatives.

### 2. Renewable Energy Awareness
- **In-Depth Source Analysis**: Detailed breakdowns of Solar (PV & thermal), Wind (onshore & offshore), Micro-Hydro (run-of-river), and Biomass (anaerobic digestion & biogas).
- **Advantages & Disadvantages**: Clear pros and cons accompanied by modern engineering solutions.
- **Pollution & Emission Reduction**: Scientific explanations of how renewables eliminate fine particulate matter (PM2.5), sulfur dioxide (SO₂), nitrogen oxides (NOₓ), and greenhouse gases.
- **Interactive Energy-Saving Tips**: Filterable by category (*Home*, *Heating & Cooling*, *Lighting*, *Appliances*, *Solar Optimization*) with estimated monthly kWh savings badges.
- **Educational Articles & Guides**: Complete articles with reading times and key takeaways.

### 3. Solar & Energy Savings Calculator
- **Dynamic Interactive Inputs**:
  - Monthly electricity bill amount ($/₹)
  - Electricity tariff rate ($/kWh)
  - Available unshaded roof area (sq. ft.)
  - Daily peak sunlight hours
  - Target offset percentage (50%, 75%, 100% net zero, 120%)
- **Dynamic Real-Time Sizing**:
  - Recommended solar system capacity (kW)
  - Required 400W solar panels count
  - Roof area feasibility check
  - Monthly and annual bill savings
  - Estimated net system cost & payback period (years)
  - Estimated carbon reduction (tons/year), trees planted equivalent, and car miles avoided
- **Interactive Chart.js Visualizations**:
  - *Chart 1*: Monthly electricity bill comparison (Current Grid Bill vs With Solar vs Savings).
  - *Chart 2*: 25-Year cumulative savings projection factoring in utility rate escalation.
- **Save & Export**: Logged-in users can save calculations to their profile and print/export clean PDF reports.

### 4. Community Management & Forum
- **User Authentication**: Secure registration and login with hashed passwords (`scrypt`/`pbkdf2`).
- **User Profiles**: Manage bio, location, and clean energy interests; view saved calculations and personal posts.
- **Experience Sharing Wall**: Members can publish installation stories, real utility savings, equipment reviews, and tips.
- **Interactive Comments & AJAX Upvoting**: Real-time upvotes and replies to foster constructive dialogue.

### 5. Renewable Energy Projects
- **Project Directory**: Filter community initiatives by category (*Solar*, *Wind*, *Hydro*, *Biomass*) and status (*Active*, *Planning*).
- **Project Details**: Complete project metrics, descriptions, subscriber counts, and environmental benefits.
- **Solar Installation Guide**: Comprehensive 5-phase guide covering *Energy Audit & Sizing*, *Design & Quotes*, *Permitting & Interconnection*, *Physical Installation*, and *Inspection & PTO*.
- **Community Proposals**: Registered users can submit proposals for new community clean energy projects.

### 6. Analytics Dashboard
- **Executive KPI Cards**: Total registered users, active renewable projects, annual clean generation (MWh), community bill savings ($), and CO₂ offset (Tons).
- **Chart.js Visualizations**:
  - *Generation Mix Donut Chart*: Solar, Wind, Hydro, and Biomass breakdown.
  - *12-Month Generation & Savings Trend Chart*: Dual-axis chart displaying monthly power generation and financial savings.
- **Environmental Scorecard**: Tree equivalency and avoided fossil fuel combustion.
- **Personalized Activity**: User's saved calculations and community discussions.

### 7. Contact & Feedback
- **Contact Form**: Validated user inputs with database persistence into `feedback_messages`.
- **Categorized Inquiries**: Support for *Inquiries*, *Community Suggestions*, *Collaborations*, and *Technical Issues*.
- **Contact Details**: Headquarters address, helpline, advisory desk hours, and FAQ accordion.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3.3, Bootstrap Icons |
| **Charts** | Chart.js 4.4.2 |
| **Backend** | Python Flask, Werkzeug, Jinja2 |
| **Database** | MySQL (with seamless SQLite fallback for zero-setup execution) |
| **ORM / Driver** | Flask-SQLAlchemy 3.1+, SQLAlchemy 2.1+, PyMySQL 1.2+ |

---

## 📁 Project Folder Structure

```text
PROJECT/
├── .env                         # Environment configuration (MySQL / Flask settings)
├── .env.example                 # Example environment template
├── requirements.txt             # Python dependencies
├── config.py                    # Dual MySQL / SQLite database configuration
├── py_loader.py                 # Pure-Python loader for Windows App Control compatibility
├── models.py                    # SQLAlchemy database models
├── schema.sql                   # MySQL DDL schema and seed data
├── init_db.py                   # Automated database table creator and seeder
├── app.py                       # Flask application factory and route handlers
├── test_app.py                  # Unit and integration test suite
├── static/
│   ├── css/
│   │   └── style.css            # Custom theme styles (Emerald Green & Ocean Blue)
│   ├── js/
│   │   ├── main.js              # Navbar, alerts, AJAX upvoting, tip filter
│   │   ├── calculator.js        # Dynamic solar sizing, formulas, and Chart.js charts
│   │   └── dashboard.js         # Dashboard generation mix and trend charts
│   └── img/
│       ├── logo.svg             # Portal vector logo
│       ├── hero_illustration.svg# Eco-community landscape illustration
│       ├── solar_farm.svg       # Solar project illustration
│       ├── wind_project.svg     # Wind project illustration
│       ├── hydro_project.svg    # Micro-hydro project illustration
│       ├── biomass_project.svg  # Biomass digester illustration
│       └── microgrid_project.svg# Smart microgrid illustration
└── templates/
    ├── base.html                # Base layout with navbar, footer, and flash alerts
    ├── index.html               # 1. Home Page
    ├── awareness.html           # 2. Renewable Energy Awareness & Tips
    ├── article_detail.html      # Educational article view
    ├── calculator.html          # 3. Energy Savings Calculator
    ├── projects.html            # 5. Renewable Energy Projects & Installation Guide
    ├── project_detail.html      # Individual project view
    ├── community.html           # 4. Community Forum & Experience Sharing
    ├── dashboard.html           # 6. Analytics Dashboard
    ├── contact.html             # 7. Contact and Feedback
    ├── login.html               # User Login
    ├── register.html            # User Registration
    ├── profile.html             # User Profile & Activity
    ├── 404.html                 # Page Not Found Error
    └── 500.html                 # Internal Server Error
```

---

## ⚙️ Step-by-Step Instructions to Run Locally

### 1. Prerequisites
- **Python 3.10 or higher** installed.
- Optional: **MySQL Server** or **XAMPP / WampServer / MariaDB** (if running MySQL locally).

---

### 2. Install Dependencies
Open PowerShell or Command Prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

---

### 3. Database Configuration

#### Option A: Running with MySQL (Recommended for Production)
1. Start your local MySQL service (e.g. via XAMPP Control Panel or MySQL Windows Service).
2. Open the `.env` file in the project root and configure your credentials:
   ```ini
   MYSQL_USER=root
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_DB=community_renewable_energy
   ```
3. Initialize the database and populate default seed data by running:
   ```bash
   python init_db.py
   ```
   *(Alternatively, you can import `schema.sql` directly in phpMyAdmin or the MySQL Command Line Client).*

#### Option B: Zero-Configuration SQLite Mode (Out-of-the-Box)
If MySQL is not installed or currently running on your machine, the application **automatically detects this and runs with SQLite (`community_energy.db`)**. No database configuration or software installation is required!

---

### 4. Initialize Database
Initialize the database tables and sample projects/articles:
```bash
python init_db.py
```
*(To reset the database back to clean demo data at any time, run: `python init_db.py --reset`)*.

---

### 5. Start the Web Application
Run the Flask server:
```bash
python app.py
```
The application will start on:
```text
http://127.0.0.1:5000  (or http://localhost:5000)
```

Open your browser and navigate to `http://localhost:5000`.

---

## 🔑 Pre-Configured Demo Accounts

You can immediately log in with these pre-seeded accounts:

| Role | Email | Password | Details |
| :--- | :--- | :--- | :--- |
| **Admin** | `elena@greenportal.org` | `admin123` | Community Solar Co-op Coordinator |
| **Member** | `marcus@cleanenergy.org` | `green123` | Homeowner with 8.4 kW Rooftop Solar |
| **Member** | `sophia@ecocommunity.net` | `green123` | Biogas & Permaculture Advocate |

You can also create a new account anytime via the **Join Portal** button.

---

## 🧪 Running Automated Tests

To run the unit and integration test suite:
```bash
python -m unittest test_app.py
```
This tests all 7 modules including page rendering, calculator formulas, database storage, and authentication.

---

## 📜 License
Developed for educational, community, and environmental sustainability initiatives.
