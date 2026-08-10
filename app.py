"""
Social Media Calendar — a Streamlit app.

Two views over one shared dataset:
  • List     – an editable table; every change saves automatically.
  • Calendar – a month/week view, colour-coded by platform; drag an event
               to a new day to reschedule it (also saved automatically).

Storage is Google Sheets when configured, otherwise a local CSV. See README.
"""

import os
from datetime import date, datetime

import pandas as pd
import streamlit as st
from streamlit_calendar import calendar

from utils import data_store as ds

def check_password():
    if st.session_state.get("auth_ok"):
        return True
    pw = st.text_input("Password", type="password")
    if pw:
        if pw == st.secrets["app_password"]:
            st.session_state["auth_ok"] = True
            st.rerun()
        else:
            st.error("Incorrect password")
    return False

if not check_password():
    st.stop()

LOGO_PATH = os.path.join("assets", "logo.png")

st.set_page_config(
    page_title="Social Media Calendar",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
)

if os.path.exists(LOGO_PATH):
    try:
        st.logo(LOGO_PATH, size="large")
    except Exception:
        pass


# --------------------------------------------------------------------------
# Session state + save plumbing
# --------------------------------------------------------------------------

def _init_state():
    if "df" not in st.session_state:
        st.session_state.df = ds.load_data()
        st.session_state.saved_sig = ds.signature(st.session_state.df)
        st.session_state.editor_version = 0
        st.session_state.last_saved_at = None
        st.session_state.save_error = None
        st.session_state.selected_id = None
        st.session_state.cal_token = None


def reload_from_source():
    st.session_state.df = ds.load_data()
    st.session_state.saved_sig = ds.signature(st.session_state.df)
    st.session_state.save_error = None


def autosave_if_changed() -> bool:
    """Write to the backend only when the data actually changed."""
    sig = ds.signature(st.session_state.df)
    if sig == st.session_state.saved_sig:
        return False
    try:
        saved = ds.save_data(st.session_state.df)
        st.session_state.df = saved
        st.session_state.saved_sig = ds.signature(saved)
        st.session_state.last_saved_at = datetime.now().strftime("%H:%M:%S")
        st.session_state.save_error = None
        st.toast(f"Saved to {ds.backend_name()}", icon="✅")
        return True
    except Exception as exc:  # surfaced in the sidebar banner
        st.session_state.save_error = str(exc)
        st.toast("Couldn't save — see the sidebar", icon="⚠️")
        return False


_init_state()


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def fmt_day(value) -> str:
    if pd.isna(value):
        return "(no date)"
    return pd.to_datetime(value).strftime("%a %d %b %Y")


def row_label(row) -> str:
    title = str(row["Title"]).strip() or "(untitled)"
    return f"{fmt_day(row['Date'])} · {row['Platform']} · {title}"


def apply_filters(df, platforms, statuses, start, end) -> pd.DataFrame:
    out = df.copy()
    if platforms:
        out = out[out["Platform"].isin(platforms)]
    if statuses:
        out = out[out["Status"].isin(statuses)]
    if start and end:
        d = pd.to_datetime(out["Date"], errors="coerce")
        lo, hi = pd.Timestamp(start), pd.Timestamp(end)
        out = out[d.isna() | ((d >= lo) & (d <= hi))]
    return out.reset_index(drop=True)


COLUMN_CONFIG = {
    "ID": st.column_config.TextColumn("ID", disabled=True, width="small", help="Auto-generated"),
    "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD", width="small"),
    "Time": st.column_config.TextColumn("Time", width="small", help="Optional, e.g. 09:00"),
    "Platform": st.column_config.SelectboxColumn("Platform", options=ds.PLATFORMS, width="medium"),
    "Title": st.column_config.TextColumn("Title / Campaign", width="medium"),
    "Content": st.column_config.TextColumn("Content / Caption", width="large"),
    "Status": st.column_config.SelectboxColumn("Status", options=ds.STATUSES, width="small"),
    "Link": st.column_config.LinkColumn("Link", width="small", help="Post or media URL"),
    "Owner": st.column_config.TextColumn("Owner", width="small"),
    "Notes": st.column_config.TextColumn("Notes", width="medium"),
}
COLUMN_ORDER = ["Date", "Time", "Platform", "Title", "Content", "Status", "Link", "Owner", "Notes", "ID"]


