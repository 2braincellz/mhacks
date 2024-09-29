import streamlit as st

from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(page_title="home")

#sections = st.sidebar.toggle("Sections", value=True, key="use_sections")

#nav = get_nav_from_toml(
#    ".streamlit/pages_sections.toml" if sections else ".streamlit/pages.toml"
#)

#st.logo("logo.png")

#pg = st.navigation(nav)

#add_page_title(pg)


st.title("home")
st.markdown("---")
st.sidebar.success("Select a page")
st.markdown(
        """
        GAAT is an innovative and all-encompassing student hub application designed to both seamlessly integrate
        the physical and digital worlds. This connection allows us to more deeply integrate traditional and modern
        forms of life to unlock greater levels of personal reflection.

        **👈 Check out some of our features on the sidebar!**
        """
        )
st.markdown(
        """
        > The unexamined life is not worth living\n
        Socrates
        """
        )

# Footer
st.markdown("---")
st.markdown("GAAT: Greatest App of All Time")
