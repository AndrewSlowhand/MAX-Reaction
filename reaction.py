from pathlib import Path
import argparse
import hashlib
import json
import logging
import re
import sys
import os
from datetime import datetime
from urllib.parse import urlparse

# Set paths before Playwright is imported.
# In a PyInstaller --onedir build, __file__ points inside _internal,
# while the bundled ms-playwright folder is placed beside the EXE.
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
PROFILES_DIR = DATA_DIR / "profiles"
LOG_DIR = DATA_DIR / "logs"
BROWSERS_DIR = BASE_DIR / "ms-playwright"

if BROWSERS_DIR.exists():
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(BROWSERS_DIR)

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

LIKE_SELECTOR = '.inlineKeyboard button[aria-label^="👍"]'
BUTTON_SELECTOR = '.inlineKeyboard button'


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("bot_url")
    p.add_argument("mode", nargs="?", default="both",
                   choices=["like", "useful", "fire", "both"])
    p.add_argument("--profile", default="default")
    p.add_argument("--headed", action="store_true")
    return p.parse_args()


def safe_name(value):
    return (re.sub(r"[^0-9A-Za-zА-Яа-я._-]+", "_", value) or "default")[:80]


def dirs(profile):
    DATA_DIR.mkdir(exist_ok=True)
    PROFILES_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
    d = PROFILES_DIR / safe_name(profile)
    d.mkdir(exist_ok=True)
    return d


def setup_logging(profile):
    log = LOG_DIR / f"{safe_name(profile)}.log"
    logging.basicConfig(
        filename=log, level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8")
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)


def state_path(profile, bot_url):
    key = hashlib.sha256(bot_url.encode("utf-8")).hexdigest()[:16]
    return DATA_DIR / f"state_{safe_name(profile)}_{key}.json"


def load_state(path):
    if not path.exists():
        return {"like_message_id": None, "useful_message_id": None, "fire_message_id": None,
                "last_run": None, "bot_url": None}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        logging.exception("Ошибка чтения state")
        return {"like_message_id": None, "useful_message_id": None, "fire_message_id": None,
                "last_run": None, "bot_url": None}


def save_state(path, state):
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2),
                    encoding="utf-8")


def message_id(text):
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def parent_message(button):
    return button.locator(
        "xpath=ancestor::div[contains(@class, 'messageWrapper')]"
    )


def find_useful(page):
    buttons = page.locator(BUTTON_SELECTOR)
    result = []
    for i in range(buttons.count()):
        b = buttons.nth(i)
        try:
            t = re.sub(r"\s+", " ", b.inner_text(timeout=1000).strip())
        except Exception:
            continue
        if re.fullmatch(r"✅?\s*Полезно", t, flags=re.I):
            result.append(b)
    return result


def find_fire(page):
    """Find visible fire reaction buttons (🔥) in the current bot post."""
    buttons = page.locator(BUTTON_SELECTOR)
    result = []
    for i in range(buttons.count()):
        b = buttons.nth(i)
        try:
            t = re.sub(r"\s+", " ", b.inner_text(timeout=1000).strip())
        except Exception:
            continue
        if t == "🔥":
            result.append(b)
    return result


def open_bot_in_browser(page, context):
    """Click MAX's intermediate 'Открыть в браузере' link if shown."""
    try:
        candidates = [
            page.get_by_text("Открыть в браузере", exact=True),
            page.locator('a').filter(has_text="Открыть в браузере"),
            page.locator('button').filter(has_text="Открыть в браузере"),
        ]

        link = None
        for candidate in candidates:
            try:
                if candidate.count() > 0 and candidate.first.is_visible(timeout=1200):
                    link = candidate.first
                    break
            except Exception:
                continue

        if link is None:
            logging.info("Промежуточной кнопки 'Открыть в браузере' нет.")
            return page

        logging.info("MAX: нажимаю 'Открыть в браузере'.")
        link.scroll_into_view_if_needed()
        page.wait_for_timeout(300)

        old_url = page.url
        old_pages = set(context.pages)
        try:
            with context.expect_page(timeout=5000) as page_info:
                link.click(timeout=10000)
            new_page = page_info.value
            new_page.wait_for_load_state("domcontentloaded", timeout=30000)
            new_page.wait_for_timeout(2500)
            logging.info("MAX открыл браузерную страницу: %s", new_page.url)
            return new_page
        except PlaywrightTimeoutError:
            # Most likely the click navigated the existing tab.
            try:
                page.wait_for_timeout(2500)
            except Exception:
                pass
            new_pages = [p for p in context.pages if p not in old_pages]
            if new_pages:
                p2 = new_pages[-1]
                try:
                    p2.wait_for_load_state("domcontentloaded", timeout=30000)
                    p2.wait_for_timeout(1500)
                except Exception:
                    pass
                logging.info("MAX открыл новую вкладку: %s", p2.url)
                return p2
            logging.info("MAX продолжил работу в текущей вкладке: %s -> %s", old_url, page.url)
            return page
    except Exception:
        logging.exception("Не удалось автоматически нажать 'Открыть в браузере'")
        return page


