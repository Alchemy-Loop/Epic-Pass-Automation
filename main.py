from scripts.reservation import pass_reservation

complete = 0
max_retries = 3
while not complete and max_retries:
    pass_reservation = pass_reservation()
    if pass_reservation == "Error":
        max_retries -= 1
    else:
        complete = 1