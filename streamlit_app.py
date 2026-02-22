import streamlit as st
import numpy as np
import random
import time

st.set_page_config(layout="wide")
st.title("🚗 Ultra Realistic Smart Parking Simulation")

# =====================================
# PARKING CONFIG
# =====================================
parking = {
    "Ground": {"type":"Bike","slots":20},
    "Floor1": {"type":"Car","slots":10},
    "Floor2": {"type":"Car","slots":10},
    "Floor3": {"type":"Car","slots":10},
    "Floor4": {"type":"Mini Truck","slots":10}
}

gates = ["Gate 1","Gate 2","Gate 3","Gate 4"]

# =====================================
# SESSION STATE
# =====================================
if "occupancy" not in st.session_state:
    st.session_state.occupancy = {}
    for f,d in parking.items():
        st.session_state.occupancy[f] = [0]*d["slots"]

# =====================================
# INPUT
# =====================================
vehicle = st.selectbox(
    "Select Vehicle Type",
    ["Bike","Car","Mini Truck"]
)

# =====================================
# VEHICLE ICON
# =====================================
def vehicle_icon(v):
    if v=="Bike":
        return "bike.png"
    elif v=="Car":
        return "car.png"
    return "truck.png"

# =====================================
# FIND SLOT + NEAREST GATE
# =====================================
def find_slot(vehicle):

    for floor,data in parking.items():
        if data["type"] == vehicle:

            slots = st.session_state.occupancy[floor]

            for i,s in enumerate(slots):
                if s == 0:

                    # simulate nearest gate logic
                    gate = gates[i % 4]
                    return floor,i,gate

    return None,None,None

# =====================================
# ANIMATION ENGINE
# =====================================
def animate_movement(vehicle,floor,slot,gate):

    icon = vehicle_icon(vehicle)
    frame = st.empty()

    for step in range(8):

        with frame.container():

            st.markdown(f"### 🚦 {vehicle} moving from {gate} → {floor} → Slot {slot+1}")

            cols = st.columns(8)

            for i in range(8):
                if i == step:
                    cols[i].image(icon,width=60)
                else:
                    cols[i].markdown("⬜")

        time.sleep(0.4)

    frame.empty()

# =====================================
# PARK BUTTON
# =====================================
if st.button("🚗 Start Simulation"):

    floor,slot,gate = find_slot(vehicle)

    if floor is None:
        st.error("❌ No slot available")
    else:

        st.success(f"AI Selected → {floor} | Slot {slot+1} | {gate}")

        animate_movement(vehicle,floor,slot,gate)

        st.session_state.occupancy[floor][slot]=1

        st.success("🎉 Vehicle Parked Successfully!")

# =====================================
# LIVE PARKING VISUAL
# =====================================
st.subheader("🅿 Live Parking Layout")

for floor,data in parking.items():

    st.markdown(f"### {floor}")

    slots = st.session_state.occupancy[floor]
    cols = st.columns(len(slots))

    for i,s in enumerate(slots):

        if s==0:
            cols[i].success(f"S{i+1}")
        else:
            cols[i].image(vehicle_icon(data["type"]),width=45)
