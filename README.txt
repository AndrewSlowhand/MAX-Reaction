MAX Reaction Automation

PUBLIC/GITHUB VERSION

IMPORTANT:
This public version intentionally contains NO real institution/bot address.
Different institutions use different MAX bots, while the automation principle is the same.

BOT ADDRESS:
Before first use, open bot_url.txt and replace the placeholder with the actual MAX bot URL.
Example:
https://max.ru/YOUR_BOT

FIRST LOGIN:
1. Edit bot_url.txt.
2. Run login.bat.
3. Chromium opens.
4. The program automatically clicks "Открыть в браузере" when that page appears.
5. Complete MAX authorization manually if needed.

DAILY:
daily.bat reads the URL from bot_url.txt.
daily_hidden.vbs can be used for a hidden scheduled launch.

REACTIONS:
mode=both processes 👍, Полезно and 🔥 when the corresponding buttons are present.

BUILD:
Run build.bat on a Windows build PC with Python installed, then package_portable.bat.
Python is NOT required on the target PC.
