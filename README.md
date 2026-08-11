# LCN Social Media Calendar

A Streamlit app for running LCN's publishing program, built around two standing franchises and an observance engine.

- **📋 List** an editable table. Edit any cell and it saves automatically. Clear a date to move a post to the bench.
- **📅 Calendar** a month or week view, color coded by series. Click a post for the full copy, or **drag it to a new day** to reschedule. The app warns you if a drag moves a franchise post off the weekday it owns.
- **🎉 Observances** a reference calendar of health awareness and fun days, each carrying a fit rating and a compliance caution. One click adds any of them to the calendar as a draft.

Storage is a **Google Sheet** when configured, otherwise a local CSV so it runs the moment you clone it.

---

## The two franchises

The whole calendar is built on a fixed weekly rhythm. Two posts a week, same two days, every week. Consistency is the point: an audience learns a cadence, and the cadence is what makes a modest volume of publishing compound.

**The program starts Tuesday August 18, 2026** and runs to Tuesday September 29. Thirteen franchise posts, thirteen observance rows, and thirteen posts held on the bench.

### Atomic Essay Tuesday

One essay, one idea, one persona, anchored to one positioning pillar. Names the cost of answering a high stakes question from fragmented sources. The method stays invisible and LCN is never positioned as a vendor, with a single deliberate exception in the closing post of the quarter.

Seven dated essays, from August 18 to September 29, plus seven more on the bench. The arc runs problem, then planning deadline, then defensibility, then peak commercial argument, then the underserved persona, then proof, then one explicit ask in the closing post.

Roughly 270 to 300 words, or 1,600 to 1,900 characters. That is about 60 percent of the LinkedIn limit. The length is deliberate: an expert reader will not give attention to a post that states a problem and stops, but will give it to one that explains the mechanism behind the problem.

### Burning Budget Thursday

Q3 and Q4 spend down. One mechanic of the fiscal year close per post, and what that mechanic costs. Every post reframes unspent budget as a decision made with less rather than money saved.

Six dated posts, from August 20 to September 24, plus two on the bench. The escalation runs governance, then the October approval deadline, then procurement lead time as the real deadline rather than December 31, then the carryover myth and why finance punishes an underspend, then three ranked uses for an amount too small to fit the standard menu, then last call.

### Observances

Health awareness and fun days, published on **Monday, Wednesday, or Friday only**, so nothing ever collides with the two franchises. Where a real observance falls on a Tuesday, a Thursday, or a weekend, the app suggests the nearest free day and the post references the day as upcoming.

Thirteen dated observance rows, plus twenty nine days on file in the reference calendar including an October look ahead. Four rows whose 2026 dates have already passed sit on the bench with their copy intact, ready for next year.

---

## The standing rule on disease awareness days

Disease awareness observances are the single highest compliance risk in this repo, and the rule is absolute.

**A disease awareness post is about the evidence or the decision challenge. Never about the disease, the treatment, the outcomes, or any product.** Do not post on a therapeutic area where LCN has a live engagement, because it reads as promotion by proxy. If a post cannot be written without touching one of those, it does not get written.

Three rows are deliberately held at **On hold** and should be decided rather than defaulted:

| Date | Row | Why |
|---|---|---|
| August 31 | International Overdose Awareness Day | No appropriate commercial angle exists |
| September 2 | Childhood Cancer Awareness Month | Legitimate angle, severe tone risk, needs senior sign off |
| September 11 | September 11 remembrance | **Publish nothing commercial.** This row exists so the date is visible in the calendar rather than discovered by accident |

Before the week of September 7, check three things: no scheduled LinkedIn post lands on September 11, no nurture email is queued to send, and no automated sequence fires that day.

---

## Voice rules, enforced by review not by code

- **No dashes of any kind.** No em dash, no en dash, no hyphen as a connector. Commas, colons, and separate sentences instead. Compound terms phrased so they need no hyphen.
- No medical, efficacy, or off label claims about any product.
- No invented statistics, client names, or proof points.
- American spellings.
- Lead with the implication, not the setup. Active voice. No hedging.

---

## Flagged before publication

Two items are blocking and live in the row Notes as well as here.

1. **The Seton Hall figure.** The essay dated September 22 cites a 34 percent average advantage. That figure comes from prior internal narrative rather than from the source study. Confirm the figure, the study year, and the sample, or cut the clause and run the ranking claim alone, which is fully supported: LCN ranked above competitors on accuracy, insight quality, client service, and trust.
2. **Keep the two proof points separate.** The Seton Hall result and the count of more than one hundred brand engagements measure different things. Conflating them weakens both.

Also open: the contact line in the September 29 closing essay is a placeholder, and several observance drafts carry a `[PLACEHOLDER: ...]` marker where a real personal detail is needed. Do not publish a book you have not read or a dog that does not exist.

---

## Cadence and compliance checks

The header carries an expander that fires automatically when any of three things is true:

- A franchise post sits on the wrong weekday. Drift is how a publishing program quietly dies.
- A Tuesday or Thursday inside the date range has no franchise post. Pull from the bench rather than skipping a week.
- Any post exceeds the LinkedIn character limit.

The **Chars** column in the List view is computed live and read only.

---

## 1. Run it locally

