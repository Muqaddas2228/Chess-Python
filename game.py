import streamlit as st

# Sample product data
products = [
    {"id": 1, "name": "Laptop", "price": 999, "image": "💻"},
    {"id": 2, "name": "Smartphone", "price": 499, "image": "📱"},
    {"id": 3, "name": "Headphones", "price": 199, "image": "🎧"},
    {"id": 4, "name": "Smartwatch", "price": 299, "image": "⌚"}
]

# Initialize session state for cart if not already done
if "cart" not in st.session_state:
    st.session_state.cart = []

st.title("🛒 Simple E-Commerce App")

# Display products
st.subheader("Products")
cols = st.columns(len(products))
for idx, product in enumerate(products):
    with cols[idx]:
        st.markdown(f"**{product['image']} {product['name']}**")
        st.write(f"💲{product['price']}")
        if st.button(f"Add to Cart {product['name']}", key=product["id"]):
            st.session_state.cart.append(product)
            st.success(f"Added {product['name']} to cart!")

# Display Cart
st.sidebar.header("🛍️ Shopping Cart")
if st.session_state.cart:
    total = 0
    for item in st.session_state.cart:
        st.sidebar.write(f"{item['image']} {item['name']} - 💲{item['price']}")
        total += item['price']
    st.sidebar.write("---")
    st.sidebar.write(f"**Total: 💲{total}**")
    if st.sidebar.button("Checkout"):
        st.sidebar.success("Checkout successful! Thank you for your purchase.")
        st.session_state.cart = []  # Clear cart after checkout
else:
    st.sidebar.write("Your cart is empty.")
