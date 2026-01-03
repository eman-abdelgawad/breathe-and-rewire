# PROJECT TITLE: Breathe & Rewire

#### Description:

Breathe & Rewire is a breathwork Web application that is designed to help users practice structured breathing techniques. Users can create a profile, log in, choose a breathwork pattern, practice it through a guided interface, and save their completed sessions.

**Why I chose this project?**
Movement and breathwork (breathing exercises) have a profound impact on my life, helping me experience a calmer and more balanced way of being. For this reason it was the first idea that came to my mind when choosing the final project. Each mindful breath gently retrains your nervous system, inviting calm and building resilience. Through this project, I hope to encourage exploration without self-judgment or self-stereotyping. Find the form of movement and breathwork that works for you.

---

#### Features (Overview)

- User authentication (registration and login).
- Default and customizable Breathwork patterns.
- Guided breathing sessions with timers.
- Session history tracking.
- Responsive and clean user interface

---

#### Feature Details:

**User authentication:**

- Users can register with a name and password.
- Registered users can log in to access all application features.
- Users can log out.

**Breathworks Types**

There are two types of breathworks:

1. The default breathworks:
   Pre-defined breathing patterns stored in the database and automatically available to every user.
2. The custom breathworks:
   Users can create their own breathwork patterns and fully control their configuration.

**Custom Breathwork Fields:**
Each breathwork has these data fields:

- Name
- Description
- Inhale (seconds, > 0)
- Inhale hold (seconds, >= 0)
- Exhale (seconds, >= 0)
- Exhale hold (seconds, > 0)
- Rounds (integer >= 1)

**Edit Custom Breathworks**

Users can:
- Create
- Edit and Update
- Delete
their custom breathing patterns.

**Practice Mode**

Once the user starts any breathwork:

- The current round and total rounds are displayed.
- The current phase (inhale, hold, exhale, etc.) and its countdown timer appear.
- A dynamic visual progress bar indicates the active phase progress.
- Users can end the session at any time or at the end of all phases. Completed sessions are saved with:
    - Breathwork name
    - Duration (minutes and seconds)
    - User notes
    - Date of the session

**Session History**

- Users can access all previously saved sessions.
- User can delete any of saved session history.

**Settings**
Users can change their password in settings page.

**Responsive and clean user interface**

The layout adapts to different screen sizes while maintaining readability and visual calm.

---

##### Technologies Used

- Python / Flask
- SQLite
- HTML, CSS, JavaScript
- Bootstrap

---

#### Installation/How to Run

This project was developed in CS50.dev. To run the application:
1. Navigate to the project directory
2. Install dependencies: ``` pip install -r requirements.txt ```
3. Run the Flask application: ``` flask run ```
4. Open the provided URL in your browser

---

##### Project Structure

```
project/
│
├── static/
│   ├── styles.css
├── templates/
│   ├── apology.html
│   ├── history.html
│   ├── login.html
│   ├── settings.html
│   ├── edit-breathwork.html
│   ├── index.html
│   ├── practice.html
│   ├── editor.html
│   ├── layout.html
│   └── register.html
│
├── app.py
├── helpers.py
├── requirements.txt
├── breathwork.db
└── README.md
```

---

#### File Descriptions

**`app.py`**
Main Flask application entry point.
Defines all routes, handles request/response logic, manages session state, and connects user actions (login, practice, editor, history, settings) to the appropriate templates and database operations.

**`helpers.py`**
Contains reusable helper functions used across the application, such as authentication checks, validation logic, which keep `app.py` concise and readable.

**`requirements.txt`**
Lists all Python dependencies required to run the application, ensuring a consistent setup across environments.

**`breathwork.db`**
SQLite database storing user accounts, breathwork patterns, and session history.

##### `templates/`

Contains all HTML templates rendered by Flask using Jinja2.

**`layout.html`**
  Base template shared by all pages. Defines the common layout, navigation, and global structure.

**`index.html`**
  The landing page that introduces the application and provides entry points to key actions. It displays all the available breathworks patterns for users to browse and choose from.

**`login.html`** / **`register.html`**
  Authentication pages for user login and account creation.

**`apology.html`**
  Displays error messages and user-friendly feedback when invalid actions occur.

**`practice.html`**
  Core interaction page where users perform guided breathwork sessions. It provides the breathing guidance and displays the timer when the user starts a breathwork session.

**`editor.html`**
  Main interface for creating and managing custom breathwork patterns. Users can:
  - Create new custom breathwork patterns.
  - View a table of their created breathwork patterns with options to edit or delete them.

**`edit-breathwork.html`**
  Allows users to modify an existing custom breathwork pattern.

**`history.html`**
  Displays previously completed breathwork sessions for the logged-in user.

**`settings.html`**
  User settings page that allows authenticated users to change their password.

##### `static/`

Contains static assets used by the application.

**`styles.css`**
  Defines the visual styling and layout of the application UI.

---

##### Design Choices

Several design decisions were made during development:

1. **Repeated reloading of the page "editor":**

   **Context**
   The editor page allows users to:
   - Create a new custom breathwork.
   - View a table of existing custom breathworks with options to:
	   - Edit
	   - Delete

   **The problem:**
   I first implemented it using regular http requests and the page needed to reload:
   - after each creation of new breathwork.
   - after each deletion of old breathwork.

   **The solution:**
   I reimplemented the logic using AJAX, which allowed the table to update instantly without reloading the entire page. This solution improved the user experience, though it introduced a new challenge to handle.

   **The new problem after solving the original one:**
   The newly created breathwork items are added to the table with "Edit" and "delete" buttons. Initially, I attached the event listener only to the existing rows when the page is loaded. As a result, the newly added rows did not respond to user interactions.

   **Solution: Event Delegation**
   I implemented event delegation in JavaScript, which is a technique for handling events efficiently by attaching a single event listener to a parent element instead of individual child elements. This approach leverages the concept of event bubbling, where events initiated on a child element propagate up through its ancestor elements in the DOM tree. It allows users to edit or delete dynamically added breathwork items seamlessly.

2. **UI Design**

   **Context**
   Initially, the UI consisted of a select menu where users could choose a breathwork session. The corresponding information was displayed, but users had to repeat the process to view information about another breathwork.

   **Problem**
   This design resulted in a poor UI and a bad user experience, with excessive cognitive load. Users had to remember multiple breathwork details in order to decide which session to practice.

   **Solution**
   I redesigned the index page to display all breathworks as cards, allowing users to view information at a glance and choose a session more easily. This solution introduced a new challenge, as the page became overwhelming for users.

   To address this, I separated default and custom breathworks into two sections. JavaScript and CSS were used to create toggle buttons that allow users to control which category of breathworks is displayed.
