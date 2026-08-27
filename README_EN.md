# MAX Reaction

Browser-based automation for reactions and actions in MAX chat bots.

The project is intended for automating interaction with MAX bots. Different organizations may use different bot URLs, while the interaction principle remains the same.

> **Important:** This project does not contain the URL of any specific bot. Before the first run, the user must provide the URL of the MAX bot they want to use.

## Features

- automatic MAX launch using bundled Chromium;
- automatic handling of the **"Open in browser"** button when it appears;
- 👍 reaction when available;
- **"Полезно" (Useful)** action when available;
- 🔥 reaction when available;
- persistent state for already processed messages;
- support for multiple MAX profiles;
- daily execution through Windows Task Scheduler;
- hidden execution without a visible CMD window;
- portable build: Python is not required on the target computer.

## How it works

```text
Start
  ↓
Chromium
  ↓
MAX bot
  ↓
"Open in browser" (if shown)
  ↓
MAX profile
  ↓
New posts
  ↓
👍 / Useful / 🔥
```

## 1. Configure your bot

Open:

```text
bot_url.txt
```

and enter the URL of the MAX bot you want to use, for example:

```text
https://max.ru/YOUR_BOT
```

Different organizations can use different MAX bots. No code changes are required — only the bot URL needs to be changed.

## 2. First run

Run:

```text
login.bat
```

Chromium will open.

If MAX displays the **"Open in browser"** button, the program will click it automatically.

Then sign in to the required MAX profile.

## 3. Daily execution

For a manual test:

```text
daily.bat
```

For hidden execution:

```text
daily_hidden.vbs
```

The hidden launcher is convenient for Windows Task Scheduler.

## Reactions

The default:

```text
both
```

mode processes the available actions:

- 👍;
- **Полезно (Useful)**;
- 🔥.

If a particular button is not present in a post, it is skipped.

## Multiple profiles

Different MAX profiles can be stored separately.

For example:

```bat
login.bat "https://max.ru/example_bot" account1
```

and:

```bat
login.bat "https://max.ru/example_bot" account2
```

## Build

On the developer/build computer:

```text
build.bat
```

After building, create the portable package with:

```text
package_portable.bat
```

Python is not required on the target computer when using the portable build.

The portable package includes the required Chromium browser.

## Windows Task Scheduler

The recommended hidden launch method is:

```text
wscript.exe
```

with:

```text
daily_hidden.vbs
```

as the argument.

This allows the automation to run without a visible command prompt window.

## Project structure

```text
MAX-Reaction/
├── README.md
├── README_RU.md
├── LICENSE
├── .gitignore
├── bot_url.txt
├── reaction.py
├── build.bat
├── login.bat
├── daily.bat
├── daily_hidden.vbs
├── package_portable.bat
└── VERSION.txt
```

## Requirements

### Developer/build computer

- Windows;
- Python;
- internet access for dependencies and Chromium;
- PyInstaller.

### Portable target computer

- Windows;
- Python is not required;
- separate Chromium installation is not required.

## Security

Do not publish the following to GitHub:

- login credentials;
- cookies;
- profile directories;
- `data/` contents;
- private configuration files;
- bot URLs you do not want to make public.

## License

This project is distributed under the license specified in `LICENSE`.

---

If you find the project useful, consider giving the repository a ⭐.
