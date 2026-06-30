"""
Data layer for the Social Media Calendar.

Backend selection is automatic:
  * If a [gcp_service_account] block exists in Streamlit secrets, posts are
    read from / written to a Google Sheet (real, shared persistence).
  * Otherwise the app runs in local demo mode backed by data/posts.csv so it
    works the moment you clone it. (Note: on Streamlit Cloud the local file is
    ephemeral — configure Google Sheets for durable storage.)

The functions that touch Streamlit only read secrets / cache the client.
The reshaping helpers (apply_edits, ensure_ids, signature, ...) are pure so
they can be unit-tested without a running Streamlit server.
"""

from __future__ import annotations

import hashlib
import os
import uuid
from datetime import date, timedelta

import pandas as pd
import streamlit as st

# --- Schema ----------------------------------------------------------------

COLUMNS = ["ID", "Date", "Time", "Platform", "Title", "Content", "Status", "Link", "Owner", "Notes"]

PLATFORMS = [
    "Instagram", "Facebook", "X (Twitter)", "LinkedIn",
    "TikTok", "YouTube", "Threads", "Pinterest",
]

STATUSES = ["Idea", "Draft", "Scheduled", "Published", "On hold"]

# Brand-ish colours used only to colour-code events in the calendar view.
PLATFORM_COLORS = {
    "Instagram": "#E1306C",
    "Facebook": "#1877F2",
    "X (Twitter)": "#14171A",
    "LinkedIn": "#0A66C2",
    "TikTok": "#FE2C55",
    "YouTube": "#FF0000",
    "Threads": "#3D3D3D",
    "Pinterest": "#E60023",
}
DEFAULT_COLOR = "#4F46E5"

LOCAL_CSV = os.path.join("data", "posts.csv")


# --- Backend detection -----------------------------------------------------

def using_sheets() -> bool:
    """True when Google Sheets credentials are configured."""
    try:
        return "gcp_service_account" in st.secrets
    except Exception:
        return False


def backend_name() -> str:
    return "Google Sheets" if using_sheets() else "local file"


@st.cache_resource(show_spinner=False)
def _get_worksheet():
    """Authorise with the service account and return the target worksheet.

    Cached as a resource so we reuse one authorised client across reruns.
    """
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]), scopes=scopes
    )
    client = gspread.authorize(creds)

    cfg = dict(st.secrets.get("gsheets", {}))
    if cfg.get("spreadsheet_key"):
        sh = client.open_by_key(cfg["spreadsheet_key"])
    elif cfg.get("spreadsheet_url"):
        sh = client.open_by_url(cfg["spreadsheet_url"])
    else:
        sh = client.open(cfg.get("spreadsheet_name", "Social Media Calendar"))

    ws_name = cfg.get("worksheet_name", "Posts")
    try:
        ws = sh.worksheet(ws_name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=ws_name, rows=200, cols=len(COLUMNS))
        ws.update([COLUMNS])
    return ws


# --- Pure helpers (safe to unit test) --------------------------------------

def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Force the frame onto the canonical schema with sensible dtypes."""
    df = df.reindex(columns=COLUMNS)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    for col in COLUMNS:
        if col != "Date":
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df.reset_index(drop=True)


def ensure_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Give every row a stable short ID, generating one for blanks."""
    df = df.copy()
    ids = df["ID"].fillna("").astype(str).str.strip() if "ID" in df else pd.Series([""] * len(df))
    df["ID"] = [v if v else uuid.uuid4().hex[:8] for v in ids]
    return df


def signature(df: pd.DataFrame) -> str:
    """Order-stable content hash, used to detect unsaved changes."""
    tmp = df.copy().reindex(columns=COLUMNS)
    tmp["Date"] = pd.to_datetime(tmp["Date"], errors="coerce").dt.strftime("%Y-%m-%d").fillna("")
    tmp = tmp.fillna("").astype(str)
    return hashlib.md5(tmp.to_csv(index=False).encode("utf-8")).hexdigest()


def apply_edits(full_df: pd.DataFrame, edited_view: pd.DataFrame) -> pd.DataFrame:
    """Merge cell edits made on a (possibly filtered) view back into the full
    dataset, matching rows by ID. The editor uses fixed rows, so this only
    handles edits — additions and deletions are done elsewhere."""
    if edited_view is None or edited_view.empty:
        return full_df
    result = full_df.copy()
    result.index = result["ID"].astype(str)
    ev = edited_view.copy()
    ev.index = ev["ID"].astype(str)
    cols = [c for c in COLUMNS if c != "ID"]
    common = result.index.intersection(ev.index)
    if len(common):
        result.loc[common, cols] = ev.loc[common, cols]
    return result.reset_index(drop=True)


