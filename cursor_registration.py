# cursor_registration.py

import logging
import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# The initial sign-up URL; Cursor’s JavaScript will redirect to the password step automatically
CURSOR_SIGNUP_URL = (
    "https://authenticator.cursor.sh/sign-up?state=%257B%2522returnTo%2522%253A%2522https%253A%252F%252Fwww.cursor.com%252Fdashboard%2522%257D&redirect_uri=https%3A%2F%2Fcursor.com%2Fapi%2Fauth%2Fcallback&authorization_session_id=01JWTJ8ZZFVGSXW5PJ4B4BFXFH"
)


def solve_recaptcha(driver):
    """
    If a reCAPTCHA iframe appears, switch into it and click the “I’m not a robot” checkbox,
    then switch back to the main document.
    """
    try:
        # Wait up to 10s for any iframe with “recaptcha” in its src
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
            )
        )
        # Click the checkbox inside
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))
        ).click()
        logging.info("  ‣ Clicked reCAPTCHA checkbox.")
    except Exception:
        # If no reCAPTCHA appears (or any error), continue quietly
        pass
    finally:
        driver.switch_to.default_content()


def human_type(element, text):
    """
    Type each character of `text` with a small random delay (0.1–0.3s),
    then wait 0.5–1.0s after finishing.
    """
    for ch in text:
        element.send_keys(ch)
        time.sleep(random.uniform(0.1, 0.3))
    time.sleep(random.uniform(0.5, 1.0))


def register_cursor_account(driver, first_name: str, last_name: str, email: str, password: str) -> bool:
    """
    Automate Cursor's two‐step sign‐up:

      Step 1:
        • firstName  (name="first_name")
        • lastName   (name="lastN_name")
        • email      (type="email" or placeholder="Email")
        → (brief pause)

      Step 2:
        • password   (name="password")
        → click “Sign up” → solve reCAPTCHA → wait for “check your email” or URL→“confirm”

    Returns True if successful; False otherwise.
    """
    try:
        logging.info("  ↪ Navigating to Cursor sign-up page…")
        driver.get(CURSOR_SIGNUP_URL)

        # ──────────── STEP 1: Fill firstName, lastName, email ────────────────────────
        WebDriverWait(driver, 30).until(
            EC.any_of(
                EC.visibility_of_element_located((By.NAME, "first_name")),
                EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='First name']"))
            )
        )

        # First Name
        try:
            fn_el = driver.find_element(By.NAME, "first_name")
        except:
            fn_el = driver.find_element(By.XPATH, "//input[@placeholder='First name']")
        fn_el.clear()
        human_type(fn_el, first_name)

        # Last Name
        try:
            ln_el = driver.find_element(By.NAME, "last_name")
        except:
            ln_el = driver.find_element(By.XPATH, "//input[@placeholder='Last name']")
        ln_el.clear()
        human_type(ln_el, last_name)

        # Email
        try:
            email_el = driver.find_element(By.XPATH, "//input[@type='email']")
        except:
            email_el = driver.find_element(
                By.XPATH,
                "//input[contains(@placeholder,'Email') or contains(@aria-label,'Email')]"
            )
        email_el.clear()
        human_type(email_el, email)

        # Small pause before next step
        time.sleep(random.uniform(0.5, 1.0))

        # Click “Continue” or “Next” on Step 1
        continue_xpath = "//button[contains(text(),'Continue') or contains(text(),'Next') or @type='submit']"
        driver.find_element(By.XPATH, continue_xpath).click()
        logging.info("  ‣ Submitted Step 1 (Name & Email). Waiting for Step 2…")
        time.sleep(random.uniform(1.5, 2.5))

        # ──────────── STEP 2: Fill password ───────────────────────────────────────────
        WebDriverWait(driver, 30).until(
            EC.any_of(
                EC.visibility_of_element_located((By.NAME, "password")),
                EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")),
                EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Password']"))
            )
        )

        # Password
        try:
            pw_el = driver.find_element(By.NAME, "password")
        except:
            pw_el = driver.find_element(By.XPATH, "//input[@type='password' or @placeholder='Password']")
        pw_el.clear()
        human_type(pw_el, password)

        # Small pause before clicking “Sign up”
        time.sleep(random.uniform(0.5, 1.0))

        # Click “Continue” or “Sign up” on Step 2
        submit_xpath = (
            "//button[contains(text(),'Continue') or contains(text(),'Next') "
            "or contains(text(),'Sign up') or @type='submit']"
        )
        driver.find_element(By.XPATH, submit_xpath).click()
        logging.info("  ‣ Submitted Step 2 (Password).")

        # ──────────── Solve reCAPTCHA (if it appears) on the post-password page ─────────
        # Wait up to 10s for reCAPTCHA iframe, then solve
        solve_recaptcha(driver)

        # Small pause to let the “confirm” page load
        time.sleep(random.uniform(1.5, 2.5))

        # ──────────── WAIT for “check your email” or URL → “confirm” ───────────────────
        WebDriverWait(driver, 30).until(
            EC.any_of(
                EC.url_contains("confirm"),
                EC.presence_of_element_located((
                    By.XPATH,
                    "//*[contains(text(),'check your email') "
                    "or contains(text(),'confirmation') "
                    "or contains(text(),'Thanks for signing')]"
                ))
            )
        )
        logging.info("  ‣ Sign-up accepted; please check your email to verify.")
        return True

    except Exception as e:
        logging.error(f"  ‣ Error during Cursor registration: {e}")
        return False