# --------------------------------------------------------------------------
# Sidebar — filters, status, utilities
# --------------------------------------------------------------------------

with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)

    st.markdown("### Filters")
    st.caption("Applies to both views.")
    f_platforms = st.multiselect("Platform", ds.PLATFORMS, placeholder="All platforms")
    f_statuses = st.multiselect("Status", ds.STATUSES, placeholder="All statuses")

    dates = pd.to_datetime(st.session_state.df["Date"], errors="coerce").dropna()
    if len(dates):
        lo, hi = dates.min().date(), dates.max().date()
    else:
        lo = hi = date.today()
    f_range = st.date_input("Date range", value=(lo, hi))
    if isinstance(f_range, (list, tuple)) and len(f_range) == 2:
        d_start, d_end = f_range
    else:
        d_start = d_end = None

    st.divider()
    if st.button("🔄 Refresh from source", use_container_width=True):
        reload_from_source()
        st.rerun()

    csv_bytes = st.session_state.df.assign(
        Date=pd.to_datetime(st.session_state.df["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
    )[ds.COLUMNS].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv_bytes, "social_posts.csv", "text/csv", use_container_width=True)

    st.divider()
    if ds.using_sheets():
        st.success("Connected to Google Sheets", icon="🟢")
    else:
        st.info("Local demo mode. Configure Google Sheets in secrets for shared, persistent storage.", icon="🟡")
    if st.session_state.last_saved_at:
        st.caption(f"Last saved at {st.session_state.last_saved_at}")
    if st.session_state.save_error:
        st.error(f"Save failed: {st.session_state.save_error}")


# --------------------------------------------------------------------------
# Header + headline metrics
# --------------------------------------------------------------------------

st.title("Social Media Calendar")

df_all = st.session_state.df
_dates = pd.to_datetime(df_all["Date"], errors="coerce")
_today = pd.Timestamp(date.today())
week_mask = (_dates >= _today) & (_dates < _today + pd.Timedelta(days=7))

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total posts", len(df_all))
m2.metric("Scheduled", int((df_all["Status"] == "Scheduled").sum()))
m3.metric("Drafts + ideas", int(df_all["Status"].isin(["Draft", "Idea"]).sum()))
m4.metric("Next 7 days", int(week_mask.sum()))

# Filtered view shared by both tabs.
view_df = apply_filters(df_all, f_platforms, f_statuses, d_start, d_end)
filter_key = ds.signature(view_df[["ID"]]) if not view_df.empty else "empty"

list_tab, cal_tab = st.tabs(["📋  List", "📅  Calendar"])


# --------------------------------------------------------------------------
# List view — add, edit (autosave), delete
# --------------------------------------------------------------------------

with list_tab:
    with st.expander("➕  Add a post", expanded=(len(df_all) == 0)):
        with st.form("add_post", clear_on_submit=True):
            c1, c2, c3 = st.columns([1, 1, 1.4])
            in_date = c1.date_input("Date", value=date.today())
            in_time = c2.text_input("Time", placeholder="09:00")
            in_platform = c3.selectbox("Platform", ds.PLATFORMS)
            in_title = st.text_input("Title / Campaign")
            in_content = st.text_area("Content / Caption", height=110)
            c4, c5 = st.columns(2)
            in_status = c4.selectbox("Status", ds.STATUSES, index=1)
            in_owner = c5.text_input("Owner")
            in_link = st.text_input("Link / Media URL")
            in_notes = st.text_input("Notes")
            submitted = st.form_submit_button("Add post", type="primary", use_container_width=True)

        if submitted:
            new_row = {
                "ID": "", "Date": pd.Timestamp(in_date), "Time": in_time.strip(),
                "Platform": in_platform, "Title": in_title.strip(), "Content": in_content.strip(),
                "Status": in_status, "Link": in_link.strip(), "Owner": in_owner.strip(),
                "Notes": in_notes.strip(),
            }
            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame([new_row])], ignore_index=True
            )
            autosave_if_changed()
            st.session_state.editor_version += 1
            st.rerun()

    if view_df.empty:
        st.info("No posts match the current filters. Add one above or widen the filters in the sidebar.")
    else:
        st.caption("Edit any cell to update a post — changes save automatically.")
        edited = st.data_editor(
            view_df,
            key=f"editor_{filter_key}_{st.session_state.editor_version}",
            num_rows="fixed",
            hide_index=True,
            use_container_width=True,
            column_config=COLUMN_CONFIG,
            column_order=COLUMN_ORDER,
        )
        st.session_state.df = ds.apply_edits(st.session_state.df, edited)
        autosave_if_changed()

        with st.expander("🗑️  Delete posts"):
            labels = {row_label(r): str(r["ID"]) for _, r in view_df.iterrows()}
            to_delete = st.multiselect("Select posts to delete", list(labels.keys()))
            if st.button("Delete selected", disabled=not to_delete):
                ids = {labels[name] for name in to_delete}
                st.session_state.df = st.session_state.df[
                    ~st.session_state.df["ID"].astype(str).isin(ids)
                ].reset_index(drop=True)
                autosave_if_changed()
                st.session_state.editor_version += 1
                st.toast("Deleted", icon="🗑️")
                st.rerun()


