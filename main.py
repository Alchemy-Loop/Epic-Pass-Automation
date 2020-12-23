from scripts.reservation import pass_reservation

complete = 0
max_retries = 3
while not complete and max_retries:
    try:
        pass_reservation = pass_reservation()
        if pass_reservation:
            print("successfully reserved passes")
        complete = 1
    except Exception as e:
        print("Exception so Retrying...")
        max_retries -= 1