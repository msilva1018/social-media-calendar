"""
Seed content for the LCN social media calendar, August and September 2026.

Two standing franchises plus opportunistic observances:

  Atomic Essay Tuesday     One essay, one idea, one persona, anchored to one
                           positioning pillar. Names the cost of answering a
                           high stakes question from fragmented sources.
                           Method stays invisible. No commercial ask except in
                           the closing post of the quarter.

  Burning Budget Thursday  Q3 and Q4 spend down. One mechanic of the fiscal
                           year close per post, and what it costs. Every post
                           reframes unspent budget as a decision made with less
                           rather than money saved.

  Observance               Health awareness and fun days, published on Monday,
                           Wednesday, or Friday so nothing collides with the
                           two franchises. See utils/observances.py for the
                           reference calendar and the compliance rules.

  Bench                    Undated essays held in reserve. When a Tuesday has
                           to move, pull from here rather than skipping a week.

VOICE RULES, ABSOLUTE
  No dashes of any kind. No em dash, no en dash, no hyphen as a connector.
  Commas, colons, and separate sentences instead. Compound terms phrased so
  they need no hyphen.
  No medical, efficacy, or off label claims about any product.
  No invented statistics, client names, or proof points.
  American spellings.

FLAGGED BEFORE PUBLICATION
  The 34 percent Seton Hall figure in the September 22 essay needs confirming
  against the source study. The supported claim without it is that LCN ranked
  above competitors on accuracy, insight quality, client service, and trust.
  Keep that result separate from the count of more than one hundred brand
  engagements. They measure different things.
  The contact line in the September 29 essay is a placeholder.
"""

from __future__ import annotations

from datetime import date

# Series labels. Must match SERIES in data_store.py.
ESSAY = "Atomic Essay Tuesday"
BUDGET = "Burning Budget Thursday"
OBSERVANCE = "Observance"

LI = "LinkedIn personal"
LI_PAGE = "LinkedIn company page"

# Persona labels. Must match PERSONAS in data_store.py.
P_INSIGHTS = "Insights and Market Research"
P_CI = "Competitive Intelligence"
P_BRAND = "Marketing and Brand"
P_MEDICAL = "Medical Affairs"
P_EXEC = "Senior C Suite"
P_WHITELABEL = "White Label Partners"
P_ALL = "All personas"
P_NONE = ""

# Pillar labels. Must match PILLARS in data_store.py.
PILLAR_1 = "I Problem First"
PILLAR_2 = "II Dimensional Insights"
PILLAR_3 = "III Decision Ready"
PILLAR_4 = "IV Proven and Validated"
PILLAR_NONE = ""


def _post(day, series, platform, persona, pillar, title, body, status="Draft",
          owner="Marketing", notes=""):
    return {
        "Date": day,
        "Time": "08:30",
        "Series": series,
        "Platform": platform,
        "Persona": persona,
        "Pillar": pillar,
        "Title": title,
        "Content": body.strip(),
        "Status": status,
        "Owner": owner,
        "Link": "",
        "Notes": notes,
    }


# ===========================================================================
# ATOMIC ESSAY TUESDAYS
# ===========================================================================

