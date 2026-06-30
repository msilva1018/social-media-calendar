# Social Media Calendar

A Streamlit app for planning social posts, with two views over one shared dataset:

- **📋 List** — an editable table. Edit any cell and the change saves automatically.
- **📅 Calendar** — a month / week view, colour-coded by platform. Click a post for details, or **drag it to a new day** to reschedule (also saved automatically).

It can store everything in a **Google Sheet** (shared, persistent) and shows your logo in the header and sidebar. Out of the box it runs in a local demo mode so you can try it before wiring up Google.

---

## 1. Run it locally

```bash
git clone https://github.com/<your-username>/social-media-calendar.git
cd social-media-calendar
pip install -r requirements.txt
streamlit run app.py
```

It opens at `http://localhost:8501`. On first run it seeds a few example posts so the calendar isn't empty. The sidebar will say **Local demo mode** until you connect Google Sheets (next steps).

> In local mode, data is stored in `data/posts.csv` on your machine. That's fine for trying it out, but for real, shared, durable storage — especially once deployed — use Google Sheets.

---

## 2. Add your logo

Replace the placeholder at **`assets/logo.png`** with your own PNG (a wide/horizontal logo around 640×200 looks best). No code change needed — the app picks it up automatically. If the file is missing the app simply shows the title.

---

## 3. Connect Google Sheets (recommended)

This is what makes "everything saves when I make changes" persist for real and lets your team share one source of truth.

**a. Create a Google Cloud project and enable two APIs**
1. Go to <https://console.cloud.google.com/> and create (or pick) a project.
2. Enable both **Google Sheets API** and **Google Drive API** (APIs & Services → Library).

**b. Create a service account + key**
1. APIs & Services → **Credentials** → *Create credentials* → **Service account**.
2. Open the new service account → **Keys** → *Add key* → **JSON**. A `.json` file downloads. Keep it private.

**c. Create your sheet and share it with the service account**
1. Create a new Google Sheet (any name).
2. Click **Share** and add the service account's email (the `client_email` from the JSON, ends in `…iam.gserviceaccount.com`) as an **Editor**.
3. Copy the sheet's ID from its URL: `https://docs.google.com/spreadsheets/d/`**`THIS_PART`**`/edit`.

**d. Add the credentials to Streamlit secrets**
1. Copy the template: `cp .streamlit/secrets.toml.example .streamlit/secrets.toml`
2. Open `.streamlit/secrets.toml` and paste the matching values from your downloaded JSON into the `[gcp_service_account]` block, then set `spreadsheet_key` to the ID from step c.
3. Keep the `private_key` exactly as in the JSON, with the `\n` newline markers intact.

> 🔒 `secrets.toml` is already in `.gitignore`, so it won't be committed. **Never paste credentials into a chat, an issue, or the code itself** — they only belong in `secrets.toml` (locally) or the Streamlit Cloud Secrets box (below).

Run `streamlit run app.py` again. The sidebar should now show **Connected to Google Sheets**, and a `Posts` worksheet is created automatically with the right headers if it doesn't exist.

---

## 4. Push to GitHub

```bash
git init
git add .
git commit -m "Social media calendar"
git branch -M main
git remote add origin https://github.com/<your-username>/social-media-calendar.git
git push -u origin main
```

(Your real `secrets.toml` and local `data/posts.csv` stay out of the repo thanks to `.gitignore`.)

---

## 5. Deploy on Streamlit Community Cloud

1. Go to <https://share.streamlit.io/> and sign in with GitHub.
2. **New app** → pick your repo and branch, set the main file to **`app.py`**.
3. Open the app's **Settings → Secrets** and paste the entire contents of your `secrets.toml` (the same `[gcp_service_account]` and `[gsheets]` blocks).
4. Deploy. Because storage is Google Sheets, your data persists across restarts and is shared by everyone who opens the app.

---

## Data model

Each post is one row with these fields:

| Field | Notes |
|---|---|
| ID | Auto-generated, used internally |
| Date | Publish date (`YYYY-MM-DD`) |
| Time | Optional, e.g. `09:00` |
| Platform | Instagram, Facebook, X (Twitter), LinkedIn, TikTok, YouTube, Threads, Pinterest |
| Title | Title / campaign name |
| Content | The caption / copy |
| Status | Idea, Draft, Scheduled, Published, On hold |
| Link | Post or media URL |
| Owner | Who's responsible |
| Notes | Anything else |

Platforms and statuses are easy to change — edit the `PLATFORMS` / `STATUSES` lists at the top of `utils/data_store.py`.

## Project layout

```
social-media-calendar/
├── app.py                      # the Streamlit app (List + Calendar views)
├── utils/data_store.py         # Google Sheets / CSV backend + helpers
├── assets/logo.png             # your logo (swap this)
├── data/                       # local CSV lives here (gitignored)
├── requirements.txt
└── .streamlit/
    ├── config.toml             # theme
    └── secrets.toml.example    # credentials template (copy to secrets.toml)
```
