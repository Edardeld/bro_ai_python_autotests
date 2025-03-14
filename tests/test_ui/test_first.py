import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker


@pytest.fixture
def browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def base_url():
    return "http://95.182.122.183"


@pytest.fixture
def wait(browser):
    return WebDriverWait(browser, 10)


@pytest.fixture
def faker_data():
    fake = Faker("ru_RU")
    return {
        "email": fake.ascii_free_email(),
        "name": fake.first_name(),
        "password": fake.password(length=8)
    }


# Регистрация с валидными данными
@pytest.mark.positive
def test_positive_registration(browser, base_url, wait, faker_data):
    browser.get(f"{base_url}/sign_up")

    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    email_field.send_keys(faker_data["email"])
    browser.find_element(By.ID, "pass1").send_keys(faker_data["password"])
    browser.find_element(By.ID, "pass2").send_keys(faker_data["password"])
    browser.find_element(By.ID, "name").send_keys(faker_data["name"])
    browser.find_element(By.CSS_SELECTOR, ".ui.button.blue").click()
    wait.until(EC.url_to_be(f"{base_url}/login"))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".Toastify")))

    alert = browser.find_element(By.CSS_SELECTOR, ".Toastify")
    assert alert.get_attribute("textContent") == "Вы успешно зарегистрировались"


# Регистрация с пробелом в начале email
@pytest.mark.negative
@pytest.mark.parametrize("email, name, password", [
    (" test2@email.ru", "User25", "qwertyu123")
])
def test_registration_mail_with_space(browser, base_url, wait, email, name, password):
    browser.get(f"{base_url}/sign_up")
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    email_field.send_keys(email)
    browser.find_element(By.ID, "pass1").send_keys(password)
    browser.find_element(By.ID, "pass2").send_keys(password)
    browser.find_element(By.ID, "name").send_keys(name)

    browser.find_element(By.CSS_SELECTOR, ".ui.button.blue").click()

    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mt-2")))
    assert alert.get_attribute("textContent") == "Укажите корректный mail"


# Регистрация с незаполненным полем email
@pytest.mark.negative
def test_registration_without_email(browser, base_url, wait, faker_data):
    browser.get(f"{base_url}/sign_up")
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    email_field.send_keys("")
    browser.find_element(By.ID, "pass1").send_keys(faker_data["password"])
    browser.find_element(By.ID, "pass2").send_keys(faker_data["password"])
    browser.find_element(By.ID, "name").send_keys(faker_data["name"])

    browser.find_element(By.CSS_SELECTOR, ".ui.button.blue").click()

    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mt-2")))
    assert alert.get_attribute("textContent") == "Это поле обязательно"


# Регистрация с пустым полем подтверждения пароля
@pytest.mark.negative
def test_registration_without_pass2(browser, base_url, wait, faker_data):
    browser.get(f"{base_url}/sign_up")
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    email_field.send_keys(faker_data["email"])
    browser.find_element(By.ID, "pass1").send_keys(faker_data["password"])
    browser.find_element(By.ID, "pass2").send_keys("")
    browser.find_element(By.ID, "name").send_keys(faker_data["name"])

    browser.find_element(By.CSS_SELECTOR, ".ui.button.blue").click()

    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mt-2")))
    assert alert.get_attribute("textContent") == "Это поле обязательно"






















# @pytest.fixture(params=[
#    {"email": "test2@email.ru",
#     "name": "User25",
#     "password": "qwerty123"},
#    {"email": "test23@email.ru",
#     "name": "User252",
#     "password": "qwerty1213"},
#    {"email": "test2523@email.ru",
#     "name": "User253",
#     "password": "qwerty1234"}
# ])