ESSAYS = [
    _post(
        date(2026, 8, 18), ESSAY, LI, P_INSIGHTS, PILLAR_1,
        "The synthesis problem",
        """More research does not produce a better decision. Fragmented research produces a more expensive guess.

Most pharma insights teams do not have a research problem. They have a synthesis problem.

Look at how evidence actually accumulates across a planning year. Qualitative gets commissioned in the spring to explore physician perception. A quantitative wave runs in the summer to size the opportunity. Competitive signals arrive continuously from a separate function on a separate cadence. Analytics builds a forecast off a different base year. Every one of those pieces is competently executed and entirely defensible on its own terms.

Then a brand decision arrives in October and there are six answers that do not agree.

The instinct at that point is to commission more. Another wave, a bridging study, a validation exercise. The instinct is understandable and it makes the problem worse, because volume was never the issue. Each input was designed to answer its own question at the moment it was scoped, not the business question that emerged months later. Adding a seventh input to six that disagree does not resolve the disagreement. It adds a voice to it.

Decision grade insight requires a different starting point. Define the decision first. Determine what evidence that specific decision actually requires. Then integrate the signals against one another rather than reading them side by side and hoping they converge.

What comes out of that sequence is not a set of findings to reconcile. It is one position, with the trade offs named and the confidence level stated openly.

The difference shows up in the room. Findings get discussed. A position gets decided.

When was the last time your research gave you confidence rather than data?""",
        notes="Opens the quarter. Reuse as the first email in the September nurture sequence.",
    ),
    _post(
        date(2026, 9, 1), ESSAY, LI, P_CI, PILLAR_2,
        "Monitoring is not intelligence",
        """Monitoring tells you what happened. Intelligence tells you what to do about it.

Most competitive intelligence functions are drowning in coverage and starved of implication.

The infrastructure usually works. Alerts fire on schedule. Congress readouts land within days. Pipeline trackers refresh. Publication monitoring, conference abstracts, trial registry changes, investor call transcripts, field intelligence from the commercial organization. By any measure of coverage, the function is performing well.

Then a brand lead asks what a competitor move means for next quarter, and the honest answer takes three weeks to assemble.

That gap is not a resourcing failure. It is structural. Monitoring is organized around sources, and each source gets read in isolation by whoever owns it. A trial registry amendment is assessed by the person who reads trial registries. An investor comment is assessed by the person who reads investor calls. Both get logged accurately. Neither gets read against the other, and the meaning lives almost entirely in the relationship between them.

Signal volume is not the constraint. Integration is.

A signal becomes intelligence at a specific moment: when it has been triangulated against every other available input, weighed for what it implies rather than what it states, and carried through to a commercial position someone can act on.

That last step is the one most often skipped, and the reason is worth naming. Reporting what a competitor did carries no professional risk. Stating what it means for your brand carries plenty. The functions that earn a seat in commercial decisions are the ones willing to take the view anyway, and to be explicit about how confident they are when they take it.

How much of your monitoring output ends in a recommendation rather than a summary?""",
        notes="Pair with the next competitive signal one pager if one is in production.",
    ),
    _post(
        None, ESSAY, LI, P_EXEC, PILLAR_3,
        "How confident are we",
        """The question that kills a recommendation is never about the data. It is: how confident are we in this?

Senior leaders are not short of information. They are short of positions they can defend when the room pushes back.

That distinction matters more than it sounds. Findings can be presented, and responsibility stays with whoever produced them. A recommendation has to be owned, and the person who carries it into the room carries it out again regardless of how the discussion goes.

So the useful question about any piece of analysis is not whether it is correct. It is whether it will hold when someone senior, well informed, and appropriately skeptical applies pressure to it.

Three things determine that, and all three happen before the work ever reaches the room.

Whether each finding was corroborated across genuinely independent sources, so a single flawed input cannot carry the conclusion on its own. Whether someone inside the team was assigned to argue against it, deliberately, before it shipped. And whether it resolves into clear implications and stated trade offs rather than a summary that quietly hands the judgment back to the reader.

Work that has cleared those three tests answers a challenge. Work that has not does not become defensible at the moment it is questioned. It becomes exposed, in front of the audience whose confidence you most needed.

The uncomfortable version of this is that most organizations discover the weakness in their evidence at the worst possible moment, then treat that as bad luck rather than as the predictable outcome of never having stress tested it.

When your recommendation gets challenged, what tends to be questioned first?""",
        status="Idea",
        notes="Bench. Strongest opening frame for senior conversations. First choice for any Tuesday that has to move.",
    ),
    _post(
        date(2026, 9, 8), ESSAY, LI, P_BRAND, PILLAR_2,
        "Four vendors, four answers",
        """Four vendors will hand you four answers. The integration work lands on your desk, unbudgeted.

The fragmented model looks efficient on a purchase order. Competitive intelligence from one partner. Qualitative from another. Quantitative from a third. Strategy from a fourth. Each priced separately, each scoped tightly, each competent inside its own boundary.

On paper that is procurement working correctly. Best in class at every line item, no premium paid for breadth nobody asked for.

Now look at what each of those contracts actually obliges the supplier to deliver. Findings, to specification, on time. Not one of them is accountable for whether those findings agree with the other three.

That accountability does not disappear. It transfers, silently, to the client. And it lands on one person, usually in the week before the decision, usually the same person already responsible for presenting the recommendation.

The work involved is substantial and almost entirely invisible. Reconciling conflicting segment definitions. Deciding which of two forecasts to believe when they diverge by twenty percent and both are methodologically sound. Working out whether a qualitative signal contradicts the quantitative read or simply explains it. Judging what to do when the competitive picture implies different sequencing than the demand model.

None of it appears in a scope of work. None of it is budgeted. It gets performed under time pressure by whoever is left holding the decision, and it is the single most consequential piece of analysis in the entire exercise.

The apparent saving in the fragmented model is real. It is just paid for somewhere that never shows up on an invoice.

Who on your team is currently doing the integration nobody scoped?""",
        notes="Strongest single argument against the multiple vendor status quo. Reuse widely.",
    ),
    _post(
        date(2026, 8, 25), ESSAY, LI, P_BRAND, PILLAR_1,
        "The seams in the 2027 plan",
        """Your 2027 brand plan is being built on inputs that were never designed to agree with each other.

Brand planning compresses a year of evidence into a few weeks of decisions. Positioning. Segmentation. Investment allocation. Launch or lifecycle sequencing. Message architecture.

Each of those decisions draws on a different study, commissioned at a different point in the year, by a different team, against a different question, often working from a different definition of the same segment.

None of that is negligence. It is how planning cycles work in every organization. Research gets scoped when a need appears, not when the plan needs it, and the plan arrives long after the scoping decisions were made.

The consequence is predictable and rarely named out loud. By the time the plan reaches review, the weaknesses are not in the data. Every individual input holds up. The weaknesses are in the seams between the inputs.

Where the segmentation from one study does not map cleanly onto the physician typology from another. Where the forecast assumes an adoption curve the qualitative work quietly contradicts. Where the competitive read and the demand model imply different sequencing and nobody has been asked to choose.

Those seams are exactly where a plan gets picked apart. A senior reviewer does not need to challenge your evidence. They only need to notice that two pieces of it point in different directions, and the conversation shifts from strategy to reconciliation for the rest of the meeting.

Nobody was scoped to own the seams. That work lands on one person, in the final week, without a budget line, and it decides how the plan lands.

Which seam in your 2027 plan worries you most right now?""",
        notes="Timing critical. Brand planning season is live now, which is why this moved ahead of the competitive intelligence essay.",
    ),
    _post(
        None, ESSAY, LI, P_INSIGHTS, PILLAR_3,
        "If it cannot be defended it is not finished",
        """If an insight cannot be defended, it is not finished.

Most research is declared complete when the deliverable is delivered. That is a production standard, not a decision standard, and the gap between the two is where most of the value leaks out.

A production standard asks whether the work was executed as scoped. Sample achieved. Fieldwork closed. Analysis run. Report formatted and sent. Each of those is a legitimate check, and passing all of them tells you almost nothing about whether the conclusion will survive contact with a leadership team.

A decision standard asks three harder questions before anything leaves the building.

Has every finding been corroborated across independent sources, or is the conclusion resting on the one input that happened to be most articulate? Has someone inside the team been assigned to argue against it, deliberately, to strip out the bias that accumulates in any group that has lived with the same data for eight weeks? Does the work end in an implication and a named trade off, or does it end in a summary that returns the judgment to the reader?

Work that clears those three tests survives scrutiny. Work that does not gets sent back, usually in front of an audience, and usually with the credibility cost landing on whoever presented rather than on the team that produced it.

The tests are not expensive. They take days rather than weeks, and they sit entirely within the control of the team doing the work.

The reason they get skipped is that they are uncomfortable, and the discomfort arrives well before the benefit does.

What would change if nothing left your team until it had been argued against internally?""",
        status="Idea",
        notes="Bench. Pairs naturally after the September 1 essay if a slot opens.",
    ),
    _post(
        date(2026, 9, 15), ESSAY, LI, P_MEDICAL, PILLAR_3,
        "Rigor the enterprise never uses",
        """Rigor that stays inside medical affairs is rigor the enterprise never gets to use.

Medical affairs generates some of the most defensible evidence in a pharmaceutical organization, and often holds the least influence over how commercial decisions actually get made.

That is not a credibility problem. Nobody doubts the rigor. It is a translation problem, and it is structural rather than cultural.

Medical evidence is produced to a standard that prioritizes accuracy, appropriate caveats, and honest uncertainty. That standard is correct and not negotiable. It also produces outputs a commercial audience finds difficult to act on, because the caveats that make the work honest are the same caveats that make it ambiguous to someone who needs a direction rather than a range.

So one of two things happens.

Either the evidence gets simplified downstream by someone who does not fully understand what they are flattening, and the nuance that mattered most is the first thing lost. Or it does not travel at all, and the commercial decision proceeds without it, informed instead by whatever evidence was easier to consume.

Both outcomes are worse than the alternative, and the alternative requires somebody to do genuinely difficult work: carry scientific evidence across functions intact, preserving the uncertainty that is real while still resolving to an implication a commercial leader can act on.

That work sits between teams, which in most organizations means it belongs to nobody, which means it does not happen. The evidence stays technically accurate, entirely credible, and largely uninfluential.

The functions that break out of this pattern are the ones that stop waiting to be asked and start delivering the implication alongside the evidence.

When commercial decisions get made in your organization, is your evidence in the room or in a footnote?""",
        notes="Reaches the one persona competitors rarely address. Very little competition for attention.",
    ),
    _post(
        date(2026, 9, 22), ESSAY, LI, P_EXEC, PILLAR_4,
        "We did not write the questions",
        """We did not write the questions. Seton Hall University did.

Claiming quality is easy. Every firm in this category does it, in similar language, and none of it is verifiable by a buyer at the point where verification would matter.

Submitting to independent measurement is a different proposition.

Researchers at Seton Hall University asked pharma decision makers to rank LCN against competitors on the attributes buyers actually weigh when choosing an insights partner: accuracy, insight quality, client service, and trust. We did not design the instrument, select the respondents, or see the results before they existed. LCN ranked above competitors on every attribute measured, an average advantage of 34 percent.

Two details matter more than the headline.

The respondents were not concentrated in one function. They spanned market research, insights, competitive intelligence, marketing, and medical affairs. That means the result is not an artifact of one type of buyer who happens to like how we work. It held across the seats that sit around an enterprise decision, which is the only version of the finding worth anything to a leadership team weighing a partner.

And the attributes were not ours to choose. Accuracy and trust are uncomfortable things to be measured on, because they are the two a client can verify from direct experience and the two that most partner relationships quietly fail on.

We name the source plainly, and we accept the constraint that comes with it. Independence is what gives a finding weight, and a firm that cites independent research forfeits the ability to describe itself in whatever terms it would prefer.

What would your current partners score if their clients were asked the same questions?""",
        status="On hold",
        notes="BLOCKING: confirm the 34 percent figure, the study year, and the sample before "
              "publishing. If it cannot be confirmed, cut that clause and run the ranking claim "
              "alone, which is fully supported. Placed one week before the close so proof lands "
              "before the ask.",
    ),
    _post(
        date(2026, 9, 29), ESSAY, LI, P_ALL, "I and III",
        "One decision. Thirty minutes.",
        """One decision. Thirty minutes. Before the year closes.

This is the direct version, and it is the only post this quarter that asks for anything.

Pharma leaders spend the fourth quarter making commitments that will be judged all through the following year. Positioning that will hold or fail at launch. Investment allocation that cannot be meaningfully revisited until the next planning cycle. Competitive posture set against moves that have not been confirmed yet.

Most of those commitments get made while reconciling inputs that were never built to agree with each other, under time pressure, by someone who will still be accountable in eighteen months when the context that produced the decision has been forgotten.

We have spent two months describing that problem because we solve it, and because describing it accurately is the fastest way for you to establish whether we are useful to you.

So here is the ask, and it is deliberately small.

Pick the single decision you most need to get right in the first half of 2027. Bring it to a thirty minute conversation. We will show you exactly how we would turn it into one answer your leadership can stand behind: what evidence that specific decision requires, how the signals get integrated rather than compared, and how the conclusion gets pressure tested before it reaches a room where it matters.

You will leave knowing whether it is worth going further. No proposal, no capabilities overview, and no follow up sequence if the answer is no.

Thirty minutes. One decision. Before the year closes.

If that is worth the time, send a note this week. [Contact placeholder: confirm address and title]""",
        status="On hold",
        notes="The single explicit ask of the quarter. Everything published before this earns the "
              "right to make it. Confirm the contact line and external title before scheduling.",
    ),
]


