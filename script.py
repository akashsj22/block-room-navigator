building = {
    1: [101, 102, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 115, 116, 119, 120, 121, 122, 123,
        124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142,
        143, 144, 145, 146, 147, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 163, 164, 165, 168, 169, 170,
        171, 172, 176]}

print("🏢 Welcome to the PRP Navigation System\n")

while True:
    print("----- FLOOR MENU -----")
    for floor in building:
        print(f"{floor}. Floor {floor}")
    print("0. Exit")

    floor_choice = int(input("\nEnter floor number: "))

    if floor_choice == 0:
        print("Exiting... Goodbye!")
        break

    if floor_choice not in building:
        print("Invalid floor! Try again.\n")
        continue

    room_choice = int(input("Enter room number: "))

    if room_choice in building[floor_choice]:
        print(f"\n Landing Page: You have selected {room_choice} on Floor {floor_choice}.\n")
    else:
        print("\nIn valid room selection in  this floor. Try again.\n")
