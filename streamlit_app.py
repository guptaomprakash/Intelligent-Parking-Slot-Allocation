import streamlit as st
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("🚗 Smart Multi-Floor Parking AI System")

# =========================
# PARKING STRUCTURE
# =========================
parking = {
    "Ground (Bike)": {"type":"Bike", "slots":20},
    "Floor 1 (Car)": {"type":"Car", "slots":10},
    "Floor 2 (Car)": {"type":"Car", "slots":10},
    "Floor 3 (Car)": {"type":"Car", "slots":10},
    "Floor 4 (MiniTruck)": {"type":"Mini Truck", "slots":10}
}

gates = ["Gate 1","Gate 2","Gate 3","Gate 4"]

# =========================
# SESSION STATE
# =========================
if "occupancy" not in st.session_state:
    st.session_state.occupancy = {}

    for floor,data in parking.items():
        st.session_state.occupancy[floor] = np.random.randint(
            0,2,data["slots"]
        ).tolist()

# =========================
# INPUT SECTION
# =========================
st.subheader("🚘 Vehicle Entry")

vehicle = st.selectbox(
    "Select Vehicle Type",
    ["Bike","Car","Mini Truck"]
)

# =========================
# FIND AVAILABLE SLOT
# =========================
def find_slot(vehicle):

    possible_floors = []

    for floor,data in parking.items():
        if data["type"] == vehicle:
            possible_floors.append(floor)

    for floor in possible_floors:
        slots = st.session_state.occupancy[floor]
        for i,s in enumerate(slots):
            if s == 0:
                gate = random.choice(gates)
                return floor, i+1, gate, slots.count(0)

    return None,None,None,0

# =========================
# PARK BUTTON
# =========================
if st.button("🔍 Find Parking Slot"):

    floor,slot,gate,available = find_slot(vehicle)

    if floor is None:
        st.error("❌ No Slot Available for this vehicle type")
    else:
        st.success("✔ Parking Found!")

        col1,col2,col3 = st.columns(3)

        col1.metric("🏢 Floor", floor)
        col2.metric("🅿 Slot Number", slot)
        col3.metric("🚪 Enter From", gate)

        st.info(f"Available Slots on this floor: {available}")

        # mark slot occupied
        st.session_state.occupancy[floor][slot-1] = 1

# =========================
# VISUALIZATION
# =========================
st.subheader("📊 Live Parking Occupancy")

for floor,data in parking.items():

    st.markdown(f"### {floor}")

    grid = np.array(st.session_state.occupancy[floor]).reshape(1,-1)

    fig,ax = plt.subplots(figsize=(8,1.5))
    sns.heatmap(grid,cmap="YlGnBu",cbar=False,
                linewidths=1,ax=ax)

    ax.set_xticklabels(range(1,len(grid[0])+1))
    ax.set_yticklabels(["Slots"])
    st.pyplot(fig)

    free = st.session_state.occupancy[floor].count(0)
    st.write(f"Available Slots: **{free}**")
