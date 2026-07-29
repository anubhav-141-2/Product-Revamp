# CareerSprint

A simple way to keep track of job and internship applications in one place.

## About

CareerSprint is a web application for students and job seekers who want to stay organized during the hiring process. Instead of relying on spreadsheets, sticky notes, or memory, it helps users record each application, track progress, save interview details, and keep notes in one place.

The goal is simple: users should be able to manage their applications without missing interviews, assessments, or opportunities.

## Features

### User Authentication

- Create an account
- Log in and log out securely
- Use a personal dashboard

### Job Application Management

Users can:

- add a new application
- view all applications
- update application details
- delete an application

Each application can include:

- company name
- job role
- application date
- source
- current status
- notes

### Application Status Tracking

Applications can move through the hiring process in stages.

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

- Applied
- OA Scheduled
- OA Completed
- Interview
- Offer
- Rejected
- Withdrawn

### Interview Tracking

Interview rounds are tracked inside each application. When an application reaches the interview stage, users can add interview rounds with details such as round number, round type, interview date, result, and notes.

### Notes

Users can keep notes about recruiter conversations, interview preparation, referrals, or feedback after interviews.

### Search and Filter

Users can search by company name and filter applications by status to quickly find the opportunities they need to follow up on.

### Dashboard

The dashboard shows:

- total applications
- applications in interview
- offers received
- rejections

## Target Users

### Final-Year Students

- applying to multiple companies during placement season
- tracking interview schedules
- keeping all applications in one place

### Internship Seekers

- applying through LinkedIn, Internshala, and company portals
- needing a better way to stay organized
- keeping interview notes in one place

### Professionals

- looking for a job switch
- managing several interviews at once
- keeping track of recruiter conversations

## Application Workflow

<img width="400" height="1000" alt="image" src="https://github.com/user-attachments/assets/d2a3e6f7-391a-48bf-aac7-048f1b5ceb01" />

## Screens

- Login / Register
- Dashboard
- Add Application
- Application Details
- Status Update
- Interview Tracker

## Database Design

### User

| Field | Type |
| ----- | ---- |
| userId | Integer |
| name | String |
| email | String |
| password | String |

### Application

| Field | Type |
| ----- | ---- |
| applicationId | Integer |
| companyName | String |
| role | String |
| applicationDate | Date |
| source | String |
| status | Enum |
| notes | Text |
| userId | Integer |

### Interview Round

| Field | Type |
| ----- | ---- |
| roundId | Integer |
| applicationId | Integer |
| roundNumber | Integer |
| roundType | String |
| interviewDate | Date |
| result | Enum |
| notes | Text |

## Entity Relationship

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

One user can have many applications.

One application can have many interview rounds.

## Business Rules

- Users must log in before accessing their data.
- Every application belongs to one user.
- Users can only manage their own applications.
- Company name and role are required.
- Interview rounds are available only when an application status is Interview.
- An application can have multiple interview rounds.
- Interview rounds are not removed automatically when the application status changes.
- Deleting an application removes all related interview rounds.

## MVP Features

- User registration
- Login and logout
- Dashboard
- Add, edit, and delete applications
- Update application status
- Search and filter
- Notes
- Interview round tracking
- Basic dashboard statistics

## Future Enhancements

- Resume repository
- Referral tracker
- Calendar integration
- Deadline reminders
- Email notifications
- Dark mode
- Advanced analytics
- Export applications

## Out of Scope

The following items are not part of the initial version:

- LinkedIn integration
- Automatic job import
- AI interview coach
- Recruiter portal
- Company accounts
- Mobile application

## Tech Stack

### Frontend

- React.js
- HTML5
- CSS3
- JavaScript

### Backend

- Spring Boot

### Database

- MySQL

### Tools

- Git
- GitHub
- Maven
- Postman

## UI Preview

Actual screenshots will be added after the first version is built.Below are some of AI built screenshots that can help someone understand what we are building:
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/baeb498d-a245-4204-8242-4273c66b139a" />
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/e67af3d3-4405-41cd-bddd-bb9897174d81" />




## License

This project was created as part of a software development training assignment and is intended for educational purposes.