# ===========================================================================
# BURNING BUDGET THURSDAYS
# ===========================================================================

BUDGET_POSTS = [
    _post(
        date(2026, 8, 20), BUDGET, LI, P_EXEC, PILLAR_3,
        "Unspent budget is not savings",
        """Unspent budget is not savings. It is a decision you have chosen to make with less.

Every year, money approved specifically to reduce decision risk expires unused. The decisions it was meant to support get made anyway, on thinner evidence, by people who remain fully accountable for the outcome.

The cause is almost never negligence. It is a timing mismatch that nobody owns.

Budget gets approved annually. Decisions arrive continuously. By the third quarter, the remaining amount is too small to fund a full program and the calendar is too compressed to run a long one, so it sits. Meanwhile the decisions it was intended to underwrite keep arriving, and each one gets made with whatever evidence happens to be available rather than the evidence it warranted.

At that point something quietly shifts. The risk moves off the budget line and onto the decision maker. It does not get smaller. It stops being visible in any system that reports on it.

This is worth being precise about, because it gets treated as an administrative footnote when it is a governance issue. An organization that returns research budget while making high stakes commitments on incomplete evidence has not saved money. It has converted a funded, managed risk into an unfunded, unmanaged one, and it has done so without anyone actually deciding to.

The remedy is not to spend the money. It is to name the decisions in the next two quarters that are currently underwritten by less evidence than they deserve, then fund the one or two where that gap is least acceptable.

That is a twenty minute exercise with a leadership team. Most organizations never run it.

Which decision on your desk in the next two quarters is currently underwritten by less evidence than it deserves?""",
        notes="Opens the franchise. Sets the frame every subsequent Thursday builds on.",
    ),
    _post(
        None, BUDGET, LI, P_INSIGHTS, PILLAR_1,
        "Twenty weeks left",
        """There are about twenty weeks left in the year. Each one is a chance to turn remaining budget into a decision you can defend.

Fourth quarter is when unspent research budget stops being a finance question and becomes a strategy question.

The mechanics are familiar to anyone who has managed an insights budget. Money was approved in a planning cycle against needs that were partly hypothetical. Some of those needs never materialized. Others got absorbed by a partner already under contract. What remains is an amount too small for a full program, sitting against a calendar too short for a long one, with a deadline attached that has nothing to do with when decisions are due.

The default response is volume. Another tracker wave. A refresh of a study that did not change much. A landscape report that will arrive in February, after the decision it was scoped to inform has already been made.

That spends the budget. It does not reduce any risk, and everyone involved knows it at the time.

The better use of a small remaining budget is narrower than the instinct suggests. Identify the single decision that has to be right in the first half of next year. Not the largest project or the most interesting question. The one decision where being wrong is most expensive and where the current evidence base is thinnest.

Then commission the answer to that one question. Scoped to arrive before the decision rather than before the fiscal year closes, and built to survive the review it will face when it gets there.

One narrow, defensible answer delivered in time is worth more than three broad reports delivered late.

If you had one study left this year, which decision would you point it at?""",
        status="Idea",
        notes="Bench. RECOUNT THE WEEKS before publishing. The number in the first line must match the actual publish date, and it overlaps thematically with the franchise opener.",
    ),
    _post(
        date(2026, 8, 27), BUDGET, LI, P_BRAND, PILLAR_1,
        "October approval, September evidence",
        """Brand plans get approved in October. The evidence that decides them is being commissioned right now.

The sequencing is unforgiving, and it is arithmetic rather than opinion.

Approval dates are fixed. They sit in a governance calendar that was set months ago and will not move to accommodate a research timeline. Evidence timelines are not fixed, but they have floors. Fielding takes what fielding takes. Synthesis takes longer than most plans assume. Pressure testing a conclusion properly adds time at the end rather than the beginning.

Run that arithmetic backwards from an October approval and the window becomes obvious. Work commissioned in early to mid September arrives in time to shape what the plan says. Work commissioned in late October arrives in time to explain what the plan already says.

Those two outcomes cost roughly the same and are worth entirely different amounts.

This is the narrow period where a brand team still holds genuine optionality. Positioning can still change. Segment prioritization can still change. Investment allocation across the portfolio can still change, because none of it has been socialized to the point where changing it costs political capital.

Two weeks later, all of that hardens. Not because the evidence improved, but because the plan got circulated, and a circulated plan defends itself.

The window closes quietly. There is no notification. Most teams identify it accurately in hindsight, in January, when a question that could have been answered in September becomes the reason a plan gets reopened mid year.

What is the one question your 2027 plan still cannot answer?""",
        notes="Time critical. If this post slips past early September the argument weakens.",
    ),
    _post(
        date(2026, 9, 3), BUDGET, LI, P_INSIGHTS, PILLAR_1,
        "The real deadline is procurement",
        """The deadline for spending this year's budget is not December 31. It is whenever your procurement cycle takes.

Every insights team working on a fourth quarter commitment is working from the wrong date.

The mental deadline is the fiscal year end. The real deadline is the fiscal year end minus the time it takes to get a statement of work through legal, vendor onboarding, purchase order issuance, and whatever internal approval threshold the amount happens to trigger.

For a supplier who is not already onboarded at a large pharma organization, that sequence is measured in weeks rather than days. Vendor registration alone can take three. Legal review of a master services agreement takes longer than anyone plans for, and it does not accelerate because a budget is expiring.

Run it backwards. If procurement takes six weeks and the work takes eight, a January delivery requires a decision in early October, not late November.

Which means the practical window for committing this year's remaining budget closes several weeks before the calendar suggests, and it closes earliest for exactly the partners you have never used before.

Two things follow. Decide now which decisions you are funding, rather than in November once the final amount is confirmed. And if the answer involves a supplier who is not already in your system, start the paperwork in parallel with the scoping conversation rather than after it.

The budget does not care that the process was slow.

How many weeks does a new supplier take to get through your procurement process?""",
        notes="Operationally useful, which makes it the most internally shareable post in the "
              "franchise. Also quietly reduces the friction on our own onboarding.",
    ),
    _post(
        date(2026, 9, 10), BUDGET, LI, P_EXEC, PILLAR_3,
        "Assume it does not carry over",
        """Assume the budget does not carry over. It almost never does, and planning as though it might is how it gets lost.

Every year some portion of approved research budget goes unspent on the assumption that it will still be there in January. Occasionally that is true. Usually it is not, and the reasons are structural rather than punitive.

Finance treats an underspend as evidence the original amount was too high. Next year's allocation gets set against actual spend rather than approved spend, which means an unspent quarter this year quietly becomes a smaller number next year. The team that showed restraint gets less to work with. The team that spent everything gets its allocation defended.

That is a perverse incentive and everyone involved knows it. It is also how most budgeting cycles behave in practice.

The correct response is not to spend indiscriminately in December, which produces exactly the low value work that makes the underspend look justified in retrospect. It is to identify, now, which decisions in the next two quarters are genuinely underfunded, and to commit against those while the money still exists.

That requires a conversation most organizations put off until the remaining amount is small enough to be embarrassing.

The honest version of the question is not what should we spend this on. It is which decision are we currently planning to make with less evidence than it deserves, and whether that is acceptable.

Does unspent research budget carry over in your organization, or does it quietly reset the baseline?""",
        notes="World Suicide Prevention Day falls on this date. This post is neutral and commercial, which is fine, but read it once before scheduling. Also confirm nothing in the nurture sequence lands on September 11.",
    ),
    _post(
        None, BUDGET, LI, P_BRAND, PILLAR_1,
        "The fourth quarter dollar is worth more",
        """The same dollar buys more decision confidence in the fourth quarter than it does in the first. Most teams treat it as worth less.

There is a reason fourth quarter research has a poor reputation, and it is not the timing. It is that fourth quarter research is usually scoped badly.

Consider what is actually different about commissioning work in September versus March.

In March the question is broad, because the decision is far away. You do not yet know which of four scenarios you are planning for, so the brief covers all of them and the output is necessarily general. That is not waste. It is the cost of buying information early.

In September the decision is close and the question has narrowed. You know what you are deciding, when you are deciding it, who will challenge it, and which specific unknown will get challenged first. A brief written from that position is dramatically tighter, and a tighter brief produces a more useful answer for less money.

So the same dollar is worth more, not less.

The reason it does not feel that way is that fourth quarter briefs get written under time pressure by someone trying to spend an amount rather than answer a question. The amount leads the brief instead of the other way round, and the output is broad because the brief was.

Start from the decision. The budget will follow it far more efficiently than the reverse.

Is your remaining budget looking for a question, or is your question looking for a budget?""",
        status="Idea",
        notes="Bench. Strongest reframe in the franchise and the closing line is the best of the set. First choice for any Thursday that has to move.",
    ),
    _post(
        date(2026, 9, 17), BUDGET, LI, P_INSIGHTS, PILLAR_2,
        "Three uses for an awkward amount",
        """If the remaining amount is too small for a full program, here are the three things worth doing with it, in order.

The most common fourth quarter problem is not a lack of budget. It is an amount that does not fit anything on the standard menu.

Too small for a segmentation study. Too small for a full competitive assessment. Large enough that returning it looks like poor planning. So it gets spent on a tracker extension or a landscape refresh, neither of which changes a decision.

Three better uses, ranked.

First, buy an answer to one narrow question that a decision in the next two quarters actually turns on. Not a broad update. One question, scoped tightly enough that the answer arrives in weeks and is specific enough to act on. This is almost always the highest return option and it is the one most often skipped, because narrow briefs feel like they are underusing the money.

Second, buy integration of evidence you already own. Most organizations are sitting on studies commissioned separately that have never been read against each other. Reconciling them into one position is faster and cheaper than generating anything new, and it addresses the problem that actually causes trouble in review.

Third, buy a pressure test. Take the recommendation you already intend to make and have it challenged properly before it reaches leadership.

The worst use is volume. It spends the money and changes nothing.

Which of those three would help you most before the year closes?""",
        notes="Maps directly to what LCN sells without naming a service. Strongest conversion "
              "candidate in the franchise.",
    ),
    _post(
        date(2026, 9, 24), BUDGET, LI, P_ALL, PILLAR_3,
        "The last week that lands this year",
        """This is the last week where work commissioned this year can still land before the year closes.

The arithmetic is simple and unsentimental.

Scope a piece of work in the final week of September and it can be contracted in October, fielded through November, and delivered in December. Scope it in mid October and it delivers in the first quarter of next year, which is fine if the decision is in the first quarter and useless if the decision is in December.

That is the entire content of this post. Not a strategy. A date.

Everything we have published on Thursdays this quarter has pointed at the same underlying thing. Budget approved to reduce risk expires unused. The decisions it was meant to support get made anyway. The risk does not disappear, it just stops being funded and starts being personal.

There is still time to change that this year. There is not very much of it, and the amount reduces by a week every week.

So the practical version. Take fifteen minutes this week. Write down the two decisions in the next two quarters where you are least comfortable with the evidence. Establish what it would cost to fix the more expensive of the two. Then decide whether returning that money is genuinely the better option.

It might be. But it should be a decision rather than a default.

Which two decisions made your list?""",
        notes="Closes the Burning Budget franchise and sets up the September 29 ask.",
    ),
]


