import hashlib
import streamlit as st

# ----------------------------
# Helper functions
# ----------------------------


def hash_password(password: str) -> str:
    """Return SHA256 hex digest for password (deterministic)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


# ----------------------------
# Demo credentials (hashed)
# ----------------------------
# CHANGE THESE before sharing publicly. For production, load from env/secret store.
_demo_users = {
    # username: (display_name, hashed_password, role)
    "analyst": ("Analyst", hash_password("analyst123"), "analyst"),
    "cro":     ("CRO",     hash_password("cro123"),     "cro"),
}

# ----------------------------
# Auth helpers using session_state
# ----------------------------


def init_auth_state():
    if "auth" not in st.session_state:
        st.session_state.auth = {
            "logged_in": False,
            "username": None,
            "display_name": None,
            "role": None,
            "login_error": None
        }


def login_ui():
    """Render a compact login UI; returns True if logged in."""
    init_auth_state()
    auth = st.session_state.auth

    if auth["logged_in"]:
        st.sidebar.markdown(
            f"**Signed in as:** {auth['display_name']}  •  _{auth['role'].upper()}_")
        if st.sidebar.button("Logout"):
            logout()
            st.experimental_rerun()
        return True

    st.sidebar.header("🔐 Sign in")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Sign in"):
        success = authenticate(username.strip(), password)
        if success:
            st.experimental_rerun()
        else:
            st.session_state.auth["login_error"] = "Invalid username or password."

    if st.session_state.auth.get("login_error"):
        st.sidebar.error(st.session_state.auth["login_error"])
    st.sidebar.markdown("---")
    st.sidebar.write(
        "Demo accounts: `analyst` / `analyst123`, `cro` / `cro123`")
    return False


def authenticate(username: str, password: str) -> bool:
    init_auth_state()
    auth = st.session_state.auth

    if username in _demo_users:
        display_name, hashed_pw, role = _demo_users[username]
        if verify_password(password, hashed_pw):
            auth["logged_in"] = True
            auth["username"] = username
            auth["display_name"] = display_name
            auth["role"] = role
            auth["login_error"] = None
            return True

    # fail
    auth["login_error"] = "Invalid username or password."
    return False


def logout():
    if "auth" in st.session_state:
        st.session_state.auth = {
            "logged_in": False,
            "username": None,
            "display_name": None,
            "role": None,
            "login_error": None
        }


def current_user():
    init_auth_state()
    return st.session_state.auth
