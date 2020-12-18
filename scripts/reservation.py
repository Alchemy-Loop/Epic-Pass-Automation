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
import config

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
    s.login("meetsheth2311@gmail.com", "incorret2311")

    # sending the mail

    s.sendmail(messsage['From'], email, messsage.as_string())

    # terminating the session

    s.quit()

    return True

def get_non_reserved_dates():
    """

    :return:
    """
    date_all = driver.find_elements_by_class_name('passholder_reservations__calendar__day')
    date_dis = driver.find_elements_by_class_name('passholder_reservations__calendar__day--disabled')
    date_exp = driver.find_elements_by_class_name('passholder_reservations__calendar__day--expired')
    non_reserved_dates = set(date_all) - set(date_dis) - set(date_exp)
    non_reserved_dates = list(non_reserved_dates)
    return non_reserved_dates

def open_web_link(web_link,browser=False):
    """
    This function open link passed in argument.
    :param web_link:
    :return:
    """
    global driver
    option = Options()
    option.add_argument("--headless")
    # option.add_argument("window-size=1200x600")
    if browser:
        driver = webdriver.Chrome(ChromeDriverManager().install())
    else:
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
    driver.get('https://www.epicpass.com/Plan-Your-Trip/Lift-Access/Reservations?reservation=true')
    print("Opened")
    return driver



def login_to_portal(user_id,password):
    """
    First enter email_id/User id
    Enter Password
    Enter
    :return:
    """
    username_box = driver.find_element_by_id('txtUserName_3')
    username_box.send_keys(user_id)
    print("Email Id entered")

    password_box = driver.find_element_by_id('txtPassword_3')
    password_box.send_keys(password)
    print("Password entered")

    password_box.send_keys(Keys.RETURN)

def get_resort_availability_calendar(resort_name):
    """
    This function will open calendar for resort passed in argument.
    :param resort_name:
    :return:
    """
    m = {1:10}
    park_city = driver.find_element_by_xpath('//*[@id="PassHolderReservationComponent_Resort_Selection"]/option[10]')
    park_city.click()
    sleep(5)

    check_avail = driver.find_element_by_xpath('//*[@id="passHolderReservationsSearchButton"]')
    check_avail.click()

def change_calendar_to_next_month():
    """

    :return:
    """
    nxt = driver.find_element_by_class_name('passholder_reservations__calendar__arrow--right')
    nxt.click()


def get_next_n_days_for_current_month():
    """

    :return:
    """
    timezn = timezone(config.TIMEZONE)
    current_datetime = str(datetime.now(timezn))
    full_date = current_datetime.split(' ')[0]
    year, month, current_date = full_date.split('-')
    _, total_days = monthrange(int(year), int(month))
    next_seven_days_from_today = [int(current_date.split('-')[-1]) + i for i in range(7) if
                                  int(current_date.split('-')[-1]) + i < total_days]

    if len(next_seven_days_from_today) < 7:
        change_calendar_to_next_month()
        sleep(5)
        non_reserved_dates.extend(get_non_reserved_dates())
        for i in range(1, config.NEXT_NO_OF_DAYS + 1 - len(next_seven_days_from_today)):
            next_seven_days_from_today.append(i)
    return next_seven_days_from_today

def book_for_the_date(date):
    """
    This function will return status of booked or not for a given particular date.
    :return:
    """
    driver.execute_script("arguments[0].click();", i)
    sleep(5)
    person_selector = driver.find_elements_by_class_name('passholder_reservations__assign_passholder_modal__name')
    for person in person_selector:
        if person.text in config.PERSONS_LIST:
            person.click()
    x = driver.find_element_by_xpath(
        '//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[2]/div[1]/div[2]/div/div[3]/button[2]')
    driver.execute_script("arguments[0].click();", x)
    try:
        driver.find_element_by_class_name('passholder_reservations__assign_passholder_modal__error')
    except Exception as e:
        print("Available on " + str(i.text))
        return True
    cancel = driver.find_element_by_xpath(
        '//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[2]/div[1]/div[2]/div/div[3]/button[1]')
    driver.execute_script("arguments[0].click();", cancel)
    print(cancel)
    return False
    # except Exception as e:
    #     print("Available on " + str(i.text))
    #     return True


user = config.EMAIL_ID
password = config.PASSWORD

driver = open_web_link(web_link=config.WEB_LINK,browser=True)

sleep(10)

login_to_portal(user_id=user,password=password)

sleep(30)

for resort in config.RESORT_LIST:
    get_resort_availability_calendar(resort_name=resort)

    sleep(10)

    non_reserved_dates = get_non_reserved_dates()

    next_seven_days_from_today = get_next_n_days_for_current_month()

    booked_days = []
    for i in non_reserved_dates:
        cal_date = int(i.text)
        if cal_date in next_seven_days_from_today:
            status = book_for_the_date(cal_date)
            if status:
                booked_days.append(cal_date)
            sleep(8)

    sleep(15)

            # tnc = driver.find_element_by_xpath('//*[@id="passHolderReservations__wrapper"]/div[3]/div[2]/div[6]/div[2]/div[2]/div[2]/label/span/')
            # print(tnc)
            # tnc.click()
            # sleep(5)

# driver.close()
driver.quit()