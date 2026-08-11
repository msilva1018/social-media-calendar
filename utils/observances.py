"""
Observance reference calendar for LCN Consulting.

Health awareness days and general fun days that LCN can post against, each
carrying a fit rating and a compliance caution. This is a reference list, not
a content plan: the Observances tab in the app lets you review what is coming
and push any of them into the calendar as a draft.

FIT ratings
  Recommended  Strong fit for LCN. Post it.
  Consider     Usable, but the angle has to be right. Read the caution first.
  Avoid        Do not post commercial content. Remembrance days and observances
               where a pharma adjacent firm has nothing appropriate to say.

CATEGORY
  Health       Clinical, professional, or disease awareness observance.
  Fun          Light, human, no business angle required or wanted.
  Remembrance  Days where the correct action is silence on commercial content.

THE STANDING RULE ON DISEASE AWARENESS
Disease awareness observances are the single highest compliance risk on this
list. LCN sells research, not therapies, but a post about a disease can still
read as promotion by proxy, especially where LCN has a live engagement in that
therapeutic area. So the rule is absolute: a disease awareness post is about
the evidence or decision challenge, never about the disease, the treatment,
the outcomes, or any product. If the post cannot be written without touching
one of those, it does not get written.

Dates below are the true observance dates. Where a date lands on a Tuesday, a
Thursday, or a weekend, the app suggests the nearest free Monday, Wednesday,
or Friday so nothing collides with Atomic Essay Tuesday or Burning Budget
Thursday.
"""

from __future__ import annotations

from datetime import date, timedelta

# Days reserved for the two standing franchises (Monday is 0).
RESERVED_WEEKDAYS = {1, 3}  # Tuesday, Thursday

FIT_ORDER = ["Recommended", "Consider", "Avoid"]

# ---------------------------------------------------------------------------
# The list. Edit freely: the app reads this every run.
#   observed  the real date of the observance
#   span      optional text when the observance runs longer than a day
# ---------------------------------------------------------------------------

