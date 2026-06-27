# What is **Promethium**?
**Promethium** is just a simple Trello clone. I needed to make a final project for **CS50x**, and this is what I settled on.

# What technologies does **Promethium** use?
## Frontend
 - **HTML**
 - **CSS**
 - **Jinja**
 - **Lucide Icons**

## Backend
 - **Python**
 - **Flask**

## Database
 - **SQLite**

## How to actually run **Promethium Project Planner**
Writing native installation instructions that account for Python environments on both Windows and macOS is difficult, especially since this application was developed natively on **Arch Linux** using **WSL2**.

To bypass the "it only works on my machine" problem, I leveraged the exact same tools I use to provide preconfigured development environments for my business: **GitHub Codespaces** and **Docker**.

By containerizing the environment, Promethium is incredibly easy to spin up on any machine, directly in the browser. **NOTE: DATABASE STORAGE IS TEMPORARY!**

**To run Promethium Project Planner:**
1. Click the green **Code** button on this repository and select **Create codespace on main**.
2. Once the VS Code environment loads in your browser, click into the terminal and paste: `flask run --host=0.0.0.0`
3. When Flask starts, a pop-up will appear in the bottom right corner. Click **Open in Browser** to launch the live application. _(If the pop-up does not appear, click the **Ports** tab next to the terminal and click the globe icon next to Port 5000)._