# ===========================================================================
# OBSERVANCES
# Published Monday, Wednesday, or Friday so nothing collides with the
# two franchises. See utils/observances.py for the reference calendar.
# ===========================================================================

OBSERVANCE_POSTS = [
    _post(
        None, OBSERVANCE, LI_PAGE, P_NONE, PILLAR_NONE,
        "National Immunization Awareness Month opener",
        """ANGLE, NOT YET DRAFTED. National Immunization Awareness Month runs all of August.

The only defensible LCN angle is the decision environment: long planning horizons, recommendation bodies that shift, and public confidence that moves faster than evidence can be generated. That is a genuine forecasting and evidence timeline problem and it is ours to talk about.

Write nothing about any vaccine, any schedule, any efficacy or safety finding, or any policy position. If the post cannot be written without touching one of those, it does not get written.""",
        status="Idea",
        notes="The 2026 month opener window has passed. Runs all of August annually. High sensitivity, so decide whether to run it at all before drafting.",
    ),
    _post(
        None, OBSERVANCE, LI, P_NONE, PILLAR_NONE,
        "National Lighthouse Day",
        """It is National Lighthouse Day, which is a strange thing to celebrate until you think about what a lighthouse actually does.

It does not tell you where to go. It does not tell you how fast to travel or what cargo to carry. It has exactly one job, performed the same way every night for two centuries: it tells you where the rocks are.

There are more than seven hundred lighthouses still standing in the United States and most have been automated for decades. The keepers are gone. The light still turns.

The part I find remarkable is how little the design needed to change. A Fresnel lens from the 1820s, a stack of concentric glass rings, could throw a single flame's light more than twenty miles out to sea. Some of those original lenses are still in service. Two centuries of technological progress and nobody improved on the geometry.

Happy National Lighthouse Day to everyone who has ever climbed one on holiday and pretended the view was the reason.

What is the best one you have been to?""",
        status="Idea",
        notes="August 7 annually, so the 2026 date has passed. Copy is drafted and ready for next year. Verify the count of surviving US lighthouses before publishing.",
    ),
    _post(
        None, OBSERVANCE, LI, P_NONE, PILLAR_NONE,
        "National Book Lovers Day",
        """It was National Book Lovers Day yesterday, so here is a better question than a reading list: what is a book you have actually reread?

Rereading is the real test. Anyone can finish something once. Going back means it changed how you look at things and you wanted to check whether it still worked.

[PLACEHOLDER: name a real title and say something true about it. Three sentences. What the first read felt like, what the second read revealed, and what you noticed the third time. Do not use a book you have not read, because someone will ask.]

There is a version of this post that turns into a business point. I am going to resist it.

What is yours? Not the best book you have read. The one you went back to.""",
        status="Idea",
        notes="August 9 annually, so the 2026 date has passed. Held for next year. Needs a real title from whoever posts it.",
    ),
    _post(
        None, OBSERVANCE, LI_PAGE, P_NONE, PILLAR_NONE,
        "National Health Center Week",
        """ANGLE, NOT YET DRAFTED. National Health Center Week runs the week of August 9.

Community health centers are the access point most commercial models under weight, and a real source of evidence on adoption friction that never appears in a specialist sample.

That is a legitimate and slightly unexpected point about where evidence comes from. No product, no access policy position, no comment on funding.""",
        status="Idea",
        notes="The 2026 week has passed. Runs in early to mid August annually. Verify the exact week before scheduling next year.",
    ),
    _post(
        date(2026, 8, 17), OBSERVANCE, LI, P_NONE, PILLAR_NONE,
        "National Nonprofit Day",
        """ANGLE, NOT YET DRAFTED. National Nonprofit Day.

Patient advocacy organizations are one of the most credible and least systematically used evidence sources in commercial pharma research. They hold longitudinal understanding of lived experience that no eight week study reproduces.

Credit them properly and make no claim about any specific organization. Do not name one without permission and do not imply a partnership that does not exist.""",
        status="Idea",
        notes="Monday August 17, the first day of the new cadence. Good angle and low risk, but it is undrafted, so treat it as optional rather than a commitment.",
    ),
    _post(
        date(2026, 8, 26), OBSERVANCE, LI, P_NONE, PILLAR_NONE,
        "National Dog Day",
        """It is National Dog Day, which in a company that works across time zones means the meeting participants nobody invited finally get their moment.

[PLACEHOLDER: one real dog, one real detail. The dog who appears in every call. The one who has learned that walking across a keyboard produces attention faster than any other available strategy. Keep it specific, because specific is what makes it funny.]

The thing about dogs on video calls is that they are the only participant who is definitely not performing. Everyone else on the grid is managing a face. The dog is looking for a warm spot and has correctly identified the laptop.

Post your coworkers. The ones with four legs.""",
        notes="Reliably the highest engagement post of any month and carries no risk. Needs one "
              "real dog and one real detail.",
    ),
    _post(
        date(2026, 8, 31), OBSERVANCE, LI_PAGE, P_NONE, PILLAR_NONE,
        "International Overdose Awareness Day",
        """DO NOT PUBLISH COMMERCIAL CONTENT.

International Overdose Awareness Day. There is no commercial angle here that is appropriate.

If LCN posts at all it is acknowledgment only, with no reference to our work, our capabilities, or our positioning, and it should be reviewed by someone senior before it goes out. Not posting is a completely acceptable answer.""",
        status="On hold",
        notes="Held deliberately. Decide, do not default.",
    ),
    _post(
        date(2026, 9, 2), OBSERVANCE, LI_PAGE, P_NONE, PILLAR_NONE,
        "Childhood Cancer Awareness Month",
        """DEFAULT TO NOT POSTING.

Childhood Cancer Awareness Month runs all of September and it is the highest sensitivity observance on this calendar.

There is a legitimate angle. The evidence base in pediatric oncology is genuinely thinner, and decision making under real scarcity of evidence is a subject LCN understands. That angle is defensible.

The reputational downside of getting the tone even slightly wrong is severe, and there is no version of this post that should mention what LCN sells. If it runs, it needs senior sign off first.""",
        status="On hold",
        notes="Held deliberately. The angle is real. The risk is real. Someone senior decides.",
    ),
    _post(
        date(2026, 9, 4), OBSERVANCE, LI_PAGE, P_NONE, PILLAR_NONE,
        "World Alzheimer's Month opener",
        """ANGLE, NOT YET DRAFTED. World Alzheimer's Month runs all of September, with World Alzheimer's Day on September 21.

The LCN angle is planning horizon. This is a therapeutic area where the commercial planning horizon regularly outlasts the tenure of the team doing the planning, which makes evidence durability a first order problem rather than a technical footnote.

No product, no efficacy, no claims about diagnostics. Stay entirely on planning horizons and how evidence ages.""",
        status="Idea",
        notes="Strong angle. Decide whether to run it on the month opener or on September 21.",
    ),
    _post(
        date(2026, 9, 11), OBSERVANCE, LI_PAGE, P_NONE, PILLAR_NONE,
        "September 11 remembrance: publish nothing",
        """PUBLISH NOTHING COMMERCIAL ON SEPTEMBER 11.

This row exists so the date is visible in the calendar rather than discovered by accident.

Before this week, check three things. No scheduled LinkedIn post lands on September 11. No nurture email is queued to send. No automated sequence fires that day.

This is the single most important line in the observance calendar.""",
        status="On hold",
        notes="Blocking check, not a post. Do not delete this row.",
    ),
    _post(
        date(2026, 9, 14), OBSERVANCE, LI_PAGE, P_NONE, PILLAR_NONE,
        "World Sepsis Day",
        """ANGLE, NOT YET DRAFTED. World Sepsis Day is Sunday September 13, so this would publish Monday.

There is a clinical parallel available here about speed of decision under incomplete information, and it is elegant, and it is also very easy to make tasteless.

Do not compare a commercial decision to a clinical emergency. If the post cannot avoid that comparison, skip the day.""",
        status="Idea",
        notes="Skip rather than force it. The parallel is tempting and the tone risk is real.",
    ),
    _post(
        date(2026, 9, 16), OBSERVANCE, LI, P_NONE, PILLAR_NONE,
        "World Patient Safety Day",
        """World Patient Safety Day is tomorrow, and the framing that gets the least attention is the one furthest upstream.

Most conversations about patient safety concentrate on the point of care: protocols, checklists, handoffs, dosing systems. That work is essential and it is where the majority of preventable harm gets caught.

But some of the decisions that shape patient experience get made years earlier, in rooms with no clinical staff in them. Which populations a trial recruits. How a therapy gets positioned to physicians who have very little time to make a choice. Which unmet need gets prioritized when a portfolio cannot fund everything.

Those are commercial and strategic decisions. They are also decisions with a downstream clinical consequence, and they get made on evidence of wildly varying quality.

Nobody in those rooms is thinking about patient safety. That is exactly why the quality of the evidence in front of them matters.

World Patient Safety Day is September 17.""",
        notes="Strongest health observance fit on the calendar. Dignified, no product, no efficacy "
              "claim, and it lands LCN's actual thesis without pitching.",
    ),
    _post(
        date(2026, 9, 18), OBSERVANCE, LI, P_NONE, PILLAR_NONE,
        "National Cheeseburger Day",
        """OPTIONAL FILLER. National Cheeseburger Day, Friday.

Low effort, low risk, no angle required. Worth using only if a Friday slot needs filling and nothing better is available.

Skip it rather than force it.""",
        status="Idea",
        notes="Lowest priority row on the calendar. Delete if the month is already full.",
    ),
    _post(
        date(2026, 9, 21), OBSERVANCE, LI_PAGE, P_NONE, PILLAR_NONE,
        "World Alzheimer's Day",
        """ANGLE, NOT YET DRAFTED. World Alzheimer's Day, Monday September 21. Also International Day of Peace.

If the month opener on September 4 ran, this is the follow through. If it did not, this is the better of the two dates because the day carries more attention than the month.

Same rules. Planning horizons and evidence durability only. No product, no efficacy, no diagnostics.""",
        status="Idea",
        notes="Pick either September 4 or September 21, not both.",
    ),
    _post(
        date(2026, 9, 23), OBSERVANCE, LI, P_NONE, PILLAR_NONE,
        "First day of autumn",
        """Autumn is here, which means there are about a hundred days left in the year.

That is the number worth sitting with. Not "the fourth quarter," which sounds like a phase with room in it. About a hundred days, of which roughly seventy are working days once the weekends and the holidays at the end come out.

Seventy working days to close everything you told someone in January you would close.

I am not going to pretend that is motivating. Mostly it is clarifying. There is a real difference between a list of things you intend to do and a list of things that fit inside seventy days, and September is when those two lists stop resembling each other.

Happy autumn. Go outside before it gets cold.""",
        notes="Sits adjacent to Burning Budget without being a budget post, which is why it works "
              "on a Wednesday. Confirm the 2026 equinox date.",
    ),
    _post(
        date(2026, 9, 25), OBSERVANCE, LI, P_NONE, PILLAR_NONE,
        "World Pharmacists Day",
        """It is World Pharmacists Day, and pharmacists are the most consulted and least credited professionals in healthcare.

Consider the asymmetry. A patient sees a physician by appointment, for a length of time measured in minutes. They see a pharmacist without an appointment, repeatedly, often monthly for years, at the counter of a building they can walk into. The pharmacist knows every medication that patient is taking, including the ones prescribed by someone who did not know about the others.

That last part is not a small thing. It is frequently the only place in the entire system where a complete medication picture exists in one person's head.

They also field the questions people are too embarrassed to ask a physician, absorb the frustration when a plan denies something they did not decide, and do all of it standing up.

To every pharmacist reading this, thank you. Especially the ones who caught something.""",
        notes="Warm, dignified, entirely safe. No product, no dispensing guidance, no policy "
              "position.",
    ),
    _post(
        date(2026, 9, 28), OBSERVANCE, LI, P_NONE, PILLAR_NONE,
        "National Coffee Day",
        """National Coffee Day is tomorrow, and the history is considerably better than the drink.

Coffee reached Europe in the 1600s and was immediately controversial. It was banned in Mecca. It was banned in Constantinople. It was denounced in England in a 1674 pamphlet written by women complaining that it had rendered their husbands useless. And it was outlawed in Sweden along with the cups and the saucers, which strikes me as the most thorough prohibition on the list.

The reason it survived all of that is not taste. It is that coffee houses turned out to be where things happened. Lloyd's of London began in one. So did the London Stock Exchange. People sat down for something to drink and accidentally invented insurance.

[PLACEHOLDER: how many cups, and one honest admission about having no interesting opinions on beans.]

How do you take yours?""",
        notes="Actual day is Tuesday September 29, which is reserved, so this publishes Monday. "
              "Verify the Swedish ban and the Lloyd's origin before publishing. Both are widely "
              "documented but worth a check.",
    ),
]


