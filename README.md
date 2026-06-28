# Promethium Project Planner
#### Video Demo:  <URL HERE>

## What is **Promethium Project Planner**
The idea of **Promethium** started out as a simple Trello clone. I needed to make a final project for **CS50x**, and I figured I might as well build a tool I could actually use in my day-to-day life to keep my projects organized.

To use Promethium, you need to create an account and access it from a desktop browser. If you try loading it on a phone, you'll hit a redirect asking you to switch devices. This is because Kanban boards don't really display well on mobile devices.

Once an account has been created, you can create boards, lists, and cards to track information, tasks, and jobs. All of this information is stored in a **SQLite3** database, allowing you to sign in, work, sign out, and when you're ready, sign back in again, and pick up where you left off.

## What technologies does **Promethium Project Planner** use?
### Frontend
For the frontend, **Promethium Project Planner** uses **HTML**, **Vanilla CSS**, **Vanilla Javascript**, **Jinja**, and **Lucide Icons**. Originally, **Promethium** was going to also make use of **Bootstrap**, but in the end, I opted to write fully custom **CSS** so I could have full control over the style and appearance of **Promethium**.

### Backend
For the backend, **Promethium Project Planner** runs on **Python**, **Flask**, and uses **Werkzeug Security** to hash and verify passwords.

I initially considered using the CS50 `SQLite3` library to handle database communication, but I decided instead to use the standard Python `SQLite3` library. This allowed me to write my own database helper functions (which you can find in *helpers.py* alongside the *@login_required* decorator).

Writing my own database helpers allowed me to not only learn more about database connections, but also enforce behaviour, such as setting `db.execute('PRAGMA foreign_keys = ON')`, as well as running the database through `row_factory` before returning it to *app.py* and *api.py*. Plus, by creating the helper function in one location, I didn't have to repeat it, allowing me to follow **DRY** principles.

### Database
For the Database, I went with `SQLite3` because it's serverless, requires almost no configuration, and exists as a single file which made switching machines practically seamless. Since Promethium is a relatively small application, it just didn't make sense to over-engineer it with a heavier database system.

The database schema is also structured to support drag-and-drop functionality and custom background colours, which I'll dive deeper into next.

### Side notes, Reflection, and Analysing the architecture of **Promethium Project Planner**
So, when building Promethium Project Planner, I had several goals in mind: Boards, Lists, and Cards with drag/drop functionality and support for changing their background colours; this is why the database technically supports drag/drop functionality and stores the default background colour of white.

My other goals were a fully functional account system, **SPA**-*like* behaviour, and an alliterative name, which is how I landed on the name **Promethium Project Planner**, and also why I chose the soft pink and white theme. Choosing that aesthetic is also ultimately why I scrapped the ability to add background colours.

As for the account system, the *user* can create an account, change their account username, change their password, and completely delete their account, with each one of these actions prompting a **notification**.

To jump back to what I was saying about the backend earlier, this is why writing my own database helper was so important. Because I *know* my helper function enables **foreign keys**, and my database makes use of `ON DELETE CASCADE`, I can safely delete users, boards, lists *and* cards without ever having to worry about orphans in the database.

Something else I'd like to note is the use of `jsonify`. Using tons of different routes just didn't feel right to me, and constantly reloading the page just to add and modify Kanban content was bad UX. To fix this, I decided to use Flask's `jsonify` throughout the application to dynamically generate, edit, and delete components. It communicates with the database in the background without breaking the user's flow.

## Every uploaded file, and what it does.
 - `.env.example` - **Promethium** uses a SECRET_KEY, which is stored in a .env file. The actual file has not been uploaded to github.
 - `requirements.txt` - These are the python requirements to run **Promethium**.
 - `Dockerfile` - This creates the environment, installs the requirements, exposes `port 5000`.
 - `devcontainer.json` - This tells github how to set up the codespace, and forwards `port 5000` to the browser. It also hides certain files within the codespace, and creates the database from `schema.sql`.
 - `schema.sql` - This is the schema used to create **Promethium's** SQLite3 database.
 - `helpers.py` - This contains the **database** and **loggin_required** python helpers.
 - `app.py` - This handles behaviour related to routes, such as boards, accounts, etc. This runs the app.
 - `api.py` - This handles behaviour unrelated to routes, such as creating boards, cards, updating user info, and more. This communicates with the Javascript.
 - `.gitignore` - Stops certains files from uploading the Github.
 - `helpers.js` - Contains helper functions for `scripts.js`. It currently contains a single function, but exists to accomodate for potential future development.
 - `scripts.js` - Communicates with `api.py` to create boards, lists, cards, and handle board updates and app behaviour.
 - `styles.css` - Contains all the styles for **Promethium Project Planner**.
 - `layout.html` - Base layout for the app.
 - `login.html` - Login page.
 - `register.html` - Registration page.
 - `index.html` - Main page that doesn't display boards, but has a logged-in user.
 - `board.html` - `app.py` uses this to generate the users board based on the database information.
 - `account.html` - Contains options to change the username, password, and delete the account.
 - `mobile.html` - Basic fullscreen page asking to user to switch to desktop.

## How to actually run **Promethium Project Planner**
Writing native installation instructions that account for Python environments on both Windows and macOS is difficult, especially since this application was developed natively on **Arch Linux** using **WSL2**.

My solution is to utilise the exact same tools I use to provide preconfigured development environments for my business: **GitHub Codespaces** and **Docker**.

By containerizing the environment, Promethium is incredibly easy to spin up on any machine, directly in the browser.

**NOTE: THE DATABASE STORAGE IS TEMPORARY, AND WILL BE DELETED WHEN THE CODESPACE SHUTS DOWN!**

**To run Promethium Project Planner:**
1. Click the green **Code** button on this repository and select **Create codespace on main**.
2. Once the VS Code environment loads in your browser, click into the terminal and paste: `flask run --host=0.0.0.0`
3. When Flask starts, a pop-up will appear in the bottom right corner. Click **Open in Browser** to launch the live application. _(If the pop-up does not appear, click the **Ports** tab next to the terminal and click the globe icon next to Port 5000)._