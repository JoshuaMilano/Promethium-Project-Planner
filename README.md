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

## How to actually run **Promethium Project Planner**
Writing native installation instructions that account for Python environments on both Windows and macOS is difficult, especially since this application was developed natively on **Arch Linux** using **WSL2**.

My solution is to utilise the exact same tools I use to provide preconfigured development environments for my business: **GitHub Codespaces** and **Docker**.

By containerizing the environment, Promethium is incredibly easy to spin up on any machine, directly in the browser.

**NOTE: THE DATABASE STORAGE IS TEMPORARY, AND WILL BE DELETED WHEN THE CODESPACE SHUTS DOWN!**

**To run Promethium Project Planner:**
1. Click the green **Code** button on this repository and select **Create codespace on main**.
2. Once the VS Code environment loads in your browser, click into the terminal and paste: `flask run --host=0.0.0.0`
3. When Flask starts, a pop-up will appear in the bottom right corner. Click **Open in Browser** to launch the live application. _(If the pop-up does not appear, click the **Ports** tab next to the terminal and click the globe icon next to Port 5000)._