```bash
git clone https://github.com/<your-username>/lcn-social-calendar.git
cd lcn-social-calendar
pip install -r requirements.txt
streamlit run app.py
```

It opens at `http://localhost:8501`. On first run it seeds the full calendar, thirty nine rows, so nothing is empty. The sidebar says **Local mode** until Google Sheets is connected.

> In local mode data lives in `data/posts.csv` on your machine. Fine for trying it. For shared, durable storage, and especially once deployed, use Google Sheets.

---

## 2. Connect Google Sheets (recommended)

**a. Create a Google Cloud project and enable two APIs**
1. Go to <https://console.cloud.google.com/> and create or pick a project.
2. Enable both **Google Sheets API** and **Google Drive API** under APIs and Services, then Library.

**b. Create a service account and a key**
1. APIs and Services, then **Credentials**, then Create credentials, then **Service account**.
2. Open the new service account, then **Keys**, then Add key, then **JSON**. A `.json` file downloads. Keep it private.

**c. Create the sheet and share it with the service account**
1. Create a new Google Sheet, any name.
2. Click **Share** and add the service account email, the `client_email` from the JSON ending in `…iam.gserviceaccount.com`, as an **Editor**.
3. Copy the sheet ID from the URL: `https://docs.google.com/spreadsheets/d/`**`THIS_PART`**`/edit`.

**d. Add the credentials to Streamlit secrets**
1. Copy the template: `cp .streamlit/secrets.toml.example .streamlit/secrets.toml`
2. Paste the matching values into the `[gcp_service_account]` block, then set `spreadsheet_key`.
3. Keep `private_key` exactly as it appears in the JSON, with the `\n` newline markers intact.

> 🔒 `secrets.toml` is already gitignored. **Never paste credentials into a chat, an issue, or the code.** They belong in `secrets.toml` locally or in the Streamlit Cloud Secrets box.

Run the app again. The sidebar should read **Connected to Google Sheets**, and a `Posts` worksheet is created with the right headers if it does not exist. An empty sheet gets seeded with the full calendar on first load.

### Password gate

Set `app_password` in secrets to put a shared password in front of the app. Leave it out and the app runs open, which is the right setting for local work.

---

## 3. Push to GitHub

```bash
git init
git add .
git commit -m "LCN social media calendar"
git branch -M main
git remote add origin https://github.com/<your-username>/lcn-social-calendar.git
git push -u origin main
```

Your real `secrets.toml` and local `data/posts.csv` stay out of the repo.

---

## 4. Deploy on Streamlit Community Cloud

1. Go to <https://share.streamlit.io/> and sign in with GitHub.
2. **New app**, pick the repo and branch, set the main file to **`app.py`**.
3. Open **Settings**, then **Secrets**, and paste the contents of your `secrets.toml`.
4. Deploy. Because storage is Google Sheets, data persists across restarts and is shared by everyone who opens the app.

---

## Data model

| Field | Notes |
|---|---|
| ID | Auto generated, used internally |
| Date | Publish date. **Blank means benched**, visible in the List view and hidden from the Calendar |
| Time | Optional, for example `08:30` |
| Series | Atomic Essay Tuesday, Burning Budget Thursday, Observance, Competitive Signal, Other |
| Platform | LinkedIn personal, LinkedIn company page, Email nurture, Website insights, Short video, X (Twitter) |
| Persona | The six LCN personas plus All personas |
| Pillar | I Problem First, II Dimensional Insights, III Decision Ready, IV Proven and Validated |
| Title | Short internal label, shown on the calendar |
| Content | The post copy |
| Status | Idea, Draft, In review, Approved, Scheduled, Published, On hold |
| Owner | Who is responsible |
| Link | Published post URL |
| Notes | Compliance flags, placeholders, and sequencing notes |

### Upgrading an existing sheet

This schema adds **Series**, **Persona**, and **Pillar** to the original one. Pointing the app at an older sheet is safe: `_normalize` reindexes onto the canonical columns, so the new fields arrive empty and are written the first time anything saves. Nothing is lost.

---

## Where to edit what

| I want to change | Edit |
|---|---|
| Post copy | `utils/seed_content.py` |
| Which observances exist, their fit rating or caution | `utils/observances.py` |
| Series, personas, pillars, platforms, statuses, colors | the lists at the top of `utils/data_store.py` |
| Which weekday a franchise owns | `SERIES_WEEKDAY` in `utils/data_store.py` |
| Views, filters, cadence checks | `app.py` |
| Theme colors | `.streamlit/config.toml` |
| The logo | replace `assets/logo.png` |

`utils/observances.py` carries into next year with only the dates updated. `suggested_post_date` recomputes the free Monday, Wednesday, or Friday automatically.

---

## Project layout

```
lcn-social-calendar/
├── app.py                        # List, Calendar, and Observances views
├── utils/
│   ├── data_store.py             # Google Sheets and CSV backend, schema, cadence checks
│   ├── seed_content.py           # all drafted post copy
│   └── observances.py            # observance reference calendar with fit ratings
├── assets/logo.png
├── data/                         # local CSV lives here (gitignored)
├── requirements.txt
└── .streamlit/
    ├── config.toml               # LCN theme
    └── secrets.toml.example      # credentials template
```

---

CONFIDENTIAL · INTERNAL USE ONLY · © 2026 LCN Consulting