# --------------------------------------------------------------------------
# Calendar view — colour-coded, click for details, drag to reschedule
# --------------------------------------------------------------------------

with cal_tab:
    if view_df.empty:
        st.info("Nothing to show on the calendar for the current filters.")
    else:
        legend = " ".join(
            f"<span style='display:inline-block;margin:2px 10px 2px 0;'>"
            f"<span style='display:inline-block;width:11px;height:11px;border-radius:3px;"
            f"background:{ds.PLATFORM_COLORS.get(p, ds.DEFAULT_COLOR)};vertical-align:middle;'></span> "
            f"<span style='vertical-align:middle;font-size:0.85rem;'>{p}</span></span>"
            for p in ds.PLATFORMS if p in set(view_df["Platform"])
        )
        if legend:
            st.markdown(legend, unsafe_allow_html=True)

        options = {
            "initialView": "dayGridMonth",
            "editable": True,            # enables drag-to-reschedule
            "selectable": False,
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,timeGridWeek,listWeek",
            },
            "height": 720,
            "firstDay": 1,
            "dayMaxEvents": True,
            "nowIndicator": True,
        }

        state = calendar(
            events=ds.to_events(view_df),
            options=options,
            key=f"calendar_{filter_key}",
        )

        if isinstance(state, dict):
            # Drag-to-reschedule -> update the post's Date and save.
            change = state.get("eventChange") or state.get("eventDrop")
            if change:
                ev = change.get("event", {})
                eid, new_start = ev.get("id"), ev.get("start")
                token = f"{eid}|{new_start}"
                if eid and new_start and st.session_state.cal_token != token:
                    st.session_state.cal_token = token
                    parsed = pd.to_datetime(new_start, errors="coerce")
                    if pd.notna(parsed):
                        mask = st.session_state.df["ID"].astype(str) == str(eid)
                        st.session_state.df.loc[mask, "Date"] = pd.Timestamp(parsed.date())
                        autosave_if_changed()
                        st.toast("Post rescheduled", icon="📆")
                        st.rerun()

            # Click an event -> remember which one to detail below.
            click = state.get("eventClick")
            if click:
                st.session_state.selected_id = click.get("event", {}).get("id")

        sel = st.session_state.selected_id
        if sel:
            match = df_all[df_all["ID"].astype(str) == str(sel)]
            if not match.empty:
                r = match.iloc[0]
                with st.container(border=True):
                    head = f"**{str(r['Title']).strip() or '(untitled)'}**"
                    st.markdown(f"{head} — {r['Platform'] or '—'} · {r['Status'] or '—'}")
                    when = fmt_day(r["Date"]) + (f" at {r['Time']}" if str(r["Time"]).strip() else "")
                    st.caption(when)
                    st.write(str(r["Content"]).strip() or "_No content yet._")
                    if str(r["Link"]).strip():
                        st.markdown(f"[Open link]({r['Link']})")
                    if str(r["Notes"]).strip():
                        st.caption(f"📝 {r['Notes']}")

        st.caption("Tip: drag an event to a new day to reschedule it, or click it to see details.")
