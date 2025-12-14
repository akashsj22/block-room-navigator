building = {
    1: ['101','102','104','105','106','107','108','109','110','111',],
    2: ["Room 201", "Room 202", "Room 203", "Room 204"],
    3: ["Room 301", "Room 302"],
}

print("🏢 Welcome to the Building Navigation System\n")

while True:
    print("----- FLOOR MENU -----")
    for floor in building:
        print(f"{floor}. Floor {floor}")
    print("0. Exit")

    # Ask for floor
    choice = int(input("\nEnter floor number: "))

    if choice == 0:
        print("Exiting... Goodbye!")
        break

    if choice not in building:
        print("❌ Invalid floor! Try again.\n")
        continue

    # Show rooms on that floor
    print(f"\nRooms available on Floor {choice}:")
    for i, room in enumerate(building[choice], start=1):
        print(f"{i}. {room}")

    room_choice = int(input("\nEnter room number: "))

    if 1 <= room_choice <= len(building[choice]):
        selected_room = building[choice][room_choice - 1]
        print(f"\n🛎️ Landing Page: You selected *{selected_room}* on Floor {choice}.\n")
    else:
        print("❌ Invalid room selection! Try again.\n")