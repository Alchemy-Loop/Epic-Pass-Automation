from selenium import webdriver
from time import sleep
from datetime import datetime
from pytz import timezone
from calendar import monthrange
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import config, os
from utils.utils import time_this

DELAY = 10


def get_non_reserved_dates():
    """
    Here first we will take all the dates objects of the current month,
    expired dates objects(for past dates),
    disabled dates objects(for the dates which are already booked).
    Then we filter out only future available dates objects with set operation.

    :return: List of non reserved dates object
    """
    wait_for_page_load("passholder_reservations__calendar__day", "class")

    date_all = driver.find_elements_by_class_name(
        "passholder_reservations__calendar__day"
    )
    sleep(1)
    date_dis = driver.find_elements_by_class_name(
        "passholder_reservations__calendar__day--disabled"
    )
    sleep(1)
    date_exp = driver.find_elements_by_class_name(
        "passholder_reservations__calendar__day--expired"
    )
    non_reserved_dates = set(date_all) - set(date_dis) - set(date_exp)
    non_reserved_dates = list(non_reserved_dates)
    print(len(non_reserved_dates))
    non_reserved_dates = sort_non_reserved_dates(non_reserved_dates)
    return non_reserved_dates


def open_web_link(web_link, browser=False):
    """
    This function open link passed in argument.
    :param web_link: The link the driver will fetch
    :param browser: To run headless or with browser
    :return: This function will return driver object for further use
    """
    global driver
    prefs = {"profile.managed_default_content_settings.images": 2}
    option = Options()
    # option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    option.add_experimental_option("prefs", prefs)

    # option.add_argument("window-size=1200x600")
    if browser:
        # This will open browser.
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    else:
        # If we want to hide browser then need to add option object with --headless in below argument.
        option.add_argument("--headless")
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--example-flag")
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=option
        )
    driver.get(web_link)
    return driver


def login_to_portal(user_id, password):
    """
    This function is for user's login functionality.
    First enter email_id/User id
    Enter Password
    Enter
    :return:
    """
    status = None
    for _ in range(3):
        status = wait_for_page_load("txtUserName_3", "id", 100)
        if status:
            break
    # print("status :- " + str(status))
    sleep(1)

    # close_cookies = driver.find_element_by_xpath('//*[@id="onetrust-close-btn-container"]/button')

    print("Web page opened")
    username_box = driver.find_element_by_id("txtUserName_3")
    username_box.send_keys(user_id)
    print("Email Id entered")

    password_box = driver.find_element_by_id("txtPassword_3")
    password_box.send_keys(password)
    print("Password entered")

    password_box.send_keys(Keys.RETURN)
    print("signed in")


def get_resort_availability_calendar(resort_name):
    """
    This function will open calendar of current month for resort passed in argument.
    :param resort_name:
    :return:
    """
    wait_for_page_load(
        '//*[@id="PassHolderReservationComponent_Resort_Selection"]/option['
        + str(config.RESORT_ID_DICT[resort_name])
        + "]",
        "xpath",
    )
    # sleep(5)
    try:
        close_cookies = driver.find_element_by_class_name("onetrust-close-btn-handler")
        driver.execute_script("arguments[0].click();", close_cookies)
    except Exception as e:
        print("Exception in closing privacy settings", e)
    resort = driver.find_element_by_xpath(
        '//*[@id="PassHolderReservationComponent_Resort_Selection"]/option['
        + str(config.RESORT_ID_DICT[resort_name])
        + "]"
    )
    resort.click()

    print("Resort " + str(resort_name) + " selected")

    # Here we will click check availability button.
    check_avail = driver.find_element_by_xpath(
        '//*[@id="passHolderReservationsSearchButton"]'
    )
    check_avail.click()


def change_calendar_month(term):
    """

    :return:
    """
    if term == "next":
        nxt = driver.find_element_by_class_name(
            "passholder_reservations__calendar__arrow--right"
        )
        nxt.click()
    elif term == "previous":
        nxt = driver.find_element_by_class_name(
            "passholder_reservations__calendar__arrow--left"
        )
        nxt.click()


def get_next_n_days_for_current_month(non_reserved_dates, no_of_days):
    """
    This function will return next no_of_days days from current days with defined timezone.
    :return:
    """
    # Get timezone object of defined timezone.
    timezn = timezone(config.TIMEZONE)
    current_datetime = str(datetime.now(timezn))
    full_date = current_datetime.split(" ")[0]
    year, month, current_date = full_date.split("-")
    _, total_days = monthrange(int(year), int(month))
    # from getting total days of the month we will find next n days.
    day = int(current_date.split("-")[-1])
    next_days_from_today = [day + i for i in range(no_of_days) if day + i <= total_days]
    # driver.find_element_by_xpath('//@id')

    # This condition is to tackle up month change condition.
    # TODO: Need to test the code and can change implementation .
    # if len(next_days_from_today) < no_of_days:
    #     change_calendar_month('next')
    #     sleep(5)
    #     non_reserved_dates += get_non_reserved_dates()  # TODO: Error in this
    #     for i in range(1, config.NEXT_NO_OF_DAYS + 1 - len(next_days_from_today)):
    #         next_days_from_today.append(i)
    #     change_calendar_month('previous')
    return next_days_from_today


