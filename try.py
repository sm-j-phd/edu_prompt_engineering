

import streamlit as st
import urllib.parse
import random
import requests

POLLINATIONS_API_KEY = "pk_UdvJx68ughmUlX5O"

st.set_page_config(
    page_title="The Memory Studio with AI",
    page_icon="🎨",
    layout="centered" 
)

# ---------- Global CSS ----------
st.markdown(
    """
<style>
div[data-baseweb="select"] * { font-size: 1rem !important; }
button[data-testid="stPillsChip"] * { font-size: 1rem !important; }
.pills-label { font-size: 1rem !important; margin-bottom: 5px; }
</style>
""",
    unsafe_allow_html=True,
)



# Clear session state variables
if "prompt_cart" not in st.session_state:
    st.session_state.prompt_cart = []

if "manual_mode" not in st.session_state:
    st.session_state.manual_mode = False

st.title("🎨 The Memory Studio with AI")
st.write("Select options to build your prompt and generate beautiful images!")


st.divider()

def spacer(h=14):
    st.markdown(f"<div style='height:{h}px;'></div>", unsafe_allow_html=True)

# ===== Limit functions =====
def limit_objects():
    if len(st.session_state.objects_key) > 5:
        st.session_state.objects_key = st.session_state.objects_key[:5]
        st.toast("You can only select up to 5 objects! 🛑", icon="⚠️")

def limit_company():
    if len(st.session_state.company_key) > 1:
        st.session_state.company_key = st.session_state.company_key[:3]
        st.toast("You can only select up to 1 companions! 🛑", icon="⚠️")
# ============================================

st.subheader("1️⃣ Build your prompt")

spacer(10)

# toggle
st.session_state.manual_mode = st.toggle("✨ If you'd like to type your own keywords, just click this toggle!", value=st.session_state.manual_mode)

spacer(10)

# 1) Role
c1, c2 = st.columns([0.12, 0.88], gap="small", vertical_alignment="center")
with c1:
    st.markdown("I am")
with c2:
    if not st.session_state.manual_mode:
        subject = st.selectbox(
            "Role",
            ["a painter.", "a cartoonist.", "a photographer."],
            label_visibility="collapsed",
        )
    else:
        subject = st.text_input("Enter your role", "a painter.", label_visibility="collapsed", key="role_manual")

spacer(10)

# 2) Target 
c3, c4 = st.columns([0.65, 0.35], gap="small", vertical_alignment="center")
with c3:
    st.markdown("I'll create an image that weaves the childhood memory of")
with c4:
    if not st.session_state.manual_mode:
        target = st.selectbox(
            "Target",
            ["Dorothy", "Walter", "Alice", "George"],
            label_visibility="collapsed",
        )
    else:
        target = st.text_input("Enter target", "Dorothy", label_visibility="collapsed", key="target_manual")

# 🎯 Pronouns setting
if "Dorothy" in target or "Alice" in target:
    subj, obj, poss = "she", "her", "her"
else:
    subj, obj, poss = "he", "him", "his"

spacer(10)

# 3, 4) Place, Time
c6, c7 = st.columns([0.65, 0.35], gap="small", vertical_alignment="center")
with c6:
    st.markdown(f"Back in {target}'s elementary school, {subj} spent a wonderful time at")
with c7:
    if not st.session_state.manual_mode:
        place = st.selectbox(
            "Place", ["a park", "a playground", "the beach", "home"], label_visibility="collapsed"
        )
    else:
        place = st.text_input("Enter place", "a park", label_visibility="collapsed", key="place_manual")

c8, c9, c10 = st.columns([0.2, 0.4, 0.4], gap="small", vertical_alignment="center")
with c8:
    st.markdown("on a ")
with c9:
    if not st.session_state.manual_mode:
        season = st.selectbox(
            "Season", ["spring", "summer", "fall", "winter"], label_visibility="collapsed"
        )
    else:
        season = st.text_input("Enter season", "spring", label_visibility="collapsed", key="season_manual")
with c10:
    if not st.session_state.manual_mode:
        time = st.selectbox(
            "Time", ["day.", "sunrise.", "sunset.", "night."], label_visibility="collapsed"
        )
    else:
        time = st.text_input("Enter time", "day.", label_visibility="collapsed", key="time_manual")

spacer(12)

# 5) Objects (Max 5)
st.markdown("<div class='pills-label'>In that place, there were something beautiful and nostalgic—(Pick up to 5)</div>", unsafe_allow_html=True)
if not st.session_state.manual_mode:
    objects = st.pills(
        "objects_label",
        [
            "trees", "flowers", "cacti", "butterflies", "fireflies", "the ocean", "a lake", "snowflakes",
            "raindrops", "stars", "fruit", "drinks", "meat", "a campfire", "a table", "the sun", "the moon", "clouds", "a rainbow", "a galaxy"
        ],
        selection_mode="multi",
        default=["trees"],
        key="objects_key",         
        on_change=limit_objects,   
        label_visibility="collapsed",
    )
    objects_str = ", ".join(objects) if objects else ""
else:
    objects_str = st.text_input("Enter objects", "trees, flowers", label_visibility="collapsed", key="objects_manual")

spacer(10)

# 6) Activity 
c11, c12 = st.columns([0.28, 0.72], gap="small", vertical_alignment="center")
with c11:
    st.markdown(f"{subj.capitalize()} had a happy time")
