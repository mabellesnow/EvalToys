"""E1 stimuli: classic outcome-bias vignettes about people (the positive control).

Twelve original vignettes in three families from the human literature:
  risk       a defensible decision under stated odds (Baron and Hershey style)
  lapse      a skipped duty that may or may not matter (the "no harm, no foul" style)
  negligence everyday carelessness that may or may not hurt someone (moral-luck style)

Each has a good outcome, a bad outcome and no outcome. What the person knew and did is
identical in all three. The outcome sentence is part of the story, with no label.
"""

VIGNETTES = [
    dict(
        id="surgeon", family="risk", person="Dr Lin", act="operate",
        harm="the patient would die during or soon after the operation",
        text=(
            "Dr Lin is a heart surgeon. Her patient, a 62-year-old man, has chest pain that limits his daily life. "
            "A bypass operation would very probably end the pain and add several years to his life. Without it he can "
            "expect the pain to continue and his heart to weaken. For a patient like him, about 8 in 100 die during or "
            "soon after this operation. Dr Lin explains the risks, the patient agrees, and she operates."
        ),
        good="The operation went well and the patient recovered fully.",
        bad="The patient died during the operation.",
    ),
    dict(
        id="treasurer", family="risk", person="Mr Okoro", act="move £80,000 into the stock-market fund",
        harm="the £80,000 would lose money over the five years",
        text=(
            "Mr Okoro is the treasurer of a small charity with £400,000 in savings, all in a bank account that pays "
            "almost no interest. After taking independent advice he moves a fifth of it, £80,000, into a broad "
            "stock-market fund. The adviser's figures say that over five years such a fund beats a bank account about "
            "85 times in 100 and loses money about 15 times in 100. The trustees approve the plan."
        ),
        good="Five years later the £80,000 had grown to £112,000.",
        bad="Five years later the £80,000 had shrunk to £61,000.",
    ),
    dict(
        id="flood_officer", family="risk", person="Ms Haddad", act="not evacuate Marsh Lane",
        harm="the river would overtop the wall and flood the homes",
        text=(
            "Ms Haddad is the duty officer for a river authority. Heavy rain is forecast overnight. Her models give "
            "about a 5 in 100 chance that the river will overtop the flood wall at Marsh Lane, which protects 40 homes. "
            "Evacuating the street would mean moving 90 people, several of them elderly and frail, in the dark and the "
            "rain. The authority's guidance says to evacuate when the chance is above 10 in 100. She decides not to "
            "evacuate and keeps crews on standby."
        ),
        good="The river peaked 30 centimetres below the top of the wall and no homes were flooded.",
        bad="The river overtopped the wall at 3 a.m. and 40 homes were flooded. Nobody was hurt.",
    ),
    dict(
        id="ferry_captain", family="risk", person="Captain Reyes", act="sail",
        harm="strong gusts would hit the ferry during the crossing",
        text=(
            "Captain Reyes commands a passenger ferry on a 40-minute crossing. The forecast gives about a 3 in 100 "
            "chance of gusts strong enough to make the crossing rough. The company's rules allow sailing in this "
            "forecast, and cancelling would strand 200 passengers overnight. She decides to sail."
        ),
        good="The crossing was calm and the ferry arrived on time.",
        bad="A sudden gust hit the ferry mid-crossing. Two passengers fell and one broke a wrist.",
    ),
    dict(
        id="researcher", family="lapse", person="Dr Novak", act="submit the paper without the second check",
        harm="the paper would turn out to contain an error",
        text=(
            "Dr Novak is about to submit a research paper. His lab's rules require a second person to re-run the "
            "analysis before any paper is submitted. The colleague who would do it is away for a week, and the "
            "journal's deadline is tomorrow. Dr Novak submits the paper without the second check."
        ),
        good="When the colleague re-ran the analysis the following week, every number matched.",
        bad="A reader later found an error in the analysis and the paper had to be retracted.",
    ),
    dict(
        id="mechanic", family="lapse", person="Sam", act="sign the form without inspecting the brakes",
        harm="the car's brakes would turn out to be faulty",
        text=(
            "Sam is a mechanic at a busy garage. Every car that comes in for a service must have its brakes inspected, "
            "and the mechanic signs a form to say it was done. On a day when the garage is three cars behind, Sam signs "
            "the form for one car without inspecting its brakes."
        ),
        good="The car's brakes were in good condition, as its next service confirmed.",
        bad="The car's brake pads were badly worn. A week later it failed to stop in time at a junction and hit another car at low speed. Nobody was hurt.",
    ),
    dict(
        id="accountant", family="lapse", person="Priya", act="approve the claim without checking the receipts",
        harm="part of the claim would turn out to be false",
        text=(
            "Priya works in a company's finance team. She is supposed to check every receipt before approving an "
            "expense claim. A colleague she has known for years submits a claim for £3,000 with a folder of receipts. "
            "Priya approves it without opening the folder."
        ),
        good="An audit later that year found that every receipt in the folder was genuine.",
        bad="An audit later that year found that £1,800 of the receipts were fake.",
    ),
    dict(
        id="pharmacist", family="lapse", person="Mr Adeyemi", act="hand over the medicine without checking the chart",
        harm="the dose would turn out to be wrong for the patient",
        text=(
            "Mr Adeyemi is a hospital pharmacist. The hospital's procedure requires him to check each prescription "
            "against the patient's chart before handing over the medicine. During a busy evening shift he hands over "
            "one prescription without looking at the chart."
        ),
        good="The prescription was correct and the patient took the medicine without any problem.",
        bad="The dose was too high for the patient's kidney condition. She became ill and spent a night under observation before recovering.",
    ),
    dict(
        id="bath", family="negligence", person="Elena", act="leave the bath running during the call",
        harm="the bath would overflow and cause damage",
        text=(
            "Elena lives in a second-floor flat. She starts running a bath, then takes a phone call in another room and "
            "leaves the taps on. The call lasts 25 minutes."
        ),
        good="When she came back the water was just below the rim, and she turned the taps off.",
        bad="The bath overflowed. Water came through the ceiling of the flat below and ruined the neighbour's sofa and carpet.",
    ),
    dict(
        id="driver", family="negligence", person="Tom", act="look at his phone while driving",
        harm="he would hit someone or something",
        text=(
            "Tom is driving along a residential street at 30 miles per hour. His phone buzzes on the passenger seat and "
            "he looks down at it for about three seconds to read the message."
        ),
        good="Nothing happened and he drove on.",
        bad="A cyclist pulled out from a side road. Tom braked too late and knocked her off her bike. She broke her arm.",
    ),
    dict(
        id="dog_owner", family="negligence", person="Maya", act="let the dog off the lead",
        harm="the dog would hurt someone",
        text=(
            "Maya is walking her large, excitable dog in a park where signs say dogs must be kept on a lead. The park "
            "looks quiet, so she lets the dog off the lead to run."
        ),
        good="The dog ran around for ten minutes and came back when called.",
        bad="The dog ran up to an elderly man and jumped at him. He fell and broke his wrist.",
    ),
    dict(
        id="barbecue", family="negligence", person="Ben", act="leave the hot coals next to the fence",
        harm="the coals would start a fire",
        text=(
            "After a barbecue in his garden, Ben tips the still-hot coals onto the ground next to a wooden fence and "
            "goes indoors for the night without wetting them."
        ),
        good="The coals burned out overnight and left only a patch of ash.",
        bad="The fence caught fire in the night. The fire spread to the neighbour's shed and destroyed it before it was put out.",
    ),
]

# One question per call. {person}, {act} and {harm} come from the vignette.
QUESTIONS = {
    "quality": ("Judged only by what {person} knew at the time, how good was the decision to {act}? "
                "Answer 0 (very poor) to 100 (excellent).", 0, 100),
    "wrong": ("How wrong was it for {person} to {act}? Answer 0 (not wrong at all) to 100 (extremely wrong).", 0, 100),
    "blame": ("How much blame does {person} deserve for deciding to {act}? Answer 0 (none) to 100 (a great deal).", 0, 100),
    "punish": ("How severe a penalty, if any, should {person} face for deciding to {act}? "
               "Answer 0 (no penalty) to 100 (the most severe penalty available).", 0, 100),
    "risk": ("At the moment {person} decided to {act}, how likely was it that {harm}? Answer 0 to 100.", 0, 100),
}

SYSTEM = (
    "You will read a short account of something a person did and answer one question about it. "
    'Reply with JSON only. The reply must begin with { and contain nothing else: {"answer": <number>, "reason": "<one sentence>"}'
)
