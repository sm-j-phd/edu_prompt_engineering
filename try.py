import streamlit as st
import urllib.parse
import random

# 1. Page Config
st.set_page_config(page_title="AI Image Generator", layout="wide", page_icon="🎨")

# 2. Initialize Session State (Cart)
if 'prompt_cart' not in st.session_state:
    st.session_state.prompt_cart = []

# --- UI Header ---
st.title("🎨 AI Image Generator (English)")
st.write("Select options to build your prompt and generate images instantly.")

st.divider()

# --- Section 1: Input (Build Prompt) ---
col_input, col_cart = st.columns([1, 1], gap="large")

with col_input:
    st.subheader("1️⃣ Build your prompt")
    
    # Simple Layout for sentence building
    c1, c2, c3 = st.columns([0.2, 1, 0.2])
    with c1: st.markdown("### I am a")
    with c2:
        # Direct English Inputs
        subject = st.selectbox(
            "Select Subject", 
            ["Astronaut", "Cyberpunk Cat", "Medieval Knight", "Forest Fairy", "Futuristic Robot", "Cute Puppy"],
            label_visibility="collapsed"
        )
    
    # Style Selection (English)
    style = st.pills(
        "Select Art Style", 
        ["Cinematic Lighting", "Studio Ghibli Anime", "Watercolor", "8-bit Pixel Art", "Oil Painting", "Polaroid"],
        selection_mode="single",
        default="Cinematic Lighting"
    )
    
    # Construct the final prompt directly in English
    final_prompt = f"I am a {subject}, {style}, high quality, 8k"
    
    st.info(f"📍 Prompt: **{final_prompt}**")
    
    # Add to Cart
    if st.button("Add to Cart 📥", use_container_width=True):
        st.session_state.prompt_cart.append(final_prompt)
        st.toast("Prompt added to cart!", icon="🛒")

with col_cart:
    st.subheader("2️⃣ Your Cart")
    
    if st.session_state.prompt_cart:
        for i, p in enumerate(st.session_state.prompt_cart):
            st.text(f"{i+1}. {p}")
        
        if st.button("Clear Cart 🗑️"):
            st.session_state.prompt_cart = []
            st.rerun()
    else:
        st.write("Cart is empty.")

st.divider()

# --- Section 2: Generation ---
st.subheader("3️⃣ Generate Images")

if st.button("🚀 Generate All Images", type="primary", use_container_width=True):
    if not st.session_state.prompt_cart:
        st.error("Please add items to the cart first.")
    else:
        # Grid Layout
        cols = st.columns(3)
        
        for idx, prompt in enumerate(st.session_state.prompt_cart):
            # 1. URL Encode (Handle spaces and special chars)
            encoded_prompt = urllib.parse.quote(prompt)
            
            # 2. Random Seed (To ensure unique images)
            seed = random.randint(1, 99999)
            
            # 3. Construct URL (Using the stable '/p/' endpoint and 'flux' model)
            image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={seed}&model=flux"
            
            with cols[idx % 3]:
                # Display Image
                st.image(image_url, caption=f"#{idx+1}: {prompt}", use_container_width=True)
                
        st.success(f"✅ Generated {len(st.session_state.prompt_cart)} images successfully!")