# ===========================================================================
# BENCH
# Undated essays held in reserve. When a Tuesday has to move, pull from here
# rather than skipping a week. Undated rows appear in the List view and are
# hidden from the Calendar until a date is set.
# ===========================================================================

BENCH = [
    _post(
        None, ESSAY, LI, P_CI, PILLAR_1,
        "By the time it is confirmed",
        """By the time a competitor's move is confirmed, the window to respond has usually closed.

Confirmation is comfortable. It is also late.

The commercial value of a competitive signal peaks well before certainty, at the point where it is still a pattern rather than a fact. A pipeline reprioritization that surfaces as a quiet trial registry amendment, a hiring pattern in one therapeutic area, and a shift in congress presence is readable months before anyone announces anything. By the time there is a press release, your options have narrowed to reaction.

Everyone in competitive intelligence knows this. Most organizations still wait, and the reason deserves to be said plainly.

Acting on patterns means stating a position on incomplete evidence, and most reporting structures punish exactly that. A confirmed fact carries no professional risk. A probabilistic read that turns out wrong carries a great deal, even when the expected value of making it was clearly positive. So the incentive quietly favors silence until certainty, which is precisely the moment the information stops being useful.

Getting past that requires two things.

A method for weighing incomplete signals against each other rather than assessing each in isolation, so three weak indicators pointing the same direction get treated as what they are. And the discipline to state the confidence level openly rather than burying it, so a recommendation can be acted on proportionally instead of being accepted whole or dismissed whole.

Waiting for certainty is a decision too. It is simply an expensive one, made by default, and it never appears in any review, because nobody records the option that quietly expired.

What is the last competitive move your team saw coming and could not act on in time?""",
        status="Idea",
        notes="Bench. Best used alongside a live competitive signal one pager.",
    ),
    _post(
        None, ESSAY, LI, P_CI, PILLAR_2,
        "Their fourth quarter is decided, yours is not",
        """Your competitors' fourth quarter moves are already decided. Yours are still open.

That asymmetry is the entire opportunity, and it lasts weeks rather than months.

Competitive plans set over the summer are already in motion. Launch sequencing. Access and contracting strategy. Congress positioning for the autumn cycle. Field deployment and territory changes. Medical education investment. Those decisions have been made, the budgets are committed, and execution has begun.

Execution leaves traces. Field structures change and the changes are visible. Congress programs get published. Contracting posture shifts in ways account teams notice long before anyone reports it. Hiring patterns reveal where capability is being built. Trial registry amendments reveal what is being deprioritized.

None of those traces is a disclosure. All of them are observable now.

The catch is that they sit across sources that were never designed to be read together, owned by different functions, on different reporting cadences, in different formats.

Read separately they are noise, and each individual signal is easy to dismiss on its own merits. Read against one another they resolve into a pattern, and the pattern is usually unambiguous well before any of its components is conclusive.

Timing is what makes this valuable rather than merely interesting. A pattern identified in September is actionable, because your own fourth quarter and first quarter commitments are still open. The identical pattern confirmed in January is history. Same information, same analytical quality, a fraction of the commercial value.

What would you do differently in the fourth quarter if you knew where your two closest competitors were placing their bets?""",
        status="Idea",
        notes="Bench. Time sensitive. Loses force after early October.",
    ),
    _post(
        None, ESSAY, LI, P_EXEC, PILLAR_4,
        "Consistency is a system",
        """Consistency across more than one hundred brand engagements is not talent. It is a system.

Any firm can point to one exceptional project. Ask about it and you will usually hear a story about a particular team, a particular relationship, and a particular set of circumstances that came together well.

That story is often true. It is also the wrong thing to buy on, because none of it constitutes a commitment about the next engagement.

The harder claim, and the only one that matters to an enterprise buyer, is that the next one will be just as good. Different team. Different brand. Different therapeutic area. Different deadline, probably a worse one. No shared history with the client, and none of the benefit of the relationship that made the last one work.

That claim only holds when quality is engineered rather than assumed.

It means the same governed process determines what evidence a question requires, so the answer does not depend on which individual happened to scope it. The same internal challenge runs before anything ships, so nothing reaches a client on the strength of one person's confidence. And the same standard applies whether the client is a top 20 pharma with a global remit or an early stage biopharma with one asset and a board to convince.

LCN has operated this way since 2006, across more than one hundred brand engagements. The number matters less than what it demonstrates: output quality that does not vary with staffing, and does not require the client to manage for it.

How much of your current partner's quality depends on which individuals happen to be assigned?""",
        status="Idea",
        notes="Bench. Keep this proof point separate from the Seton Hall result. They measure "
              "different things and conflating them weakens both.",
    ),
    _post(
        None, ESSAY, LI, P_WHITELABEL, PILLAR_2,
        "Saying no to the one question",
        """The fastest way to lose an account is to say no to the one question you cannot answer.

Agencies and consultancies lose ground less often to competitors than to scope.

The pattern is consistent. A client relationship is strong. Delivery is good. Then a question arrives that sits just outside the core: real competitive depth on a new entrant, a quantitative read to support a positioning decision, a strategic recommendation that has to be pressure tested before it reaches a brand team.

The honest answer is that it is not what you do.

Saying so is professional, and it is also expensive, because it does two things at once. It signals a ceiling on the relationship, and it creates a reason for the client to bring in someone else. That someone else now has a foothold, a direct relationship, and first position on the next question of the same type.

Building the capability internally is the obvious response and rarely the right one. It takes years, requires specialist hiring against uncertain demand, and the first several engagements are learning exercises delivered to paying clients.

There is a third option most firms underuse. A partner who delivers at your standard, under your brand, on your process, without ever appearing in the room. Disclosed if you want it disclosed. Invisible if you do not.

That model works on exactly one condition: the partner has to be genuinely indifferent to being credited. Anything less and it becomes a business development risk dressed as a partnership.

What is the last request you turned down that you would rather have delivered?""",
        status="Idea",
        notes="Bench. The only post aimed at a channel rather than a client. Consider running it "
              "from the company page rather than a personal profile.",
    ),
    _post(
        None, ESSAY, LI, P_INSIGHTS, PILLAR_3,
        "Pressure test your own work",
        """Pressure test your own work before your leadership does it for you.

Every recommendation gets challenged eventually. The only variable is where.

Either it gets challenged in a working session, where a weakness is a finding and there is time to address it. Or it gets challenged in a leadership review, where a weakness is a credibility event and there is no time at all.

The same challenge, applied to the same work, costs radically different amounts depending on which room it happens in. That asymmetry is the entire argument for adversarial internal review, and it is available to any team at almost no cost.

The mechanics are unglamorous. Before anything ships, someone is assigned to argue against the conclusion rather than to check it. Not to proofread, not to sanity check. To genuinely try to break it. Sourcing gets traced back to establish whether the conclusion rests on independent inputs or on one input that was repeated in three places. The weakest link gets named explicitly, on the record, so the team decides what to do about it rather than hoping nobody notices.

Uncomfortable internally, and considerably less uncomfortable than the alternative.

The reason most teams skip it has nothing to do with resourcing. Adversarial review requires someone to argue against colleagues they will work alongside next week, and requires the person who produced the work to absorb that criticism in front of them. Both are socially costly, and the cost arrives weeks before the benefit does.

Teams that do it anyway acquire something specific. Their conclusions stop being surprised.

Who in your process is responsible for trying to break the recommendation before it ships?""",
        status="Idea",
        notes="Bench. Strong closing line. Good substitute for any Tuesday that has to move.",
    ),
]


def all_rows() -> list[dict]:
    """Every seed row, sorted by publish date with undated bench rows last."""
    rows = ESSAYS + BUDGET_POSTS + OBSERVANCE_POSTS + BENCH
    return sorted(rows, key=lambda r: (r["Date"] is None, r["Date"] or date.min))
