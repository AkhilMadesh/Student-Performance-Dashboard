# Student-Performance-Dashboard
This project is an interactive Student Performance Dashboard built using Flask and Dash. It visualizes academic data using multiple charts and allows both overall and student-wise performance analysis.
# 🎓 Student Performance Analytics Dashboard 

## 📌 Project Overview

This project is an interactive **Student Performance Analytics Dashboard** designed for **Students**. It helps visualize and analyze student marks across multiple subjects using modern data visualization techniques.

The system uses a **Flask backend** to manage student data and a **Dash + Plotly frontend** to present interactive charts and tables.

---

## 🚀 Features

* 📊 Combined performance analysis of all students
* 👤 Individual student performance view (subject-wise)
* 🎨 Multiple graph types:

  * Bar Chart
  * Pie Chart
  * Line Chart
* 🔽 Graph selection dropdown (user-controlled)
* 📋 Complete marks table (Name | Subject | Marks)
* 🌈 Clean, colourful, and professional dashboard UI

---

## 🧑‍💻 Tech Stack

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* SQLite (file-based database)
* Flask-CORS

### Frontend

* Dash
* Plotly
* Pandas

---

## 📚 Subjects Used 

* DSA – Data Structures & Algorithms
* DBMS – Database Management Systems
* OS – Operating Systems
* CN – Computer Networks
* SE – Software Engineering

---

## 📁 Project Structure

```
student-performance-dashboard/
│
├── app.py              # Flask backend (APIs + DB)
├── dashboard.py        # Dash frontend (visualizations)
├── students.db         # SQLite database (auto-created)
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 2️⃣ Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install flask flask-sqlalchemy flask-cors dash plotly pandas requests
```

---

## ▶️ Running the Project

### Step 1: Start Flask Backend

```bash
python app.py
```

Backend runs at:

```
http://127.0.0.1:5000
```

### Step 2: Start Dash Dashboard (New Terminal)

```bash
python dashboard.py
```

Dashboard runs at:

```
http://127.0.0.1:8050
```

---

## 🗄️ Database Information

* Database used: **SQLite**
* File name: `students.db`
* The database file is **automatically created** when data is first inserted
* No manual database setup is required

---

## 📊 How the Dashboard Works

1. Flask provides REST APIs for student data
2. Dash fetches data from Flask APIs
3. User selects:

   * Type of graph
   * Student (optional)
4. Charts and table update dynamically

---

## 🎯 Use Cases

* Academic performance analysis
* Subject-wise comparison
* Individual student evaluation
* Dashboard development practice
* Data visualization project

---

## 👨‍🎓 Author

**Student Name:** *Akhil Madesh Gudise*
**Course:** B.Tech CSE- AI and DE

---

⭐ If you like this project, feel free to extend and improve it!