def book_for_the_date(date_obj, date):
    """
    This function will return status of booked or not for a given particular date.


    :return:
    """

    # Click on that date in calander.
    driver.execute_script("arguments[0].click();", date_obj)

    wait_for_page_load(
        "passholder_reservations__assign_passholder_modal__name", "class"
    )
    sleep(1)

    print("date " + str(date) + " clicked")
    # Fetch all persons class
    person_selector = driver.find_elements_by_class_name(
        "passholder_reservations__assign_passholder_modal__name"
    )

    unselectable_persons = driver.find_elements_by_class_name(
        "passholder_reservations__assign_passholder_modal__unselectable"
    )
    unselectable_persons_list = []
    for person in unselectable_persons:
        unselectable_persons_list.append(person.text.split("\n")[0])

    # For each person do the selection mentioned in person_list.
    for person in person_selector:
        if person.text in config.PERSONS_LIST:
            if person.text in unselectable_persons_list:
                close = driver.find_element_by_xpath(
                    '//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[2]/div[1]/div[1]/button'
                )
                driver.execute_script("arguments[0].click();", close)
                print("person not clickable closing...")
                return False
            driver.execute_script("arguments[0].click();", person)
            # person.click()
            sleep(0.5)
            print("Person " + str(person.text) + " selected")

    try:
        # After selecting all persons, click on submit button.
        x = driver.find_element_by_xpath(
            '//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[2]/div[1]/div[2]/div/div[3]/button[2]'
        )
        driver.execute_script("arguments[0].click();", x)

        # If there is already done then close the pop up else return True where it can't find Error element.
        wait_for_page_load(
            '//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[2]/div[1]/div[2]/div/ul/li[3]/span/label/h4/i',
            "xpath",
            delay=2,
        )
        driver.find_element_by_xpath(
            '//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[2]/div[1]/div[2]/div/ul/li[3]/span/label/h4/i'
        )
    except Exception as e:
        print("Available on " + str(date_obj.text))
        print("Assigned pass for this date")
        return True
    close = driver.find_element_by_xpath(
        '//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[2]/div[1]/div[1]/button'
    )
    driver.execute_script("arguments[0].click();", close)
    print("Not eligible for pass closing...")
    return False


def wait_for_page_load(element_to_check, parameter, delay=DELAY):
    """

    :param element_to_check:
    :param parameter:
    :return:
    """
    try:

        element_present = None
        if parameter == "xpath":
            element_present = EC.presence_of_element_located(
                (By.XPATH, element_to_check)
            )
        elif parameter == "id":
            element_present = EC.presence_of_element_located((By.ID, element_to_check))
        elif parameter == "class":
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, element_to_check)
            )
        WebDriverWait(driver, delay).until(element_present)
    except TimeoutException as e:
        print("Internet Delay")
        return False


def sort_non_reserved_dates(non_reserved_dates):
    date_list = []
    non_reserved_dates_sorted = []
    for i in non_reserved_dates:
        date_list.append((i, int(i.text)))

    date_list = sorted(date_list, key=lambda x: x[1])
    for obj in date_list:
        non_reserved_dates_sorted.append(obj[0])
    return non_reserved_dates_sorted


@time_this()
def main():
    """
    ------------------------------------------------------
    Starting Of Code.
    -------------------------------------------------------
    This is the outer function to run our functionality.
    :return:
    """

    # Take Credentials of users from config document
    user = config.EMAIL_ID
    password = config.PASSWORD

    driver = open_web_link(web_link=config.WEB_LINK, browser=True)

    login_to_portal(user_id=user, password=password)

    # For Each mountain resort we will book pass for given days.
    resort = config.RESORT
    get_resort_availability_calendar(resort_name=resort)
    print("Calendar Opened")

    non_reserved_dates = get_non_reserved_dates()

    next_days_from_today = get_next_n_days_for_current_month(
        non_reserved_dates, config.NEXT_NO_OF_DAYS
    )

    # sort_non_reserved_dates(non_reserved_dates)

    booked_days = []
    print(non_reserved_dates)
    next_month_flag = True
    count = 0
    while next_month_flag:
        count += 1
        for i in non_reserved_dates:
            try:
                print(i.text)
                cal_date = int(i.text)
            except Exception as e:
                print("Exception in fetching text:",e)
                continue
            if cal_date in next_days_from_today:
                status = book_for_the_date(i, cal_date)
                if status:
                    # save the booked days
                    # TODO : Implement proper DS to store info.
                    booked_days.append(cal_date)
            elif cal_date > max(next_days_from_today):
                break
        if len(next_days_from_today) < config.NEXT_NO_OF_DAYS and count <= 2:
            change_calendar_month("next")
            print("Changing the next month")
            non_reserved_dates = get_non_reserved_dates()
            current_len = len(next_days_from_today)
            next_days_from_today = []
            for i in range(1, config.NEXT_NO_OF_DAYS + 1 - current_len):
                next_days_from_today.append(i)
        else:
            next_month_flag = False

    try:
        wait_for_page_load(
            '//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[6]/div[2]/div[2]/div[2]',
            "xpath",
            delay=2,
        )

        # This will tick the terms & conditions button.
        tnc = driver.find_element_by_xpath(
            '//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[6]/div[2]/div[2]/div[2]'
        )
        # sleep(10)
        driver.execute_script("arguments[0].click();", tnc)
        tnc.click()
        print("checked the terms and condition button")
        # This sleep is temporary
        # TODO : Remove this sleep call.
        # sleep(15)

        # This code will click complete button.
        # TODO : Test this.
        """
        complete = driver.find_element_by_xpath('//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[6]/div[3]/button')
        driver.execute_script("arguments[0].click();", complete)
        """
    except Exception as e:
        print(e)
        print("All days are already reserved")
    driver.close()
    driver.quit()


main()
