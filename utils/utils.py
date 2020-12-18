import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps
import time


def send_mail(msg=None):
    message = MIMEMultipart()
    email = "#"
    verify_url = "http://verify.example.com"
    message["From"] = "#"
    message["To"] = email
    message["Subject"] = "MEM Correction Verification"
    if not msg:
        msg = """ Need MEM Correction for Yesterday
        """
    message.attach(MIMEText(msg, "plain"))

    # creates SMTP session
    s = smtplib.SMTP("smtp.gmail.com", 587)

    # start TLS for security
    s.starttls()

    # Authentication
    id = "abc@gmail.com"
    password = "12345678"
    s.login(id, password)

    # sending the mail

    s.sendmail(message["From"], email, message.as_string())

    # terminating the session

    s.quit()

    return True


def time_this(logger=None):
    """
    decorator to time any method
    :param logger:
    :return:
    """

    def decorator(function):
        @wraps(function)
        def wrapper_timer(*args, **kwargs):
            start_time = time.time()
            resp = function(*args, **kwargs)
            end_time = time.time()
            if logger:
                logger.info("Time taken to execute: " + str(end_time - start_time))
            else:
                print("Time taken to execute: " + str(end_time - start_time))
            return resp

        return wrapper_timer

    return decorator
