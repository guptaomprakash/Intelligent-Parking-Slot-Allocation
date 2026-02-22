import streamlit as st
import numpy as np
import random

# =========================
# PAGE SETTINGS
# =========================
st.set_page_config(layout="wide")
st.title("🚗 Smart Multi-Floor Parking System")

# =========================
# PARKING STRUCTURE
# =========================
parking = {
    "Ground Floor (Bike)": {"type": "Bike", "slots": 20},
    "Floor 1 (Car)": {"type": "Car", "slots": 10},
    "Floor 2 (Car)": {"type": "Car", "slots": 10},
    "Floor 3 (Car)": {"type": "Car", "slots": 10},
    "Floor 4 (Mini Truck)": {"type": "Mini Truck", "slots": 10}
}

gates = ["Gate 1", "Gate 2", "Gate 3", "Gate 4"]

# =========================
# SAFE SESSION STATE INIT
# =========================
if "occupancy" not in st.session_state:
    st.session_state["occupancy"] = {}

for floor, data in parking.items():
    if floor not in st.session_state["occupancy"]:
        st.session_state["occupancy"][floor] = np.random.randint(
            0, 2, data["slots"]
        ).tolist()

# =========================
# INPUT SECTION
# =========================
st.subheader("🚘 Vehicle Entry")

vehicle = st.selectbox(
    "Select Vehicle Type",
    ["Bike", "Car", "Mini Truck"]
)

# =========================
# FIND SLOT FUNCTION
# =========================
def find_slot(vehicle_type):

    possible_floors = []

    for floor, data in parking.items():
        if data["type"] == vehicle_type:
            possible_floors.append(floor)

    for floor in possible_floors:

        slots = st.session_state["occupancy"].get(floor, [])

        for i, s in enumerate(slots):
            if s == 0:
                gate = random.choice(gates)
                available = slots.count(0)
                return floor, i + 1, gate, available

    return None, None, None, 0

# =========================
# PARK VEHICLE BUTTON
# =========================
if st.button("🔍 Find Parking Slot"):

    floor, slot, gate, available = find_slot(vehicle)

    if floor is None:
        st.error("❌ No Slot Available for this vehicle type")

    else:
        st.success("✔ Parking Found!")

        c1, c2, c3 = st.columns(3)
        c1.metric("🏢 Floor", floor)
        c2.metric("🅿 Slot Number", slot)
        c3.metric("🚪 Enter From", gate)

        st.info(f"Available Slots on this floor: {available}")

        # Mark slot occupied
        st.session_state["occupancy"][floor][slot - 1] = 1

# =========================
# PNG PARKING VIEW
# =========================
st.subheader("🅿 Live Parking View")

for floor, data in parking.items():

    st.markdown(f"### {floor}")

    slots = st.session_state["occupancy"].get(floor, [])

    cols = st.columns(len(slots))

    for i, slot in enumerate(slots):

        # EMPTY SLOT
        if slot == 0:
            cols[i].image("empty.png", width=60)

        # OCCUPIED SLOT
        else:
            if data["type"] == "Bike":
                cols[i].image("bike.png", width=60)

            elif data["type"] == "Car":
                cols[i].image("car.png", width=60)

            elif data["type"] == "Mini Truck":
                cols[i].image("truck.png", width=60)

    free = slots.count(0)
    st.write(f"Available Slots: **{free}**")