OBSERVANCES: list[dict] = [
    # ---------------- AUGUST ----------------
    {
        "observed": date(2026, 8, 1),
        "name": "National Immunization Awareness Month",
        "span": "All of August",
        "category": "Health",
        "fit": "Consider",
        "angle": "The decision environment for vaccine portfolios: long horizons, "
                 "shifting recommendation bodies, and public confidence that moves "
                 "faster than evidence can be generated.",
        "caution": "High sensitivity. Write about forecasting and evidence timelines only. "
                   "No product, no schedule guidance, no efficacy or safety language, "
                   "and no position on policy.",
    },
    {
        "observed": date(2026, 8, 1),
        "name": "National Wellness Month",
        "span": "All of August",
        "category": "Fun",
        "fit": "Consider",
        "angle": "Light internal angle: how the team actually works in August. "
                 "Nothing clinical.",
        "caution": "Keep it about working life. Do not offer health advice of any kind.",
    },
    {
        "observed": date(2026, 8, 1),
        "name": "World Lung Cancer Day",
        "category": "Health",
        "fit": "Consider",
        "angle": "One of the most crowded competitive landscapes in oncology, and "
                 "therefore one of the hardest places to read a signal.",
        "caution": "Falls on a Saturday in 2026. Disease awareness rules apply in full. "
                   "Do not post if LCN has a live engagement in this area.",
    },
    {
        "observed": date(2026, 8, 7),
        "name": "National Lighthouse Day",
        "category": "Fun",
        "fit": "Recommended",
        "angle": "A lighthouse has exactly one job and it has not changed in two "
                 "hundred years. Genuinely fun, no business subtext needed.",
        "caution": "None. Friday, so the slot is free.",
    },
    {
        "observed": date(2026, 8, 9),
        "name": "National Book Lovers Day",
        "category": "Fun",
        "fit": "Recommended",
        "angle": "Ask what people have reread rather than what they have read. "
                 "Rereading is the interesting question.",
        "caution": "Falls on a Sunday. Publish Monday August 10. Use a real title.",
    },
    {
        "observed": date(2026, 8, 9),
        "name": "National Health Center Week",
        "span": "August 9 to 15",
        "category": "Health",
        "fit": "Consider",
        "angle": "Community health centers are the access point that most commercial "
                 "models under weight, and a real source of evidence on adoption friction.",
        "caution": "Verify the exact 2026 week before scheduling. No product, no access "
                   "policy positions.",
    },
    {
        "observed": date(2026, 8, 17),
        "name": "National Nonprofit Day",
        "category": "Fun",
        "fit": "Consider",
        "angle": "Patient advocacy organizations as an underused and highly credible "
                 "evidence source, credited properly.",
        "caution": "Do not name a specific organization without permission, and do not "
                   "imply a partnership that does not exist.",
    },
    {
        "observed": date(2026, 8, 19),
        "name": "World Photography Day",
        "category": "Fun",
        "fit": "Consider",
        "angle": "Light. Post a photograph. Wednesday, so the slot is free.",
        "caution": "None.",
    },
    {
        "observed": date(2026, 8, 26),
        "name": "National Dog Day",
        "category": "Fun",
        "fit": "Recommended",
        "angle": "The meeting participants nobody invited. Reliably the highest "
                 "engagement post of any month and carries zero risk.",
        "caution": "None. Wednesday, so the slot is free.",
    },
    {
        "observed": date(2026, 8, 31),
        "name": "International Overdose Awareness Day",
        "category": "Remembrance",
        "fit": "Avoid",
        "angle": "No commercial angle exists that is appropriate here.",
        "caution": "Do not publish commercial content. If LCN posts at all, it is "
                   "acknowledgment only, with no reference to LCN's work, and it should "
                   "be reviewed by someone senior before it goes out.",
    },

    # ---------------- SEPTEMBER ----------------
    {
        "observed": date(2026, 9, 1),
        "name": "Childhood Cancer Awareness Month",
        "span": "All of September",
        "category": "Health",
        "fit": "Avoid",
        "angle": "The evidence base in pediatric oncology is genuinely thinner, which "
                 "is a real and important point about decision making under scarcity.",
        "caution": "Highest sensitivity observance on the calendar. The angle is "
                   "legitimate and the reputational downside of getting the tone wrong "
                   "is severe. Default to not posting. If LCN does post, it needs senior "
                   "sign off and it must never reference LCN's commercial offer.",
    },
    {
        "observed": date(2026, 9, 1),
        "name": "World Alzheimer's Month",
        "span": "All of September, with World Alzheimer's Day on September 21",
        "category": "Health",
        "fit": "Consider",
        "angle": "Long range planning in a therapeutic area where the planning horizon "
                 "outlasts most commercial teams. A real strategic problem.",
        "caution": "No product, no efficacy, no claims about diagnostics. Stay on "
                   "planning horizons and evidence durability.",
    },
    {
        "observed": date(2026, 9, 1),
        "name": "Sepsis Awareness Month",
        "span": "All of September, with World Sepsis Day on September 13",
        "category": "Health",
        "fit": "Consider",
        "angle": "Speed of decision under incomplete information, which is the clinical "
                 "parallel to the commercial problem LCN solves.",
        "caution": "The parallel is elegant and it is also easy to make tasteless. "
                   "Do not compare a business decision to a clinical emergency.",
    },
    {
        "observed": date(2026, 9, 1),
        "name": "Healthy Aging Month",
        "span": "All of September",
        "category": "Health",
        "fit": "Consider",
        "angle": "Demographic shift as the single most predictable variable in long "
                 "range demand modeling, and the one most often left static.",
        "caution": "Keep it demographic and commercial. No health advice.",
    },
    {
        "observed": date(2026, 9, 8),
        "name": "International Literacy Day",
        "category": "Fun",
        "fit": "Consider",
        "angle": "Health literacy as a commercial variable, not a corporate social "
                 "responsibility line.",
        "caution": "Falls on a Tuesday, which is reserved. Publish Wednesday September 9 "
                   "or skip.",
    },
    {
        "observed": date(2026, 9, 11),
        "name": "September 11 remembrance",
        "category": "Remembrance",
        "fit": "Avoid",
        "angle": "None.",
        "caution": "Publish nothing commercial on September 11. Check that no scheduled "
                   "post, nurture email, or automated send lands that day. This is the "
                   "single most important line on this list.",
    },
    {
        "observed": date(2026, 9, 13),
        "name": "World Sepsis Day",
        "category": "Health",
        "fit": "Consider",
        "angle": "See Sepsis Awareness Month.",
        "caution": "Falls on a Sunday. Publish Monday September 14 if at all.",
    },
    {
        "observed": date(2026, 9, 15),
        "name": "World Lymphoma Awareness Day",
        "category": "Health",
        "fit": "Consider",
        "angle": "A landscape reshaped repeatedly inside a single planning cycle, which "
                 "is a real problem for anyone holding a five year forecast.",
        "caution": "Falls on a Tuesday, which is reserved. Disease awareness rules apply "
                   "in full. Do not post if LCN has a live engagement here.",
    },
    {
        "observed": date(2026, 9, 17),
        "name": "World Patient Safety Day",
        "category": "Health",
        "fit": "Recommended",
        "angle": "The strongest health observance fit on the calendar. Patient safety "
                 "conversations concentrate at the point of care, but some decisions that "
                 "shape patient experience get made years earlier by people with no "
                 "clinical training, on evidence of varying quality.",
        "caution": "Falls on a Thursday, which is reserved. Publish Wednesday "
                   "September 16 and reference the day. No product, no efficacy.",
    },
    {
        "observed": date(2026, 9, 18),
        "name": "National Cheeseburger Day",
        "category": "Fun",
        "fit": "Consider",
        "angle": "Low effort, low risk, Friday. Fine as filler if a slot needs one.",
        "caution": "None. Skip it rather than force it.",
    },
    {
        "observed": date(2026, 9, 19),
        "name": "Talk Like a Pirate Day",
        "category": "Fun",
        "fit": "Consider",
        "angle": "Genuinely funny in the right voice and badly wrong in the wrong one.",
        "caution": "Falls on a Saturday. Only worth doing if it is committed to fully. "
                   "A half hearted version reads worse than skipping it.",
    },
    {
        "observed": date(2026, 9, 21),
        "name": "World Alzheimer's Day",
        "category": "Health",
        "fit": "Consider",
        "angle": "See World Alzheimer's Month.",
        "caution": "Monday, so the slot is free. Disease awareness rules apply in full.",
    },
    {
        "observed": date(2026, 9, 22),
        "name": "First day of autumn",
        "category": "Fun",
        "fit": "Recommended",
        "angle": "About a hundred days left in the year, roughly seventy of them working "
                 "days. Sits adjacent to Burning Budget without being a budget post.",
        "caution": "Confirm the exact 2026 equinox date. Falls on a Tuesday, which is "
                   "reserved, so publish Wednesday September 23.",
    },
    {
        "observed": date(2026, 9, 24),
        "name": "National Punctuation Day",
        "category": "Fun",
        "fit": "Consider",
        "angle": "A firm with a documented rule against dashes has an unusually strong "
                 "claim on this one.",
        "caution": "Falls on a Thursday, which is reserved. Publish Friday September 25 "
                   "only if World Pharmacists Day is not used.",
    },
    {
        "observed": date(2026, 9, 25),
        "name": "World Pharmacists Day",
        "category": "Health",
        "fit": "Recommended",
        "angle": "The most consulted and least credited profession in healthcare. "
                 "Frequently the only place a complete medication picture exists in one "
                 "person's head. Dignified, warm, and entirely safe.",
        "caution": "No product, no dispensing guidance, no policy position.",
    },
    {
        "observed": date(2026, 9, 29),
        "name": "National Coffee Day",
        "category": "Fun",
        "fit": "Recommended",
        "angle": "The history is better than the drink. Banned in four jurisdictions and "
                 "still managed to produce Lloyd's of London.",
        "caution": "Falls on a Tuesday, which is reserved. Publish Monday September 28.",
    },
    {
        "observed": date(2026, 9, 29),
        "name": "World Heart Day",
        "category": "Health",
        "fit": "Consider",
        "angle": "Cardiovascular is the reference case for evidence that has to hold "
                 "across decades rather than quarters.",
        "caution": "Falls on a Tuesday, which is reserved, and collides with the closing "
                   "post of the quarter. Skip for 2026.",
    },

    # ---------------- OCTOBER LOOK AHEAD ----------------
    {
        "observed": date(2026, 10, 20),
        "name": "World Statistics Day",
        "category": "Fun",
        "fit": "Recommended",
        "angle": "The best natural fit of the year for LCN and it sits just outside this "
                 "calendar. Start drafting it in September.",
        "caution": "Verify: observed every five years by the United Nations, with wider "
                   "national observances annually. Confirm 2026 status.",
    },
    {
        "observed": date(2026, 10, 1),
        "name": "Breast Cancer Awareness Month",
        "span": "All of October",
        "category": "Health",
        "fit": "Consider",
        "angle": "The most commercially saturated awareness month of the year, which is "
                 "itself the interesting observation.",
        "caution": "Extremely crowded. A generic post adds nothing and reads as "
                   "obligatory. Either say something specific or stay out.",
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def suggested_post_date(observed: date) -> date:
    """Nearest publishable day that does not collide with the two franchises.

    Tuesday and Thursday belong to Atomic Essay and Burning Budget. Weekends are
    skipped. Everything else moves to the closest free Monday, Wednesday, or
    Friday, preferring the day before so the post can reference the observance
    as upcoming rather than past.
    """
    if observed.weekday() <= 4 and observed.weekday() not in RESERVED_WEEKDAYS:
        return observed

    for offset in (-1, 1, -2, 2, -3, 3, -4, 4):
        cand = observed + timedelta(days=offset)
        if cand.weekday() <= 4 and cand.weekday() not in RESERVED_WEEKDAYS:
            return cand
    return observed


def in_window(start: date, end: date) -> list[dict]:
    """Observances whose real date falls inside a window, soonest first."""
    hits = [o for o in OBSERVANCES if start <= o["observed"] <= end]
    return sorted(hits, key=lambda o: (o["observed"], o["name"]))


def upcoming(from_day: date, days: int = 60) -> list[dict]:
    return in_window(from_day, from_day + timedelta(days=days))


def as_rows() -> list[dict]:
    """Flat view for tables, with the suggested publish date resolved."""
    out = []
    for o in sorted(OBSERVANCES, key=lambda x: (x["observed"], x["name"])):
        out.append(
            {
                "Observed": o["observed"],
                "Suggested post date": suggested_post_date(o["observed"]),
                "Observance": o["name"],
                "Runs": o.get("span", "Single day"),
                "Category": o["category"],
                "Fit": o["fit"],
                "Angle": o["angle"],
                "Caution": o["caution"],
            }
        )
    return out