def to_events(df: pd.DataFrame) -> list[dict]:
    """Turn rows into FullCalendar event dicts for the calendar view."""
    events = []
    for _, r in df.iterrows():
        if pd.isna(r["Date"]):
            continue
        day = pd.to_datetime(r["Date"]).strftime("%Y-%m-%d")
        time = str(r.get("Time", "")).strip()
        start = f"{day}T{time}" if time and ":" in time else day
        label = str(r["Title"]).strip() or str(r["Content"]).strip()[:32] or "(untitled)"
        events.append(
            {
                "id": str(r["ID"]),
                "title": f"{r['Platform']} · {label}" if r["Platform"] else label,
                "start": start,
                "allDay": not (time and ":" in time),
                "backgroundColor": PLATFORM_COLORS.get(r["Platform"], DEFAULT_COLOR),
                "borderColor": PLATFORM_COLORS.get(r["Platform"], DEFAULT_COLOR),
                "textColor": "#FFFFFF",
            }
        )
    return events


def sample_data() -> pd.DataFrame:
    """A small, today-relative seed so the calendar looks alive on first run."""
    today = date.today()

    def d(offset):
        return pd.Timestamp(today + timedelta(days=offset))

    rows = [
        [d(-3), "09:00", "Instagram", "Behind the scenes", "A peek at how we build things this week. #buildinpublic", "Published", "", "Maya", ""],
        [d(-1), "12:30", "LinkedIn", "Founder note", "Why we started — three lessons from year one.", "Published", "", "Sam", ""],
        [d(0), "08:00", "X (Twitter)", "Launch teaser", "Something new drops Friday. Any guesses? 👀", "Scheduled", "", "Maya", "Pin to top"],
        [d(1), "17:00", "TikTok", "Quick tip", "60-second tutorial: getting started in under a minute.", "Draft", "", "Lee", "Need to film"],
        [d(2), "10:00", "Facebook", "Customer story", "How @client cut their workflow in half.", "Scheduled", "", "Sam", ""],
        [d(4), "11:00", "Instagram", "Product reel", "New feature walkthrough, set to music.", "Draft", "", "Lee", "Awaiting assets"],
        [d(7), "09:30", "YouTube", "Deep dive", "Full 10-minute explainer on the new release.", "Idea", "", "Maya", ""],
        [d(9), "15:00", "LinkedIn", "Hiring post", "We're growing — two roles open on the team.", "Idea", "", "Sam", ""],
        [d(14), "13:00", "Pinterest", "Inspiration board", "Seasonal mood board for the spring campaign.", "Idea", "", "Lee", ""],
    ]
    df = pd.DataFrame(rows, columns=[c for c in COLUMNS if c != "ID"])
    df.insert(0, "ID", [uuid.uuid4().hex[:8] for _ in range(len(df))])
    return _normalize(df)


# --- Public load / save ----------------------------------------------------

def load_data() -> pd.DataFrame:
    """Load posts from the active backend, seeding demo data on first local run."""
    if using_sheets():
        from gspread_dataframe import get_as_dataframe

        ws = _get_worksheet()
        df = get_as_dataframe(ws, evaluate_formulas=True, header=0)
        df = df.dropna(how="all")
        return ensure_ids(_normalize(df))

    if os.path.exists(LOCAL_CSV):
        df = pd.read_csv(LOCAL_CSV)
        return ensure_ids(_normalize(df))

    # First local run: seed sample data and persist it.
    df = sample_data()
    save_data(df)
    return df


def save_data(df: pd.DataFrame) -> pd.DataFrame:
    """Persist the full dataset. Returns the saved frame (with IDs filled in)."""
    df = ensure_ids(_normalize(df))
    out = df.copy()
    out["Date"] = out["Date"].dt.strftime("%Y-%m-%d").fillna("")

    if using_sheets():
        from gspread_dataframe import set_with_dataframe

        ws = _get_worksheet()
        ws.clear()
        set_with_dataframe(ws, out[COLUMNS], include_index=False, resize=True)
    else:
        os.makedirs(os.path.dirname(LOCAL_CSV), exist_ok=True)
        out[COLUMNS].to_csv(LOCAL_CSV, index=False)

    return df