def find_chromium_executable():
    """Find bundled Chromium executable in the portable ms-playwright folder."""
    if not BROWSERS_DIR.exists():
        return None

    # Playwright browser folder names contain a version/build number,
    # so never depend on a fixed chromium-XXXX directory.
    matches = list(BROWSERS_DIR.rglob("chrome.exe"))
    if not matches:
        return None

    # Prefer the normal Chromium executable if several files are present.
    matches.sort(key=lambda p: (
        "chrome-win64" not in str(p).lower(),
        "chrome-win" not in str(p).lower(),
        len(p.parts),
    ))
    return matches[0]


def process_like(page, state):
    buttons = page.locator(LIKE_SELECTOR)
    try:
        buttons.first.wait_for(state="attached", timeout=5000)
    except PlaywrightTimeoutError:
        logging.info("👍: кнопок нет.")
        return False

    if buttons.count() == 0:
        return False

    b = buttons.last
    m = parent_message(b)
    try:
        text = m.inner_text(timeout=5000).strip()
    except Exception:
        logging.exception("👍: не удалось прочитать сообщение")
        return False

    mid = message_id(text)
    if state.get("like_message_id") == mid:
        logging.info("👍: уже обработано.")
        return False

    logging.info("👍: нажимаю. %s", text[:300])
    b.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    b.click(timeout=10000)
    page.wait_for_timeout(1200)
    state["like_message_id"] = mid
    return True


def process_useful(page, state):
    buttons = find_useful(page)
    if not buttons:
        logging.info("Полезно: кнопок нет.")
        return False

    b = buttons[-1]
    m = parent_message(b)
    try:
        text = m.inner_text(timeout=5000).strip()
    except Exception:
        logging.exception("Полезно: не удалось прочитать сообщение")
        return False

    mid = message_id(text)
    if state.get("useful_message_id") == mid:
        logging.info("Полезно: уже обработано.")
        return False

    logging.info("Полезно: нажимаю. %s", text[:300])
    b.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    b.click(timeout=10000)
    page.wait_for_timeout(1200)
    state["useful_message_id"] = mid
    return True


def process_fire(page, state):
    """Click the 🔥 reaction on the newest post when that button is present."""
    buttons = find_fire(page)
    if not buttons:
        logging.info("🔥: кнопок нет.")
        return False

    b = buttons[-1]
    m = parent_message(b)
    try:
        text = m.inner_text(timeout=5000).strip()
    except Exception:
        logging.exception("🔥: не удалось прочитать сообщение")
        return False

    mid = message_id(text)
    if state.get("fire_message_id") == mid:
        logging.info("🔥: уже обработано.")
        return False

    logging.info("🔥: нажимаю. %s", text[:300])
    b.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    b.click(timeout=10000)
    page.wait_for_timeout(1200)
    state["fire_message_id"] = mid
    return True


def main():
    args = parse_args()

    u = urlparse(args.bot_url)
    if u.scheme not in ("http", "https") or not u.netloc:
        print("Некорректный URL MAX.")
        return 2

    profile_dir = dirs(args.profile)
    setup_logging(args.profile)
    st_path = state_path(args.profile, args.bot_url)
    state = load_state(st_path)
    state["bot_url"] = args.bot_url

    logging.info("=" * 60)
    logging.info("bot=%s mode=%s profile=%s headed=%s",
                 args.bot_url, args.mode, args.profile, args.headed)

    executable_path = find_chromium_executable()
    if executable_path:
        logging.info("Использую встроенный Chromium: %s", executable_path)
    else:
        logging.warning("Встроенный Chromium не найден; Playwright попробует найти браузер сам.")

    with sync_playwright() as p:
        launch_kwargs = dict(
            user_data_dir=str(profile_dir),
            headless=not args.headed,
            viewport={"width": 1400, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        if executable_path:
            launch_kwargs["executable_path"] = str(executable_path)

        context = p.chromium.launch_persistent_context(**launch_kwargs)
        try:
            page = context.pages[0] if context.pages else context.new_page()
            page.goto(args.bot_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)

            # MAX can first show a bot landing page. Open the actual browser chat.
            page = open_bot_in_browser(page, context)
            page.wait_for_timeout(2500)

            if "login" in page.url.lower():
                logging.error("MAX требует авторизацию.")
                print("MAX не авторизован. Запустите login.bat.")
                return 3

            changed = False
            if args.mode in ("like", "both"):
                changed |= process_like(page, state)
                save_state(st_path, state)

            if args.mode in ("useful", "both"):
                changed |= process_useful(page, state)
                save_state(st_path, state)

            if args.mode in ("fire", "both"):
                changed |= process_fire(page, state)
                save_state(st_path, state)

            state["last_run"] = datetime.now().isoformat(timespec="seconds")
            save_state(st_path, state)

            logging.info("Результат: %s",
                         "реакция отправлена" if changed else "новых реакций нет")
            return 0
        except Exception:
            logging.exception("Критическая ошибка")
            print("Ошибка. Смотрите data\\logs.")
            return 1
        finally:
            context.close()


if __name__ == "__main__":
    sys.exit(main())
