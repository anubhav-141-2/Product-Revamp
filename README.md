# 🚀 CareerSprint

<p align="center">

**Track Every Job Application. Never Miss an Opportunity.**

*A simple and intuitive job application tracker for students and job seekers.*

</p>

---

## 📖 About

CareerSprint is a web application that helps students and job seekers organize and track their job and internship applications from one centralized dashboard.

Instead of relying on spreadsheets, sticky notes, or memory, CareerSprint allows users to record every application, monitor hiring progress, store interview details, and keep important notes throughout the recruitment process.

> **🎯 Success Metric:** A user should be able to manage all their job applications in one place and never miss an interview, assessment, or opportunity.

---

# ✨ Features

### 👤 User Authentication

* Register a new account
* Secure Login & Logout
* User-specific dashboard

---

### 💼 Job Application Management

Users can:

* ➕ Add a new application
* 👀 View all applications
* ✏️ Edit application details
* ❌ Delete an application

Each application stores:

* Company Name
* Job Role
* Application Date
* Source (LinkedIn, Referral, Careers Page, etc.)
* Current Status
* Personal Notes

---

### 📊 Application Status Tracking

Every application progresses through the hiring pipeline.

```text
Applied
   │
   ▼
OA Scheduled
   │
   ▼
OA Completed
   │
   ▼
Interview
   │
   ├──────────────► Rejected
   │
   ▼
Offer
```

Possible statuses:

* Applied
* OA Scheduled
* OA Completed
* Interview
* Offer
* Rejected
* Withdrawn

---

### 🎤 Interview Tracking

Interview rounds are tracked **inside an application**.

Once an application's status becomes **Interview**, an additional **Interview Rounds** section appears.

Each round stores:

* Round Number
* Round Type
* Interview Date
* Result
* Notes

Example

```text
Google

Status : Interview

Interview Rounds

✓ Round 1
Technical
Passed

✓ Round 2
System Design
Passed

○ Round 3
HR
Scheduled
```

This allows users to monitor both the overall application status and the progress of individual interview rounds.

---

### 📝 Notes

Every application includes personal notes such as:

* Recruiter details
* Interview preparation
* Referral information
* Feedback after interviews

---

### 🔍 Search & Filter

Users can:

* Search by company name
* Filter by application status
* Quickly find active opportunities

---

### 📈 Dashboard

A simple dashboard displays:

* Total Applications
* Applications in Interview Stage
* Offers Received
* Rejections

---

# 👥 Target Users

### 🎓 Final-Year Students

* Applying to multiple companies during placement season
* Need to track interview schedules
* Want a centralized application tracker

---

### 💼 Internship Seekers

* Applying through LinkedIn, Internshala, and company portals
* Need better organization
* Want to keep interview notes

---

### 👨‍💻 Professionals

* Looking for a job switch
* Managing multiple interviews
* Tracking recruiter interactions

---

# 📱 Application Workflow

```text
Register/Login
      │
      ▼
Dashboard
      │
      ▼
Add Job Application
      │
      ▼
View Application Details
      │
      ├─────────────► Edit Application
      │
      ├─────────────► Add Notes
      │
      ├─────────────► Update Status
      │
      ▼
Status = Interview ?
      │
      ├── No → Done
      │
      ▼
Interview Rounds
      │
      ├── Add Round
      ├── Edit Round
      └── Delete Round
```

---

# 🖥️ Screens

* 🔐 Login / Register
* 📊 Dashboard
* ➕ Add Job Application
* 📄 Application Details
* ✏️ Update Application Status
* 🎤 Interview Round Tracker

---

# 🗂️ Database Design

## User

| Field    | Type    |
| -------- | ------- |
| userId   | Integer |
| name     | String  |
| email    | String  |
| password | String  |

---

## Application

| Field           | Type    |
| --------------- | ------- |
| applicationId   | Integer |
| companyName     | String  |
| role            | String  |
| applicationDate | Date    |
| source          | String  |
| status          | Enum    |
| notes           | Text    |
| userId          | Integer |

---

## Interview Round

| Field         | Type    |
| ------------- | ------- |
| roundId       | Integer |
| applicationId | Integer |
| roundNumber   | Integer |
| roundType     | String  |
| interviewDate | Date    |
| result        | Enum    |
| notes         | Text    |

---

# 🔗 Entity Relationship

```text
User
 │
 │ 1
 │
 ▼
Applications
 │
 │ 1
 │
 ▼
Interview Rounds
```

One User → Many Applications

One Application → Many Interview Rounds

---

# 📌 Business Rules

* Users must log in before accessing data.
* Every application belongs to one user.
* Users can only manage their own applications.
* Company name and role are mandatory.
* Interview rounds are available only when the application status is **Interview**.
* An application can have multiple interview rounds.
* Interview rounds are **never deleted automatically** when the application status changes.
* Deleting an application removes all associated interview rounds.

---

# 🚀 MVP Features

* ✅ User Registration
* ✅ Login & Logout
* ✅ Dashboard
* ✅ Add/Edit/Delete Applications
* ✅ Update Application Status
* ✅ Search & Filter
* ✅ Notes
* ✅ Interview Round Tracking
* ✅ Basic Dashboard Statistics

---

# 🌟 Future Enhancements

* 📄 Resume Repository
* 🤝 Referral Tracker
* 📅 Calendar Integration
* 🔔 Deadline Reminders
* 📧 Email Notifications
* 🌙 Dark Mode
* 📊 Advanced Analytics
* 📤 Export Applications

---

# ❌ Out of Scope

The following are intentionally excluded from the MVP:

* LinkedIn Integration
* Automatic Job Import
* AI Interview Coach
* Recruiter Portal
* Company Accounts
* Mobile Application

---

# 🛠️ Tech Stack

## Frontend

* React.js
* HTML5
* CSS3
* JavaScript

## Backend

* Spring Boot

## Database

* MySQL

## Tools

* Git
* GitHub
* Maven
* Postman

---

# 📸 UI Preview

> Screenshots of the application will be added after implementation.

---

# 📄 License

This project is developed as part of a Software Development training assignment and is intended for educational purposes.

---

<p align="center">

⭐ **CareerSprint helps job seekers stay organized, track every opportunity, and confidently navigate the hiring process.**

</p>
