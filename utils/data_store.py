"""
Data layer for the LCN social media calendar.

Backend selection is automatic:
  * If a [gcp_service_account] block exists in Streamlit secrets, posts are
    read from and written to a Google Sheet, which gives real shared
    persistence.
  * Otherwise the app runs in local mode backed by data/posts.csv so it works
    the moment you clone it. On Streamlit Cloud that local file is ephemeral,
    so configure Google Sheets for durable storage.

Functions that touch Streamlit only read secrets and cache the client. The
reshaping helpers are pure so they can be tested without a running server.

SCHEMA NOTE
This app adds Series, Persona, and Pillar to the original schema. If you are
pointing it at an existing sheet, the new columns are created automatically the
first time anything saves. Nothing is lost.
"""

from __future__ import annotations

import hashlib
import os
import uuid

import pandas as pd
import streamlit as st

from utils import seed_content

# --- Schema ----------------------------------------------------------------

COLUMNS = [
    "ID", "Date", "Time", "Series", "Platform", "Persona", "Pillar",
    "Title", "Content", "Status", "Owner", "Link", "Notes",
]

# The two standing franchises, plus the opportunistic and ad hoc lanes.
SERIES = [
    "Atomic Essay Tuesday",
    "Burning Budget Thursday",
    "Observance",
    "Competitive Signal",
    "Other",
]

# Which weekday each franchise owns. Monday is 0, so Tuesday is 1, Thursday 3.
SERIES_WEEKDAY = {
    "Atomic Essay Tuesday": 1,
    "Burning Budget Thursday": 3,
}

PLATFORMS = [
    "LinkedIn personal",
    "LinkedIn company page",
    "Email nurture",
    "Website insights",
    "Short video",
    "X (Twitter)",
]

PERSONAS = [
    "Insights and Market Research",
    "Competitive Intelligence",
    "Marketing and Brand",
    "Medical Affairs",
    "Senior C Suite",
    "White Label Partners",
    "All personas",
]

PILLARS = [
    "I Problem First",
    "II Dimensional Insights",
    "III Decision Ready",
    "IV Proven and Validated",
    "I and III",
]

STATUSES = ["Idea", "Draft", "In review", "Approved", "Scheduled", "Published", "On hold"]

# LCN brand palette, taken from the logo. Used to colour code the calendar.
NAVY = "#13294B"
LCN_RED = "#9E1B32"
MID_BLUE = "#4A6FA5"
DEEP_BLUE = "#2F4F76"
SLATE = "#8A94A6"

SERIES_COLORS = {
    "Atomic Essay Tuesday": NAVY,
    "Burning Budget Thursday": LCN_RED,
    "Observance": MID_BLUE,
    "Competitive Signal": DEEP_BLUE,
    "Other": SLATE,
}
DEFAULT_COLOR = SLATE

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

    Cached as a resource so one authorised client is reused across reruns.
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
        sh = client.open(cfg.get("spreadsheet_name", "LCN Social Media Calendar"))

    ws_name = cfg.get("worksheet_name", "Posts")
    try:
        ws = sh.worksheet(ws_name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=ws_name, rows=400, cols=len(COLUMNS))
        ws.update([COLUMNS])
    return ws


# --- Pure helpers (safe to unit test) --------------------------------------

