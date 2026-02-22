import streamlit as st
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import time

st.set_page_config(layout="wide")
st.title("🚗 Intelligent Parking Slot Allocation")

# =============================
# SIDEBAR SETTINGS
# =============================
st.sidebar.header("⚙ Simulation Settings")

FLOORS = st.sidebar.slider("Floors", 1, 5, 3)
SLOTS_PER_FLOOR = st.sidebar.slider("Slots per Floor", 5, 20, 10)
EPISODES = st.sidebar.slider("Training Episodes", 500, 5000, 2000)
AUTO_SIM = st.sidebar.checkbox("Enable Live Simulation", True)

TOTAL_SLOTS = FLOORS * SLOTS_PER_FLOOR

ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.2

# =============================
# SESSION STATE
# =============================
if "Q_table" not in st.session_state:
    st.session_state.Q_table = np.zeros((2**min(TOTAL_SLOTS,12), TOTAL_SLOTS))

if "rewards_rl" not in st.session_state:
    st.session_state.rewards_rl = []

if "rewards_random" not in st.session_state:
    st.session_state.rewards_random = []

Q_table = st.session_state.Q_table

# =============================
# FUNCTIONS
# =============================
def state_to_index(state):
    state = state[:12]
    return int("".join(map(str,state)),2)

def get_reward(state, action):
    return 10 if state[action]==0 else -10

def choose_action(state_idx):
    if random.random() < EPSILON:
        return random.randint(0, TOTAL_SLOTS-1)
    return np.argmax(Q_table[state_idx])

# =============================
# TRAINING
# =============================
if st.button("🚀 Train AI Agent"):

    st.session_state.rewards_rl.clear()
    st.session_state.rewards_random.clear()

    progress = st.progress(0)

    for ep in range(EPISODES):

        state = np.random.randint(0,2,TOTAL_SLOTS).tolist()
        s_idx = state_to_index(state)

        action = choose_action(s_idx)
        reward = get_reward(state, action)

        next_state = state.copy()
        if next_state[action]==0:
            next_state[action]=1

        n_idx = state_to_index(next_state)

        Q_table[s_idx,action] += ALPHA*(
            reward + GAMMA*np.max(Q_table[n_idx]) - Q_table[s_idx,action]
        )

        st.session_state.rewards_rl.append(reward)

        rand_action = random.randint(0,TOTAL_SLOTS-1)
        st.session_state.rewards_random.append(
            get_reward(state,rand_action)
        )

        progress.progress((ep+1)/EPISODES)

    st.success("Training Completed ✔")

# =============================
# LIVE SIMULATION AREA
# =============================
st.subheader("🚘 Live Smart Parking Simulation")

placeholder = st.empty()

def run_simulation():

    state = np.random.randint(0,2,TOTAL_SLOTS).tolist()
    s_idx = state_to_index(state)

    best_action = np.argmax(Q_table[s_idx])

    grid = np.array(state).reshape(FLOORS,SLOTS_PER_FLOOR)

    with placeholder.container():

        colA,colB = st.columns([2,1])

        with colA:
            fig,ax = plt.subplots(figsize=(10,4))
            sns.heatmap(grid,cmap="YlGnBu",cbar=False,linewidths=1,ax=ax)
            ax.set_title("Parking Occupancy Heatmap")
            st.pyplot(fig)

        with colB:
            floor = best_action // SLOTS_PER_FLOOR
            slot = best_action % SLOTS_PER_FLOOR

            occupied = sum(state)
            free = TOTAL_SLOTS-occupied
            efficiency = (free/TOTAL_SLOTS)*100

            st.metric("🤖 AI Suggested Floor", floor+1)
            st.metric("🚗 Suggested Slot", slot+1)
            st.metric("📊 Efficiency %", f"{efficiency:.1f}")

            if efficiency < 25:
                st.error("⚠ High Congestion Predicted")
            elif efficiency < 50:
                st.warning("⚠ Medium Traffic")
            else:
                st.success("✔ Parking Flow Smooth")

run_simulation()

if AUTO_SIM:
    for _ in range(5):
        time.sleep(1)
        run_simulation()

# =============================
# ANALYTICS
# =============================
st.subheader("📈 AI Performance Dashboard")

if len(st.session_state.rewards_rl)>0:

    df = pd.DataFrame({
        "RL Agent": st.session_state.rewards_rl,
        "Random": st.session_state.rewards_random
    })

    fig2,ax2 = plt.subplots(figsize=(10,4))
    ax2.plot(df["RL Agent"],label="RL Agent")
    ax2.plot(df["Random"],alpha=0.6,label="Random Strategy")
    ax2.legend()
    ax2.set_title("Learning Performance Comparison")
    ax2.set_xlabel("Episodes")
    ax2.set_ylabel("Reward")
    st.pyplot(fig2)

    avg_rl = np.mean(df["RL Agent"])
    avg_rand = np.mean(df["Random"])

    st.subheader("🧠 AI Smart Insights")

    if avg_rl > avg_rand:
        st.success("AI allocation strategy is smarter than random allocation.")
    else:
        st.warning("Increase training episodes for better learning.")
