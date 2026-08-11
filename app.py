"""
LCN Consulting Social Media Calendar, a Streamlit app.

Three views over one shared dataset:
  List        an editable table where every change saves automatically.
  Calendar    a month or week view, colour coded by series. Drag an event to a
              new day to reschedule it, also saved automatically.
  Observances a reference calendar of health awareness and fun days, each with
              a fit rating and a compliance caution. Push any of them into the
              calendar as a draft in one click.

The calendar is built around two standing franchises:
  Atomic Essay Tuesday      one essay, one idea, one persona, one pillar
  Burning Budget Thursday   Q3 and Q4 spend down, one mechanic per post

Storage is Google Sheets when configured, otherwise a local CSV. See README.
"""

import os
from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st
from streamlit_calendar import calendar

from utils import data_store as ds
from utils import observances as obs

# --------------------------------------------------------------------------
# Page config must come before any other Streamlit call.
# --------------------------------------------------------------------------

st.set_page_config(
    page_title="LCN Social Media Calendar",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
)

LOGO_PATH = os.path.join("assets", "logo.png")


def check_password() -> bool:
    """Simple shared password gate. Skipped entirely when no password is set."""
    try:
        expected = st.secrets["app_password"]
    except Exception:
        return True  # no password configured, run open locally

    if st.session_state.get("auth_ok"):
        return True

    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=280)
    st.markdown("#### Social Media Calendar")
    pw = st.text_input("Password", type="password")
    if pw:
        if pw == expected:
            st.session_state["auth_ok"] = True
            st.rerun()
        else:
            st.error("Incorrect password")
    return False


if not check_password():
    st.stop()

if os.path.exists(LOGO_PATH):
    try:
        st.logo(LOGO_PATH, size="large")
    except Exception:
        pass