def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Force the frame onto the canonical schema with sensible dtypes.

    Reindexing on COLUMNS is what makes a schema change non destructive: any
    column the sheet does not have yet simply arrives empty.
    """
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
    """Order stable content hash, used to detect unsaved changes."""
    tmp = df.copy().reindex(columns=COLUMNS)
    tmp["Date"] = pd.to_datetime(tmp["Date"], errors="coerce").dt.strftime("%Y-%m-%d").fillna("")
    tmp = tmp.fillna("").astype(str)
    return hashlib.md5(tmp.to_csv(index=False).encode("utf-8")).hexdigest()


def apply_edits(full_df: pd.DataFrame, edited_view: pd.DataFrame) -> pd.DataFrame:
    """Merge cell edits made on a possibly filtered view back into the full
    dataset, matching rows by ID. The editor uses fixed rows, so this handles
    edits only. Additions and deletions happen elsewhere."""
    if edited_view is None or edited_view.empty:
        return full_df
    result = full_df.copy()
    result.index = result["ID"].astype(str)
    ev = edited_view.copy()
    ev.index = ev["ID"].astype(str)
    cols = [c for c in COLUMNS if c != "ID"]
    cols = [c for c in cols if c in ev.columns]
    common = result.index.intersection(ev.index)
    if len(common):
        result.loc[common, cols] = ev.loc[common, cols]
    return result.reset_index(drop=True)


def cadence_conflicts(df: pd.DataFrame) -> pd.DataFrame:
    """Rows where a franchise post is not on the weekday it owns.

    Atomic Essay belongs on Tuesday, Burning Budget on Thursday. Drifting off
    those days is the most common way a publishing cadence quietly dies, so the
    app surfaces it rather than waiting for someone to notice.
    """
    dates = pd.to_datetime(df["Date"], errors="coerce")
    flags = []
    for i, row in df.iterrows():
        want = SERIES_WEEKDAY.get(row.get("Series", ""))
        if want is None or pd.isna(dates.iloc[i]):
            continue
        if dates.iloc[i].weekday() != want:
            flags.append(i)
    return df.loc[flags].reset_index(drop=True)


def missing_slots(df: pd.DataFrame, start, end) -> list[dict]:
    """Tuesdays with no Atomic Essay and Thursdays with no Burning Budget."""
    dates = pd.to_datetime(df["Date"], errors="coerce")
    gaps = []
    for series, weekday in SERIES_WEEKDAY.items():
        taken = set(
            dates[(df["Series"] == series) & dates.notna()].dt.date.tolist()
        )
        for day in pd.date_range(start, end, freq="D"):
            if day.weekday() == weekday and day.date() not in taken:
                gaps.append({"Date": day.date(), "Series": series})
    return sorted(gaps, key=lambda g: (g["Date"], g["Series"]))


def to_events(df: pd.DataFrame) -> list[dict]:
    """Turn rows into FullCalendar event dicts, coloured by Series."""
    events = []
    for _, r in df.iterrows():
        if pd.isna(r["Date"]):
            continue
        day = pd.to_datetime(r["Date"]).strftime("%Y-%m-%d")
        time = str(r.get("Time", "")).strip()
        start = f"{day}T{time}" if time and ":" in time else day
        label = str(r["Title"]).strip() or str(r["Content"]).strip()[:32] or "(untitled)"
        colour = SERIES_COLORS.get(str(r.get("Series", "")), DEFAULT_COLOR)
        held = str(r.get("Status", "")).strip() in {"On hold", "Idea"}
        events.append(
            {
                "id": str(r["ID"]),
                "title": label,
                "start": start,
                "allDay": not (time and ":" in time),
                "backgroundColor": colour,
                "borderColor": colour,
                "textColor": "#FFFFFF",
                # Held rows read as provisional rather than committed.
                "classNames": ["lcn-held"] if held else [],
            }
        )
    return events


def seed_data() -> pd.DataFrame:
    """The LCN August and September 2026 calendar as shipped."""
    rows = seed_content.all_rows()
    df = pd.DataFrame(rows)
    df.insert(0, "ID", [uuid.uuid4().hex[:8] for _ in range(len(df))])
    return _normalize(df)


# --- Public load / save ----------------------------------------------------

def load_data() -> pd.DataFrame:
    """Load posts from the active backend, seeding the LCN calendar on first run."""
    if using_sheets():
        from gspread_dataframe import get_as_dataframe

        ws = _get_worksheet()
        df = get_as_dataframe(ws, evaluate_formulas=True, header=0)
        df = df.dropna(how="all")
        if df.empty:
            df = seed_data()
            save_data(df)
            return df
        return ensure_ids(_normalize(df))

    if os.path.exists(LOCAL_CSV):
        df = pd.read_csv(LOCAL_CSV)
        return ensure_ids(_normalize(df))

    df = seed_data()
    save_data(df)
    return df


def save_data(df: pd.DataFrame) -> pd.DataFrame:
    """Persist the full dataset. Returns the saved frame with IDs filled in."""
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
