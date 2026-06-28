# Promethium Project Planner
#### Video Demo:  <URL HERE>

# What is **Promethium Project Planner**
**Promethium** started out as a simple Trello clone. I needed to make a final project for **CS50x**, and I figured I might as well build a tool I could actually use in my day-to-day life to keep my projects organized.

To use Promethium, you need to create an account and access it from a desktop browser. If you try loading it on a phone, you'll hit a redirect asking you to switch devices. This is because Kanban boards don't really display well on mobile devices.

Once an account has been created, you can create boards, lists, and cards to track information, tasks, and jobs. All of this information is stored in a **SQLite3** database, allowing you to sign in, work, sign out, and when you're ready, sign back in again, and pick up where you left off.

## How to actually run **Promethium Project Planner**
Writing native installation instructions that account for Python environments on both Windows and macOS is difficult, especially since this application was developed natively on **Arch Linux** using **WSL2**.

My solution is to utilise the exact same tools I use to provide preconfigured development environments for my business: **GitHub Codespaces** and **Docker**.

By containerizing the environment, Promethium is incredibly easy to spin up on any machine, directly in the browser.

**NOTE: THE DATABASE STORAGE IS TEMPORARY, AND WILL BE DELETED WHEN THE CODESPACE SHUTS DOWN!**

**To run Promethium Project Planner:**
1. Click the green **Code** button on this repository and select **Create codespace on main**.
2. Once the VS Code environment loads in your browser, click into the terminal and paste: `flask run --host=0.0.0.0`
3. When Flask starts, a pop-up will appear in the bottom right corner. Click **Open in Browser** to launch the live application. _(If the pop-up does not appear, click the **Ports** tab next to the terminal and click the globe icon next to Port 5000)._