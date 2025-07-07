import streamlit as st
import requests

API_BASE = "https://pureglow-backend.onrender.com/admin/posts"

st.set_page_config(page_title="Admin Dashboard – PureGlow Blog", layout="wide")

st.title("🛠️ Admin Panel – PureGlow Blog Manager")
st.markdown("Manage your skincare blog content using this admin interface.")

# Tabs for navigation
tab1, tab2 = st.tabs(["➕ Add New Post", "📋 View / Delete Posts"])

# -----------------------------------------------
# ➕ Tab: Add New Post
# -----------------------------------------------
with tab1:
    st.subheader("➕ Create a New Blog Post")
    with st.form("create_post_form", clear_on_submit=True):
        title = st.text_input("Title")
        slug = st.text_input("Slug (URL identifier)", help="Example: neem-facewash-uae")
        excerpt = st.text_area("Excerpt (short description)", max_chars=250)
        content = st.text_area("Full Content", height=200)
        thumbnail_url = st.text_input("Thumbnail Image URL")
        product_url = st.text_input("Amazon Product URL")
        image_urls = st.text_area("Gallery Image URLs (comma-separated)")
        tags = st.text_input("Tags (comma-separated)")
        rating = st.number_input("Rating", min_value=0.0, max_value=5.0, step=0.1)
        repeat_purchases = st.text_input("Repeat Purchases", help="Example: 2K+ bought again")

        submitted = st.form_submit_button("Create Post")
        if submitted:
            data = {
                "title": title,
                "slug": slug,
                "excerpt": excerpt,
                "content": content,
                "thumbnail_url": thumbnail_url,
                "product_url": product_url,
                "image_urls": image_urls,
                "tags": tags,
                "rating": rating,
                "repeat_purchases": repeat_purchases
            }
            res = requests.post(API_BASE + "/", json=data)
            if res.status_code == 201:
                st.success("✅ Post created successfully!")
            else:
                st.error(f"❌ Failed to create post: {res.json().get('detail')}")

# -----------------------------------------------
# 📋 Tab: View / Delete Posts
# -----------------------------------------------
with tab2:
    st.subheader("📋 All Blog Posts")
    res = requests.get(API_BASE + "/")
    if res.status_code == 200:
        posts = res.json()
        if not posts:
            st.info("No posts available.")
        else:
            for post in posts:
                with st.expander(f"📝 {post['title']}"):
                    st.markdown(f"**Slug:** `{post['slug']}`")
                    st.markdown(f"**Excerpt:** {post['excerpt']}")
                    st.markdown(f"**Product URL:** [Link]({post['product_url']})")
                    st.markdown(f"**Rating:** ⭐ {post.get('rating', 'N/A')}")
                    st.markdown(f"**Repeat Purchases:** {post.get('repeat_purchases', '')}")
                    if post.get("thumbnail_url"):
                        st.image(post["thumbnail_url"], width=200)
                    if st.button(f"🗑️ Delete '{post['title']}'", key=f"del_{post['id']}"):
                        del_res = requests.delete(f"{API_BASE}/{post['id']}")
                        if del_res.status_code == 204:
                            st.success("Post deleted successfully.")
                            st.experimental_rerun()
                        else:
                            st.error("Failed to delete post.")
    else:
        st.error("Failed to load posts. Is the backend running?")

# -----------------------------------------------
# 📋 Tab: View / Delete / Update Posts
# -----------------------------------------------
with tab2:
    st.subheader("📋 All Blog Posts")
    res = requests.get(API_BASE + "/")
    if res.status_code == 200:
        posts = res.json()
        if not posts:
            st.info("No posts available.")
        else:
            for post in posts:
                with st.expander(f"📝 {post['title']} (ID: {post['id']})"):
                    st.markdown(f"**Slug:** `{post['slug']}`")
                    st.markdown(f"**Excerpt:** {post['excerpt']}")
                    st.markdown(f"**Product URL:** [Link]({post['product_url']})")
                    st.markdown(f"**Rating:** ⭐ {post.get('rating', 'N/A')}")
                    st.markdown(f"**Repeat Purchases:** {post.get('repeat_purchases', '')}")
                    if post.get("thumbnail_url"):
                        st.image(post["thumbnail_url"], width=200)

                    st.markdown("---")
                    st.markdown("### ✏️ Edit Post")

                    with st.form(f"edit_form_{post['id']}"):
                        new_title = st.text_input("Title", post["title"])
                        new_slug = st.text_input("Slug", post["slug"])
                        new_excerpt = st.text_area("Excerpt", post["excerpt"])
                        new_content = st.text_area("Content", post["content"])
                        new_thumbnail_url = st.text_input("Thumbnail Image URL", post["thumbnail_url"])
                        new_product_url = st.text_input("Amazon Product URL", post["product_url"])
                        new_image_urls = st.text_input("Image URLs (comma-separated)", post["image_urls"])
                        new_tags = st.text_input("Tags (comma-separated)", post["tags"])
                        new_rating = st.number_input("Rating", 0.0, 5.0, float(post.get("rating", 0.0)), 0.1)
                        new_repeat = st.text_input("Repeat Purchases", post.get("repeat_purchases", ""))

                        update_submitted = st.form_submit_button("💾 Update Post")
                        if update_submitted:
                            update_data = {
                                "title": new_title,
                                "slug": new_slug,
                                "excerpt": new_excerpt,
                                "content": new_content,
                                "thumbnail_url": new_thumbnail_url,
                                "product_url": new_product_url,
                                "image_urls": new_image_urls,
                                "tags": new_tags,
                                "rating": new_rating,
                                "repeat_purchases": new_repeat
                            }
                            update_res = requests.put(f"{API_BASE}/{post['id']}", json=update_data)
                            if update_res.status_code == 200:
                                st.success("✅ Post updated successfully!")
                                st.experimental_rerun()
                            else:
                                st.error("❌ Failed to update post.")

                    if st.button(f"🗑️ Delete '{post['title']}'", key=f"del_{post['id']}"):
                        del_res = requests.delete(f"{API_BASE}/{post['id']}")
                        if del_res.status_code == 204:
                            st.success("🗑️ Post deleted successfully.")
                            st.experimental_rerun()
                        else:
                            st.error("❌ Failed to delete post.")
    else:
        st.error("❌ Failed to load posts. Is the backend running?")
