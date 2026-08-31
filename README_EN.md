# MAX Reaction

Browser-based automation for reactions and actions in MAX chat bots.

The project is intended for automating interaction with MAX bots. Different organizations may use different bot URLs, while the interaction principle remains the same.

> **Important:** starting with version 1.3.1, use a **direct MAX Web URL** (`https://web.max.ru/...`) for the bot/chat. This avoids interception by the installed MAX desktop application.

## Features

- automatic MAX launch using bundled Chromium;
- operation through the MAX Web version;
- automatic handling of the **"Open in browser"** button when it appears;
- 👍 reaction when available;
- **"Полезно" (Useful)** action when available;
- 🔥 reaction when available;
- persistent state for already processed messages;
- support for multiple MAX profiles;
- daily execution through Windows Task Scheduler;
- hidden execution without a visible CMD window;
- portable build: Python is not required on the target computer.

## 1. Configure the MAX Web URL

Open:

```text
bot_url.txt
```

and enter the **MAX Web URL of the required bot/chat**, for example:

```text
https://web.max.ru/YOUR_CHAT_ID
```

MAX officially provides its web version at `https://web.max.ru/`.

### How to get the URL

1. Open `https://web.max.ru/`.
2. Sign in to your MAX profile.
3. Open the required bot/chat.
4. Copy the URL from the browser address bar.
5. Paste it into `bot_url.txt`.

> Do not publish a specific organization's bot URL in the public repository unless you intend to make it public.

## 2. First run

Run:

```text
login.bat
```

The bundled Chromium browser will open MAX Web.

If the profile is not authorized yet, sign in to MAX.

After authorization, the script continues with the configured bot/chat.

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
login.bat "https://web.max.ru/123456789" account1
```

and:

```bat
login.bat "https://web.max.ru/123456789" account2
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
├── README_EN.md
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
