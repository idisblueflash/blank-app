import streamlit as st
from fractions import Fraction
import matplotlib.pyplot as plt

st.title("Fraction Distance Visualizer")
st.write("Use this to compare your estimation against the target value.")

# === Input Fields ===
target_input = st.text_input("Target fraction", "2/5")
candidate_input = st.text_input("Candidate fractions (comma separated)", "1/3, 3/8, 1/4")

# Convert strings to Fractions safely
def parse_fraction(s):
    try:
        return Fraction(s.strip())
    except:
        return None

target = parse_fraction(target_input)
candidates = [parse_fraction(x) for x in candidate_input.split(",")]
candidates = [c for c in candidates if c is not None]

if target is None:
    st.error("Invalid target fraction. Example: `2/5`")
else:
    if not candidates:
        st.error("No valid candidate fractions detected.")
    else:
        # Convert to floats
        target_value = float(target)
        candidate_values = [float(c) for c in candidates]

        # Compute distances
        distances = [abs(cv - target_value) for cv in candidate_values]
        closest_idx = distances.index(min(distances))
        closest_label = str(candidates[closest_idx])

        # === Plot ===
        fig, ax = plt.subplots(figsize=(8, 2))

        # Plot number line
        min_val = min(candidate_values + [target_value]) - 0.05
        max_val = max(candidate_values + [target_value]) + 0.05
        ax.hlines(0, min_val, max_val)

        # Plot candidates
        ax.scatter(candidate_values, [0]*len(candidate_values))
        for val, frac in zip(candidate_values, candidates):
            ax.text(val, 0.02, str(frac), ha='center', rotation=45)

        # Plot target (in red)
        ax.scatter([target_value], [0], color='red', s=80)
        ax.text(target_value, -0.03, str(target) + " (target)", color='red', ha='center', rotation=45)

        ax.set_yticks([])
        ax.set_xlabel("Number Line")

        st.pyplot(fig)

        # === Report Closest ===
        st.markdown(f"### ✅ Closest estimate: **{closest_label}**")
        st.write(f"Distance: `{distances[closest_idx]:.6f}`")

        # Show sorted comparison (optional helpful table)
        data = sorted(
            zip(candidates, candidate_values, distances),
            key=lambda x: x[2]
        )
        st.write("Detailed comparison:", data)