# Held rows read as provisional rather than committed.
st.markdown(
    """
    <style>
      .fc-event.lcn-held { opacity: 0.55; border-style: dashed !important; }
      .fc .fc-daygrid-day.fc-day-sat, .fc .fc-daygrid-day.fc-day-sun { background: #FAFBFC; }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------------------------------
# Session state and save plumbing
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
        st.toast("Could not save. See the sidebar.", icon="⚠️")
        return False


_init_state()


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

LINKEDIN_LIMIT = 3000


def fmt_day(value) -> str:
    if pd.isna(value):
        return "(no date)"
    return pd.to_datetime(value).strftime("%a %d %b %Y")


def row_label(row) -> str:
    title = str(row["Title"]).strip() or "(untitled)"
    return f"{fmt_day(row['Date'])} · {row['Series']} · {title}"


def apply_filters(df, series, platforms, statuses, personas, start, end) -> pd.DataFrame:
    out = df.copy()
    if series:
        out = out[out["Series"].isin(series)]
    if platforms:
        out = out[out["Platform"].isin(platforms)]
    if statuses:
        out = out[out["Status"].isin(statuses)]
    if personas:
        out = out[out["Persona"].isin(personas)]
    if start and end:
        d = pd.to_datetime(out["Date"], errors="coerce")
        lo, hi = pd.Timestamp(start), pd.Timestamp(end)
        out = out[d.isna() | ((d >= lo) & (d <= hi))]
    return out.reset_index(drop=True)


COLUMN_CONFIG = {
    "ID": st.column_config.TextColumn("ID", disabled=True, width="small", help="Auto generated"),
    "Date": st.column_config.DateColumn(
        "Date", format="YYYY-MM-DD", width="small",
        help="Leave blank to hold a post on the bench. Bench rows stay out of the calendar.",
    ),
    "Time": st.column_config.TextColumn("Time", width="small", help="Optional, for example 08:30"),
    "Series": st.column_config.SelectboxColumn(
        "Series", options=ds.SERIES, width="medium",
        help="Atomic Essay belongs on Tuesday. Burning Budget belongs on Thursday.",
    ),
    "Platform": st.column_config.SelectboxColumn("Platform", options=ds.PLATFORMS, width="medium"),
    "Persona": st.column_config.SelectboxColumn("Persona", options=ds.PERSONAS, width="medium"),
    "Pillar": st.column_config.SelectboxColumn("Pillar", options=ds.PILLARS, width="small"),
    "Title": st.column_config.TextColumn("Title", width="medium"),
    "Content": st.column_config.TextColumn("Post copy", width="large"),
    "Chars": st.column_config.NumberColumn(
        "Chars", disabled=True, width="small",
        help=f"LinkedIn allows {LINKEDIN_LIMIT:,}. Atomic essays run about 1,700 to 1,900.",
    ),
    "Status": st.column_config.SelectboxColumn("Status", options=ds.STATUSES, width="small"),
    "Owner": st.column_config.TextColumn("Owner", width="small"),
    "Link": st.column_config.LinkColumn("Link", width="small", help="Published post URL"),
    "Notes": st.column_config.TextColumn("Notes", width="medium"),
}
COLUMN_ORDER = [
    "Date", "Series", "Title", "Persona", "Pillar", "Status",
    "Content", "Chars", "Platform", "Time", "Owner", "Link", "Notes", "ID",
]


# --------------------------------------------------------------------------
# Sidebar: filters, status, utilities
# --------------------------------------------------------------------------

with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)

    st.markdown("### Filters")
    st.caption("Applies to the List and Calendar views.")
    f_series = st.multiselect("Series", ds.SERIES, placeholder="All series")
    f_statuses = st.multiselect("Status", ds.STATUSES, placeholder="All statuses")
    f_personas = st.multiselect("Persona", ds.PERSONAS, placeholder="All personas")
    f_platforms = st.multiselect("Platform", ds.PLATFORMS, placeholder="All platforms")

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
    st.download_button(
        "⬇️ Download CSV", csv_bytes, "lcn_social_calendar.csv", "text/csv",
        use_container_width=True,
    )

    st.divider()
    if ds.using_sheets():
        st.success("Connected to Google Sheets", icon="🟢")
    else:
        st.info(
            "Local mode. Configure Google Sheets in secrets for shared, persistent storage.",
            icon="🟡",
        )
    if st.session_state.last_saved_at:
        st.caption(f"Last saved at {st.session_state.last_saved_at}")
    if st.session_state.save_error:
        st.error(f"Save failed: {st.session_state.save_error}")

    st.divider()
    st.caption(
        "Voice rules: no dashes of any kind, including hyphens. No medical, efficacy, "
        "or off label claims. No invented statistics or client names."
    )


# --------------------------------------------------------------------------
# Header, metrics, cadence health
# --------------------------------------------------------------------------

st.title("Social Media Calendar")
st.caption(
    "Atomic Essay Tuesday and Burning Budget Thursday, with observances on the days between."
)

df_all = st.session_state.df
_dates = pd.to_datetime(df_all["Date"], errors="coerce")
_today = pd.Timestamp(date.today())
week_mask = (_dates >= _today) & (_dates < _today + pd.Timedelta(days=7))

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Atomic essays", int((df_all["Series"] == "Atomic Essay Tuesday").sum()))
m2.metric("Burning Budget", int((df_all["Series"] == "Burning Budget Thursday").sum()))
m3.metric("Observances", int((df_all["Series"] == "Observance").sum()))
m4.metric("Needs a decision", int(df_all["Status"].isin(["Idea", "On hold"]).sum()))
m5.metric("Next 7 days", int(week_mask.sum()))

# Cadence health. A publishing program dies from drift, so surface it early.
conflicts = ds.cadence_conflicts(df_all)
if len(dates):
    gaps = ds.missing_slots(df_all, max(dates.min().date(), date(2026, 8, 1)), dates.max().date())
else:
    gaps = []
long_posts = df_all[df_all["Content"].str.len() > LINKEDIN_LIMIT]

if len(conflicts) or gaps or len(long_posts):
    with st.expander(
        f"⚠️  Cadence and compliance checks  ({len(conflicts)} off day, "
        f"{len(gaps)} empty slot, {len(long_posts)} over length)",
        expanded=False,
    ):
        if len(conflicts):
            st.markdown("**Franchise posts on the wrong weekday**")
            st.caption(
                "Atomic Essay belongs on Tuesday, Burning Budget on Thursday. "
                "Drift is how a cadence quietly dies."
            )
            st.dataframe(
                conflicts.assign(
                    Day=pd.to_datetime(conflicts["Date"]).dt.strftime("%A %d %b")
                )[["Day", "Series", "Title"]],
                hide_index=True, use_container_width=True,
            )
        if gaps:
            st.markdown("**Empty franchise slots**")
            st.caption("Pull from the bench rather than skipping a week.")
            st.dataframe(pd.DataFrame(gaps), hide_index=True, use_container_width=True)
        if len(long_posts):
            st.markdown("**Over the LinkedIn character limit**")
            st.dataframe(
                long_posts.assign(Chars=long_posts["Content"].str.len())[
                    ["Date", "Series", "Title", "Chars"]
                ],
                hide_index=True, use_container_width=True,
            )

# Filtered view shared by the first two tabs.
view_df = apply_filters(
    df_all, f_series, f_platforms, f_statuses, f_personas, d_start, d_end
)
filter_key = ds.signature(view_df[["ID"]]) if not view_df.empty else "empty"

list_tab, cal_tab, obs_tab = st.tabs(["📋  List", "📅  Calendar", "🎉  Observances"])


# --------------------------------------------------------------------------
# List view: add, edit with autosave, delete
# --------------------------------------------------------------------------

with list_tab:
    with st.expander("➕  Add a post", expanded=(len(df_all) == 0)):
        with st.form("add_post", clear_on_submit=True):
            c1, c2, c3 = st.columns([1, 1, 1.4])
            in_date = c1.date_input("Date", value=date.today())
            in_time = c2.text_input("Time", placeholder="08:30")
            in_series = c3.selectbox("Series", ds.SERIES)
            c4, c5, c6 = st.columns([1.4, 1.2, 1])
            in_platform = c4.selectbox("Platform", ds.PLATFORMS)
            in_persona = c5.selectbox("Persona", [""] + ds.PERSONAS)
            in_pillar = c6.selectbox("Pillar", [""] + ds.PILLARS)
            in_title = st.text_input("Title")
            in_content = st.text_area("Post copy", height=160)
            c7, c8 = st.columns(2)
            in_status = c7.selectbox("Status", ds.STATUSES, index=1)
            in_owner = c8.text_input("Owner")
            in_notes = st.text_input("Notes")
            submitted = st.form_submit_button(
                "Add post", type="primary", use_container_width=True
            )

        if submitted:
            new_row = {
                "ID": "", "Date": pd.Timestamp(in_date), "Time": in_time.strip(),
                "Series": in_series, "Platform": in_platform, "Persona": in_persona,
                "Pillar": in_pillar, "Title": in_title.strip(),
                "Content": in_content.strip(), "Status": in_status,
                "Owner": in_owner.strip(), "Link": "", "Notes": in_notes.strip(),
            }
            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame([new_row])], ignore_index=True
            )
            autosave_if_changed()
            st.session_state.editor_version += 1
            st.rerun()

    if view_df.empty:
        st.info("No posts match the current filters. Add one above or widen the filters.")
    else:
        st.caption(
            "Edit any cell to update a post. Changes save automatically. "
            "Clear a date to move a post to the bench."
        )
        editable = view_df.assign(Chars=view_df["Content"].str.len())
        edited = st.data_editor(
            editable,
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
# Calendar view: colour coded by series, click for detail, drag to reschedule
# --------------------------------------------------------------------------

with cal_tab:
    if view_df.empty:
        st.info("Nothing to show on the calendar for the current filters.")
    else:
        present = set(view_df["Series"])
        legend = " ".join(
            f"<span style='display:inline-block;margin:2px 14px 2px 0;'>"
            f"<span style='display:inline-block;width:11px;height:11px;border-radius:3px;"
            f"background:{ds.SERIES_COLORS.get(s, ds.DEFAULT_COLOR)};vertical-align:middle;'>"
            f"</span> <span style='vertical-align:middle;font-size:0.85rem;'>{s}</span></span>"
            for s in ds.SERIES if s in present
        )
        if legend:
            st.markdown(legend, unsafe_allow_html=True)
        st.caption("Faded and dashed events are still an idea or on hold.")

        undated = int(pd.to_datetime(view_df["Date"], errors="coerce").isna().sum())
        if undated:
            st.caption(
                f"{undated} bench post{'s' if undated != 1 else ''} have no date "
                "and are visible in the List view only."
            )

        options = {
            "initialView": "dayGridMonth",
            "initialDate": "2026-08-01",
            "editable": True,            # enables drag to reschedule
            "selectable": False,
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,timeGridWeek,listWeek",
            },
            "height": 760,
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
            # Drag to reschedule, then save.
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
                        moved = st.session_state.df.loc[mask]
                        if not moved.empty:
                            want = ds.SERIES_WEEKDAY.get(moved.iloc[0]["Series"])
                            if want is not None and parsed.weekday() != want:
                                st.toast(
                                    "Moved, but that series belongs on another weekday.",
                                    icon="⚠️",
                                )
                            else:
                                st.toast("Post rescheduled", icon="📆")
                        st.rerun()

            click = state.get("eventClick")
            if click:
                st.session_state.selected_id = click.get("event", {}).get("id")

        sel = st.session_state.selected_id
        if sel:
            match = df_all[df_all["ID"].astype(str) == str(sel)]
            if not match.empty:
                r = match.iloc[0]
                with st.container(border=True):
                    st.markdown(f"**{str(r['Title']).strip() or '(untitled)'}**")
                    meta = " · ".join(
                        p for p in [
                            str(r["Series"]).strip(),
                            str(r["Persona"]).strip(),
                            f"Pillar {r['Pillar']}" if str(r["Pillar"]).strip() else "",
                            str(r["Status"]).strip(),
                        ] if p
                    )
                    st.caption(meta)
                    when = fmt_day(r["Date"]) + (
                        f" at {r['Time']}" if str(r["Time"]).strip() else ""
                    )
                    chars = len(str(r["Content"]))
                    st.caption(f"{when}  ·  {chars:,} characters  ·  {r['Platform']}")
                    st.write(str(r["Content"]).strip() or "_No copy yet._")
                    if str(r["Link"]).strip():
                        st.markdown(f"[Open link]({r['Link']})")
                    if str(r["Notes"]).strip():
                        st.info(f"📝 {r['Notes']}")

        st.caption("Tip: drag an event to a new day to reschedule it, or click it for the copy.")


# --------------------------------------------------------------------------
# Observances view: reference calendar, fit ratings, one click to add
# --------------------------------------------------------------------------

with obs_tab:
    st.markdown("### Health awareness and fun days")
    st.caption(
        "Reference list with a fit rating and a compliance caution for each day. "
        "Suggested post dates avoid Tuesday and Thursday so nothing collides with "
        "the two standing franchises."
    )

    with st.container(border=True):
        st.markdown("**The standing rule on disease awareness days**")
        st.write(
            "A disease awareness post is about the evidence or the decision challenge. "
            "Never about the disease, the treatment, the outcomes, or any product. "
            "Do not post on a therapeutic area where LCN has a live engagement, because "
            "it reads as promotion by proxy. If a post cannot be written without touching "
            "one of those, it does not get written."
        )

    rows = pd.DataFrame(obs.as_rows())

    c1, c2, c3 = st.columns([1, 1, 1])
    fit_pick = c1.multiselect("Fit", obs.FIT_ORDER, placeholder="All ratings")
    cat_pick = c2.multiselect(
        "Category", ["Health", "Fun", "Remembrance"], placeholder="All categories"
    )
    horizon = c3.selectbox(
        "Window", ["Everything on file", "Next 30 days", "Next 60 days", "Next 90 days"], index=0
    )

    shown = rows.copy()
    if fit_pick:
        shown = shown[shown["Fit"].isin(fit_pick)]
    if cat_pick:
        shown = shown[shown["Category"].isin(cat_pick)]
    if horizon != "Everything on file":
        days = int(horizon.split()[1])
        cutoff = date.today() + timedelta(days=days)
        shown = shown[
            (shown["Observed"] >= date.today()) & (shown["Observed"] <= cutoff)
        ]

    avoid = shown[shown["Fit"] == "Avoid"]
    if not avoid.empty:
        st.warning(
            "Do not publish commercial content on: "
            + ", ".join(
                f"{r['Observance']} ({r['Observed'].strftime('%d %b')})"
                for _, r in avoid.iterrows()
            ),
            icon="🛑",
        )

    if shown.empty:
        st.info("No observances match the current selection.")
    else:
        st.dataframe(
            shown,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Observed": st.column_config.DateColumn("Real date", format="ddd DD MMM"),
                "Suggested post date": st.column_config.DateColumn(
                    "Post on", format="ddd DD MMM",
                    help="Avoids Tuesday and Thursday, which belong to the franchises.",
                ),
                "Observance": st.column_config.TextColumn("Observance", width="medium"),
                "Runs": st.column_config.TextColumn("Runs", width="small"),
                "Category": st.column_config.TextColumn("Category", width="small"),
                "Fit": st.column_config.TextColumn("Fit", width="small"),
                "Angle": st.column_config.TextColumn("Angle", width="large"),
                "Caution": st.column_config.TextColumn("Caution", width="large"),
            },
        )

        st.divider()
        st.markdown("**Add one to the calendar**")
        addable = shown[shown["Fit"] != "Avoid"]
        if addable.empty:
            st.caption("Nothing in the current selection is safe to add automatically.")
        else:
            pick = st.selectbox(
                "Observance",
                [
                    f"{r['Observance']}  ·  post {r['Suggested post date'].strftime('%a %d %b')}"
                    for _, r in addable.iterrows()
                ],
            )
            if st.button("Add as a draft post", type="primary"):
                chosen = addable.iloc[
                    [
                        i for i, (_, r) in enumerate(addable.iterrows())
                        if pick.startswith(r["Observance"])
                    ][0]
                ]
                new_row = {
                    "ID": "",
                    "Date": pd.Timestamp(chosen["Suggested post date"]),
                    "Time": "08:30",
                    "Series": "Observance",
                    "Platform": "LinkedIn personal",
                    "Persona": "",
                    "Pillar": "",
                    "Title": chosen["Observance"],
                    "Content": f"ANGLE, NOT YET DRAFTED.\n\n{chosen['Angle']}",
                    "Status": "Idea",
                    "Owner": "Marketing",
                    "Link": "",
                    "Notes": f"{chosen['Fit']}. {chosen['Caution']}",
                }
                st.session_state.df = pd.concat(
                    [st.session_state.df, pd.DataFrame([new_row])], ignore_index=True
                )
                autosave_if_changed()
                st.session_state.editor_version += 1
                st.toast("Added as a draft in the List view", icon="🎉")
                st.rerun()

    st.caption(
        "Edit the list in utils/observances.py. It carries into next year with only the "
        "dates updated."
    )