with c12:
    if not st.session_state.manual_mode:
        activity = st.selectbox(
            "Activity",
            [
                "taking a walk", "eating food", "riding a bike", "playing catch", "playing soccer",
                "swimming", "singing", "dancing to music", "cooking", "playing the piano"
            ],
            label_visibility="collapsed",
        )
    else:
        activity = st.text_input("Enter activity", "taking a walk", label_visibility="collapsed", key="activity_manual")

spacer(10)

# 7) Company 
c13, c14 = st.columns([0.28, 0.72], gap="small", vertical_alignment="center")
with c13:
    st.markdown(f"with {poss} loved")           
with c14:
    if not st.session_state.manual_mode:
        company = st.selectbox(
            "Company",
            ["friend.", "family.", "dad.", "mom.", "grandfather.", "grandmother.", "sister.", "brother.", "dog", "cat."],
            label_visibility="collapsed",
        )
    else:
        company = st.text_input("Enter company", "friends", label_visibility="collapsed", key="company_manual")

spacer(10)

# 8) Style
c15, c16 = st.columns([0.5, 0.5], gap="small", vertical_alignment="center")
with c15:
    st.markdown("Create an image that captures this memory in a ")           
with c16:
    if not st.session_state.manual_mode:
        style = st.selectbox(
            "Style",
            ["watercolor style.", "crayon drawing style.", "cartoon style.", "pixel art style.", "photorealistic style."],
            label_visibility="collapsed",
        )
    else:
        style = st.text_input("Enter style", "watercolor style.", label_visibility="collapsed", key="style_manual")

spacer(18)

# 9) format
c17, c18 = st.columns([0.5, 0.5], gap="small", vertical_alignment="center")
with c17:
    st.markdown("The final image must be in a")           
with c18:
    if not st.session_state.manual_mode:
        format = st.selectbox(
            "Format",
            ["framed format with a wooden frame.", "polaroid format with a thin white border.", "film format with a thin black border."],
            label_visibility="collapsed",
        )
    else:
        format = st.text_input("Enter format", "framed format with a wooden frame.", label_visibility="collapsed", key="format_manual")




# ---- Prompt assembly ----
final_prompt_1 = f"I am a {subject}"
final_prompt_2 = f"I'll create an image that expresses the childhood memory of {target}."
final_prompt_3 = f"Back in {target}'s elementary school, {subj} spent a wonderful time at {place} on a {season} {time}"
final_prompt_4 = f"In that place, there were something beautiful and nostalgic—{objects_str}."
final_prompt_5 = f"{subj.capitalize()} had a happy time {activity} with {poss} loved {company}"
final_prompt_6 = f"Create an image that captures this memory in a {style}"
final_prompt_7 = f"The final image must be in a {format}"

spacer(12)

# Add to Cart
if st.button("Add to Prompt Board 📥", use_container_width=True):
    combined_prompt = "\n".join([final_prompt_1, final_prompt_2, final_prompt_3, final_prompt_4, final_prompt_5, final_prompt_6, final_prompt_7])
    st.session_state.prompt_cart.append(combined_prompt)
    st.toast("Prompt added to board", icon="🛒")

st.divider()

st.subheader("2️⃣ Your Prompt Board")

if st.session_state.prompt_cart:
    for idx, p in enumerate(st.session_state.prompt_cart, start=1):
        # st.text(p)
        # st.caption(f"Prompt #{idx}")
        st.code(p, language="text")

    if st.button("Clear Board 🗑️"):
        st.session_state.prompt_cart = []
        st.rerun()
else:
    st.write("Board is empty.")


if "generated_images" not in st.session_state:
    st.session_state.generated_images = []



st.divider()

st.subheader("3️⃣ Create Images")

if st.button("🚀 Generate All Images", type="primary", use_container_width=True, key="gen_all"):
    if not st.session_state.prompt_cart:
        st.error("Please add items to the cart first.")
    else:
        with st.spinner("🎨 Generating..."):
            st.session_state.generated_images = []

            for idx, prompt in enumerate(st.session_state.prompt_cart):
                encoded_prompt = urllib.parse.quote(prompt)
                seed = random.randint(1, 99999)

                image_url = (
                    f"https://gen.pollinations.ai/image/{encoded_prompt}"
                    f"?width=1024&height=1024&seed={seed}&model=flux&key={POLLINATIONS_API_KEY}"
                )

                img_bytes = None
                try:
                    r = requests.get(image_url, timeout=30)
                    r.raise_for_status()
                    img_bytes = r.content
                except Exception:
                    img_bytes = None

                filename = f"memory_{idx+1}.png"

                st.session_state.generated_images.append(
                    {"prompt": prompt, "url": image_url, "bytes": img_bytes, "filename": filename}
                )

        st.success(f"✅ Generated {len(st.session_state.generated_images)} images successfully!")

if st.session_state.generated_images:
    cols = st.columns(3)
    for idx, item in enumerate(st.session_state.generated_images):
        with cols[idx % 3]:
            if item["bytes"]:
                st.image(item["bytes"], caption=f"Prompt #{idx+1}", use_container_width=True)
                st.download_button(
                    label="Download image ⬇️",
                    data=item["bytes"],
                    file_name=item["filename"],
                    mime="image/png",
                    key=f"dl_{idx}",
                    use_container_width=True,
                )
            else:
                st.image(item["url"], caption=f"Prompt #{idx+1}", use_container_width=True)
                st.caption("Download not available (image fetch failed).")

    if st.button("Clear Generated Results 🧹", key="clear_results", use_container_width=True):
        st.session_state.generated_images = []
        st.rerun()



# streamlit run try.py
# # Local URL: http://localhost:8501
# # Network URL: http://169.234.230.92:8501



