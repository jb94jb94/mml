import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# === KONFIGURATION ===
URL = "https://machtmallaerm.de"
USERNAME = "Jonas"
PASSWORD = "REMOVED"
CSV_PATH = "battles.csv"  # Erwartet Spalten: url, mc1, mc2, event

# === BROWSER STARTEN ===
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get(URL)

# === LOGIN-MODAL ÖFFNEN ===
wait.until(EC.element_to_be_clickable((By.ID, "login-btn"))).click()
wait.until(EC.visibility_of_element_located((By.ID, "login-modal")))

# === LOGIN AUSFÜLLEN UND ABSENDEN ===
driver.find_element(By.ID, "username").send_keys(USERNAME)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
driver.find_element(By.ID, "login-submit-btn").click()

# === WARTEN, BIS LOGIN DURCH IST ===
wait.until(EC.invisibility_of_element_located((By.ID, "login-modal")))
wait.until(EC.visibility_of_element_located((By.ID, "add-btn")))

# === CSV LADEN UND EINTRÄGE HOCHLADEN ===
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(f"➕ Lade Battle hoch: {row['mc1']} vs {row['mc2']}")

        # === ADD-MODAL ÖFFNEN ===
        wait.until(EC.element_to_be_clickable((By.ID, "add-btn"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "battle-url")))

        # === FELDER AUSFÜLLEN ===
        driver.find_element(By.ID, "battle-url").clear()
        driver.find_element(By.ID, "battle-url").send_keys(row["url"])

        driver.find_element(By.ID, "battle-artist1").clear()
        driver.find_element(By.ID, "battle-artist1").send_keys(row["mc1"])

        driver.find_element(By.ID, "battle-artist2").clear()
        driver.find_element(By.ID, "battle-artist2").send_keys(row["mc2"])

        # === EVENT SUCHEN UND AUSWÄHLEN (per Teilstring) ===
        event_dropdown = Select(driver.find_element(By.ID, "battle-event-select"))
        target_substring = row["event"].strip().lower()
        selected = False

        for option in event_dropdown.options:
            if target_substring in option.text.strip().lower():
                event_dropdown.select_by_visible_text(option.text)
                selected = True
                break

        if not selected:
            print(f"⚠️ Kein passendes Event gefunden für: {row['event']}")
            continue  # Überspringe diesen Eintrag

        # === SPEICHERN ===
        driver.find_element(By.ID, "battle-save-btn").click()
        time.sleep(1.5)  # Modal darf nicht mehr offen sein, bevor es weitergeht

# === BROWSER SCHLIESSEN ===
print("✅ Alle Battles verarbeitet.")
driver.quit()
