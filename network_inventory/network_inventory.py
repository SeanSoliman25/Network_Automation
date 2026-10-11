class Device:
    def __init__(self, name, address, model, location, status = False):
        self.name = name
        self.address = address
        self.model = model
        self.location = location
        self.status = status

    def statusReport(self):
        print(f"{self.name}")
        print(f"\tIP Address: {self.address}")
        print(f"\tDevice Type: {self.model}")
        print(f"\tLocation: {self.location}")
        if self.status:
            print("\tStatus: Active")
        else:
            print("\tStatus: Inactive")

entries = [
    ["Router 1", "192.168.10.1", "Catalyst 8000", "Makati City, Manila", True],
    ["Router 2", "192.168.20.1", "Catalyst 8000", "Quezon City, Manila", True],
    ["Router 3", "192.168.30.1", "Catalyst 8000", "Makati, Manila"]
    ]

inventory = []
for entry in entries:
    inventory.append(Device(*entry))

print("Full Inventory\n")
for entry in inventory:
    entry.statusReport()

print("\nAvailable Devices\n")
for entry in inventory:
    if entry.status:
        entry.statusReport()

print(f"\nNumber of Available Devices: {len([x for x in inventory if x.status])}")