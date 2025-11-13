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


def render_number_line(candidate_values, candidates, target_value, target, x_min, x_max, title):
    """Render a number line visualization between x_min and x_max."""
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.hlines(0, x_min, x_max)

    ax.scatter(candidate_values, [0] * len(candidate_values))
    for val, frac in zip(candidate_values, candidates):
        ax.text(val, 0.02, str(frac), ha='center', rotation=45)

    ax.scatter([target_value], [0], color='red', s=80)
    ax.text(target_value, -0.03, str(target) + " (target)", color='red', ha='center', rotation=45)

    ax.set_xlim(x_min, x_max)
    ax.set_yticks([])
    ax.set_xlabel("Number Line")
    ax.set_title(title)
    return fig

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

        # === Report Closest ===
        st.markdown(f"### ✅ Closest estimate: **{closest_label}**")
        st.write(f"Distance: `{distances[closest_idx]:.6f}`")


        # === Plot ===
        padding = 0.05
        min_val = min(candidate_values + [target_value]) - padding
        max_val = max(candidate_values + [target_value]) + padding

        default_fixed_width = 1.0
        data_span = max_val - min_val
        view_width = max(default_fixed_width, data_span)
        center = (min_val + max_val) / 2
        fixed_min = center - view_width / 2
        fixed_max = center + view_width / 2

        fixed_fig = render_number_line(
            candidate_values,
            candidates,
            target_value,
            target,
            fixed_min,
            fixed_max,
            "Fixed-width view",
        )
        st.pyplot(fixed_fig)

        dynamic_fig = render_number_line(
            candidate_values,
            candidates,
            target_value,
            target,
            min_val,
            max_val,
            "Auto-fit view",
        )
        st.pyplot(dynamic_fig)

     