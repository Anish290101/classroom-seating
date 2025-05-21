import datetime

def get_initial_seating():
    """
    Returns the initial seating arrangement for the classroom.
    Each row is a list of seats. Each seat is a tuple,
    e.g., ("Student A", "Student B") for a pair, or ("Student C", None) for a single.
    """
    return [
        [  # Row 1
            ("Riddhima", "Samishtha"),  # Seat 1
            ("Yashika", "Harshi"),      # Seat 2
            ("Aditri", "Nitika"),       # Seat 3
            ("Tanushka", "Nivedita"),   # Seat 4
            ("Anaisha", "Ishani"),      # Seat 5
            ("Avika", "Ayesha"),        # Seat 6
        ],
        [  # Row 2
            ("Aadya", "Anushree"),      # Seat 1
            ("Yashasvi", "Tanishee"),   # Seat 2
            ("Sanskriti", "Samriddhi"), # Seat 3
            ("Vedant", "Saad"),         # Seat 4
            ("Abhiraj", "Vipul"),       # Seat 5
            ("Shaurya", "Siddhart"),    # Seat 6
        ],
        [  # Row 3
            ("Dev", None),              # Seat 1 (single student)
            ("Avyukta", "Raunak"),      # Seat 2
            ("Raghav", "Anish"),        # Seat 3
            ("Satvik", "Hemansh"),      # Seat 4
            ("Atharva", "Kunal"),       # Seat 5
            ("Himank", "Naitik"),       # Seat 6
        ],
        [  # Row 4
            ("Aryaman", None),          # Seat 1 (single student)
            ("Hammad", None),           # Seat 2 (single student)
            ("Affan", None),            # Seat 3 (single student)
            ("Aadhyan", "Aarav"),       # Seat 4
            ("Svakksh", "Tanay"),       # Seat 5
            ("Prakhyat", "Kartik"),     # Seat 6
        ],
    ]

def rotate_single_row(row_data, rotation_count):
    """
    Rotates the seats within a single row.
    The rotation is a right-shift (last element moves to front).
    """
    if not row_data:
        return []

    # Calculate effective rotation count to avoid unnecessary full rotations
    effective_rotation = rotation_count % len(row_data)

    # Perform the rotation: last 'effective_rotation' elements moved to the front
    rotated_row = row_data[-effective_rotation:] + row_data[:-effective_rotation]
    return rotated_row

def rotate_seating_row_wise(seating, rotation_count):
    """
    Applies rotation to each row independently.
    Seats only move within their assigned row.
    """
    rotated_full_seating = []
    for row in seating:
        rotated_full_seating.append(rotate_single_row(row, rotation_count))
    return rotated_full_seating

def get_rotation_week_from_date(year, month, day):
    """
    Calculates the 'rotation week' number based on a given date.
    The rotation cycle starts on a fixed 'start_date' (Jan 1, 2024, a Monday),
    and each full 7-day period from this start date increments the rotation week count.
    """
    # Define the fixed start date for your rotation cycle.
    # Jan 1, 2024 was a Monday, making it a good reference for week 0.
    start_date = datetime.date(2024, 1, 1)

    try:
        target_date = datetime.date(year, month, day)
    except ValueError:
        # Invalid date (e.g., Feb 30th)
        return -1

    # Calculate the difference in days from the start date
    delta_days = (target_date - start_date).days

    # Integer division to get the number of full 7-day periods (weeks)
    # This directly gives the rotation count.
    rotation_week = delta_days // 7

    return rotation_week

def valid_month(m):
    """Checks if the month input is between 1 and 12."""
    return 1 <= m <= 12

def valid_day(d, m, y):
    """Checks if the day input is valid for the given month and year."""
    try:
        datetime.date(y, m, d)
        return True
    except ValueError:
        return False

def display_seating(seating):
    """
    Prints the current seating arrangement in a formatted way.
    Adjusts column width dynamically for neat alignment.
    """
    print("\nCurrent Seating Arrangement:\n")

    # Step 1: Find the maximum length of any student's name
    max_name_len = 0
    for row in seating:
        for seat in row:
            for name in seat:
                if name is not None:
                    max_name_len = max(max_name_len, len(name))

    # Step 2: Define a consistent column width for names
    # Add a small buffer for spacing between names/columns.
    # We need enough space for the longest name PLUS ", " if it's a pair.
    name_column_width = max_name_len + 2 # +2 for ", "

    for r_idx, row in enumerate(seating):
        print(f"\t\tRow {r_idx+1}\n")
        for s_idx, seat in enumerate(row):
            # Check if it's a single student seat (either tuple of 1 or 2 with None)
            if len(seat) == 1 or (len(seat) == 2 and seat[1] is None):
                # Format for a single student, using left-alignment and fixed width
                print(f"Seat {s_idx+1}\t{seat[0]:<{name_column_width}}\n")
            else:
                # Format for two students, adding a comma and space between them
                # The first name gets padded, then the second name is printed immediately after.
                print(f"Seat {s_idx+1}\t{seat[0]}, {seat[1]:<{max_name_len}}\n") # Changed here
        print("") # Extra blank line for spacing between rows

def main():
    """
    Main function to run the seating arrangement program.
    Prompts user for a date, calculates rotation, and displays seating.
    """
    initial_seating = get_initial_seating()

    # Get the current year to provide as a default input hint
    current_year = datetime.date.today().year

    print("Class Seating Arrangement - Weekly Rotation (Seats rotate within their row)")
    print(f"Note: The rotation cycle starts relative to Jan 1, 2024 (a Monday).")

    while True:
        try:
            # Get year input, defaulting to current year if empty
            year_input = input(f"Enter year (e.g., {current_year}): ")
            year = int(year_input) if year_input else current_year

            # Get month input
            month = int(input("Enter month number (1-12): "))
            if not valid_month(month):
                print("Invalid month. Please input 1 to 12.")
                continue

            # Get day input
            day = int(input("Enter day of the month (1-31): "))
            if not valid_day(day, month, year):
                print(f"Invalid day {day} for month {month} in year {year}. Please re-enter.")
                continue

        except ValueError:
            print("Invalid input. Please enter numeric values for year, month, and day.")
            continue

        # Calculate the rotation count based on the entered date
        rotation_week_count = get_rotation_week_from_date(year, month, day)

        if rotation_week_count == -1:
            print("Error: Could not calculate rotation week for the given date. "
                  "Please ensure the date is valid (e.g., no Feb 30).")
            continue

        print(f"\nSeating for {month}/{day}/{year} (Rotation Week {rotation_week_count}):")

        # Get the rotated seating arrangement for the calculated week
        rotated_seating = rotate_seating_row_wise(initial_seating, rotation_week_count)

        # Display the rotated seating
        display_seating(rotated_seating)

        # Ask if the user wants to check another date
        cont = input("Check another date? (y/n): ").strip().lower()
        if cont != 'y':
            print("Exiting program. Goodbye!")
            break

if __name__ == "__main__":
    main()