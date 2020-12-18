from selenium import webdriver
from time import sleep
from datetime import datetime
from pytz import timezone
from calendar import monthrange
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import config
DELAY = 10

def send_mail(msg=None):
    messsage = MIMEMultipart()
    email = 'meets@dosepack.com'
    verify_url = 'http://verify.example.com'
    messsage['From'] = 'meetsheth2311@gmail.com'
    messsage['To'] = email
    messsage['Subject'] = 'MEM Correction Verification'
    if not msg:
        msg = """ Need MEM Correction for Yesterday
        """
    messsage.attach(MIMEText(msg, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    id = "abc@gmail.com"
    password = "12345678"
    s.login(id, password)

    # sending the mail

    s.sendmail(messsage['From'], email, messsage.as_string())

    # terminating the session

    s.quit()

    return True

def get_non_reserved_dates():
    """
    Here first we will take all the dates objects of the current month,
    expired dates objects(for past dates),
    disabled dates objects(for the dates which are already booked).
    Then we filter out only future available dates objects with set operation.

    :return: List of non reserved dates object
    """
    wait_for_page_load('passholder_reservations__calendar__day','class')

    date_all = driver.find_elements_by_class_name('passholder_reservations__calendar__day')
    date_dis = driver.find_elements_by_class_name('passholder_reservations__calendar__day--disabled')
    date_exp = driver.find_elements_by_class_name('passholder_reservations__calendar__day--expired')
    non_reserved_dates = set(date_all) - set(date_dis) - set(date_exp)
    non_reserved_dates = list(non_reserved_dates)
    print(non_reserved_dates)
    return non_reserved_dates

def open_web_link(web_link,browser=False):
    """
    This function open link passed in argument.
    :param web_link:
    :return: This function will return driver object for further use
    """
    global driver
    option = Options()
    option.add_argument("--headless")
    # option.add_argument("window-size=1200x600")
    if browser:
        # This will open browser.
        driver = webdriver.Chrome(ChromeDriverManager().install())
    else:
        # If we want to hide browser then need to add option object with --headless in below argument.
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
    driver.get(web_link)
    return driver



def login_to_portal(user_id,password):
    """
    This function is for user's login functionality.
    First enter email_id/User id
    Enter Password
    Enter
    :return:
    """
    wait_for_page_load('txtUserName_3','id',15)

    username_box = driver.find_element_by_id('txtUserName_3')
    username_box.send_keys(user_id)
    print("Email Id entered")

    password_box = driver.find_element_by_id('txtPassword_3')
    password_box.send_keys(password)
    print("Password entered")

    password_box.send_keys(Keys.RETURN)
    delay = 10
    element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="PassHolderReservationComponent_Resort_Selection"]/option[10]'))
    WebDriverWait(driver, delay).until(element_present)

def get_resort_availability_calendar(resort_name):
    """
    This function will open calendar of current month for resort passed in argument.
    :param resort_name:
    :return:
    """
    wait_for_page_load('//*[@id="PassHolderReservationComponent_Resort_Selection"]', 'xpath')
    # TODO : Need to fetch resort name and id from config file.
    # Here option[10] if for heavenly resort. Need to make it parameterized.
    park_city = driver.find_element_by_xpath('//*[@id="PassHolderReservationComponent_Resort_Selection"]/option[10]')
    park_city.click()

    # Here we will click check availability button.
    check_avail = driver.find_element_by_xpath('//*[@id="passHolderReservationsSearchButton"]')
    check_avail.click()

def change_calendar_to_next_month():
    """

    :return:
    """
    nxt = driver.find_element_by_class_name('passholder_reservations__calendar__arrow--right')
    nxt.click()


def get_next_n_days_for_current_month(no_of_days):
    """
    This function will return next no_of_days days from current days with defined timezone.
    :return:
    """
    # Get timezone object of defined timezone.
    timezn = timezone(config.TIMEZONE)
    current_datetime = str(datetime.now(timezn))
    full_date = current_datetime.split(' ')[0]
    year, month, current_date = full_date.split('-')
    _, total_days = monthrange(int(year), int(month))
    # from getting total days of the month we will find next n days.
    next_days_from_today = [int(current_date.split('-')[-1]) + i for i in range(no_of_days) if
                                  int(current_date.split('-')[-1]) + i < total_days]

    # This condition is to tackle up month change condition.
    # TODO: Need to test the code and can change implementation .
    if len(next_days_from_today) < no_of_days:
        change_calendar_to_next_month()
        sleep(5)
        non_reserved_dates.extend(get_non_reserved_dates())
        for i in range(1, config.NEXT_NO_OF_DAYS + 1 - len(next_days_from_today)):
            next_days_from_today.append(i)
    return next_days_from_today

def book_for_the_date(date_obj,date):
    """
    This function will return status of booked or not for a given particular date.


    :return:
    """

    # Click on that date in calander.
    driver.execute_script("arguments[0].click();", date_obj)

    wait_for_page_load('passholder_reservations__assign_passholder_modal__name','class')
    # sleep(5)
    # Fetch all persons class
    person_selector = driver.find_elements_by_class_name('passholder_reservations__assign_passholder_modal__name')

    # For each person do the selection mentioned in person_list.
    for person in person_selector:
        if person.text in config.PERSONS_LIST:
            person.click()

    # After selecting all persons, click on submit button.
    x = driver.find_element_by_xpath(
        '//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[2]/div[1]/div[2]/div/div[3]/button[2]')
    driver.execute_script("arguments[0].click();", x)
    try:
        # If there is already done then close the pop up else return True where it can't find Error element.
        wait_for_page_load('//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[2]/div[1]/div[2]/div/ul/li[3]/span/label/h4/i','xpath',delay=2)
        driver.find_element_by_xpath('//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[2]/div[1]/div[2]/div/ul/li[3]/span/label/h4/i')
    except Exception as e:
        print("Available on " + str(date_obj.text))
        return True
    close = driver.find_element_by_xpath('//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[2]/div[1]/div[1]/button')
    driver.execute_script("arguments[0].click();", close)
    return False

def wait_for_page_load(element_to_check,parameter,delay=DELAY):
    """

    :param element_to_check:
    :param parameter:
    :return:
    """
    try:

        element_present = None
        if parameter == 'xpath':
            element_present = EC.presence_of_element_located(
                (By.XPATH, element_to_check))
        elif parameter == 'id':
            element_present = EC.presence_of_element_located(
                (By.ID, element_to_check))
        elif parameter == 'class':
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, element_to_check))
        WebDriverWait(driver, delay).until(element_present)
    except TimeoutException as e:
        print("Internet Delay")




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


    driver = open_web_link(web_link=config.WEB_LINK,browser=True)

    # sleep(10)

    login_to_portal(user_id=user,password=password)

    # sleep(10)

    # For Each mountain resort we will book pass for given days.
    for resort in config.RESORT_LIST:
        get_resort_availability_calendar(resort_name=resort)

        non_reserved_dates = get_non_reserved_dates()

        next_days_from_today = get_next_n_days_for_current_month(config.NEXT_NO_OF_DAYS)

        booked_days = []
        print(non_reserved_dates)
        for i in non_reserved_dates:
            cal_date = int(i.text)
            if cal_date in next_days_from_today:
                status = book_for_the_date(i,cal_date)
                if status:
                    # save the booked days
                    # TODO : Implement proper DS to store info.
                    booked_days.append(cal_date)

        try:
            wait_for_page_load('//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[6]/div[2]/div[2]/div[2]','xpath',delay=2)

            # This will tick the terms & conditions button.
            tnc = driver.find_element_by_xpath('//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[6]/div[2]/div[2]/div[2]')
            driver.execute_script("arguments[0].click();", tnc)
            tnc.click()
            # This sleep is temporary
            # TODO : Remove this sleep call.
            sleep(15)

            # This code will click complete button.
            # TODO : Test this.
            '''
            complete = driver.find_element_by_xpath('//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[6]/div[3]/button')
            driver.execute_script("arguments[0].click();", complete)
            '''
        except Exception as e:
            print("All days are already reserved")
    driver.close()
    driver.quit()


main()