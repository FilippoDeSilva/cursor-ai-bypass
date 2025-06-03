# email_automation.py

import time
import re
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def solve_recaptcha(driver):
    """
    If a reCAPTCHA iframe appears, switch into it, click the “I'm not a robot” checkbox,
    then switch back to the main document.
    """
    try:
        WebDriverWait(driver, 5).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
            )
        )
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))
        ).click()
        logging.info("  ‣ Clicked reCAPTCHA checkbox on Temp-Mail-Plus.")
    except Exception:
        pass
    finally:
        driver.switch_to.default_content()


def get_temp_email(driver, timeout=30):
    """
    Navigate to Temp-Mail-Plus (https://tempmail.plus), solve reCAPTCHA if present,
    wait for the generated address, then return it.
    """
    TEMP_MAIL_URL = "https://tempmail.plus"
    logging.info("  ↪ Opening Temp-Mail-Plus for a disposable inbox…")
    driver.get(TEMP_MAIL_URL)

    # Solve any reCAPTCHA that pops up
    solve_recaptcha(driver)

    try:
        email_elem = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        temp_email = email_elem.get_attribute("value")
        logging.info(f"  ‣ Temp-Mail-Plus acquired: {temp_email}")
        return temp_email
    except Exception as e:
        logging.error(f"  ‣ Failed to get temp email from Temp-Mail-Plus: {e}")
        return None


def wait_for_confirmation_email(driver, timeout=180, poll_interval=5):
    """
    Poll the Temp-Mail-Plus inbox for a message with “cursor” or “confirm” in the subject.
    Once found, click it, switch into the email iframe, extract a “confirm” link, and return it.
    """
    logging.info("  ↪ Waiting for confirmation email via Temp-Mail-Plus…")
    deadline = time.time() + timeout

    while time.time() < deadline:
        # Solve reCAPTCHA again if it re-appears during polling
        solve_recaptcha(driver)

        # Look for list items in the inbox
        try:
            items = driver.find_elements(By.CSS_SELECTOR, "ul.message-list li")
        except Exception:
            items = []

        for itm in items:
            try:
                subj = itm.find_element(By.CSS_SELECTOR, ".subject").text.lower()
            except Exception:
                subj = ""
            if "cursor" in subj or "confirm" in subj:
                logging.info(f"  ‣ Found Temp-Mail-Plus email: {subj}")
                itm.click()
                # Wait for the email iframe to load
                WebDriverWait(driver, 15).until(
                    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#iframeMail"))
                )
                body_html = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
                driver.switch_to.default_content()
                m = re.search(r'href="([^"]*confirm[^"]*)"', body_html, re.IGNORECASE)
                if m:
                    confirm_url = m.group(1)
                    logging.info(f"  ‣ Extracted confirmation link: {confirm_url}")
                    return confirm_url
                else:
                    logging.warning("  ‣ No 'confirm' link found in email body.")
        time.sleep(poll_interval)

        # Click the refresh button if present
        try:
            driver.find_element(By.CSS_SELECTOR, ".refresh-btn").click()
        except Exception:
            pass

    logging.error("  ‣ Timed out waiting for confirmation email (Temp-Mail-Plus).")
    return None


def confirm_email_link(driver, confirm_url: str) -> bool:
    """
    Navigate to the confirmation URL and wait for “confirmed” or “verified” text.
    """
    logging.info("  ↪ Navigating to Cursor confirmation link…")
    try:
        driver.get(confirm_url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//*[contains(text(),'confirmed') or contains(text(),'verified') or contains(text(),'activated')]"
            ))
        )
        logging.info("  ‣ Cursor email confirmed successfully!")
        return True
    except Exception as e:
        logging.error(f"  ‣ Error confirming email in browser: {e}")
        return False
