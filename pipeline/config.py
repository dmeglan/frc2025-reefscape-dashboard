# ============================================================================
#  PER-YEAR CONFIG — the ONLY file you normally edit to retarget a new FRC
#  season. Titles, filenames, intro copy, Statbotics URLs, and the credit line
#  are all derived from these values.
# ============================================================================

YEAR  = 2025                # FRC competition year
GAME  = "REEFSCAPE"         # Official game name, e.g. "CRESCENDO", "REEFSCAPE"
SCORING_ELEMENT = "CORAL/ALGAE"  # Game piece, e.g. "NOTE", "CORAL"/"ALGAE", "FUEL"

# One factual sentence for the dashboard intro. Describe the scoring cycle and
# call out any low-value mechanism most top teams skipped (so "no climber" reads
# as a design choice, not missing data). May be "".
GAME_BLURB = ("REEFSCAPE is a coral-and-algae game: robots place CORAL (PVC tubes) on the "
              "REEF's four branch levels (L1-L4) and score ALGAE (foam balls) into the PROCESSOR "
              "or BARGE NET, then climb a CAGE in the endgame. Most top designs centered on a fast "
              "coral cycle (station or ground intake -> elevator/arm -> reef); many top teams ran "
              "coral-only and treated algae and deep climb as optional, lower-value choices.")

# Credit line shown in the footer (yours by default — change or blank it).
COMPILED_BY = ('Compiled by <a class=by href="https://linkedin.com/in/dmeglan" target="_blank" '
               'rel="noopener">Dwight Meglan · FRC 1757/8567 · linkedin.com/in/dmeglan</a>')

# Archetype filter dropdown (value, label). The dashboard matcher does a
# case-insensitive substring test of value vs each robot's archetype text —
# pick short tokens that actually occur. Retune per game.
ARCHETYPES = [
    ("elevator", "Elevator"), ("arm", "Arm/pivot"), ("algae", "Algae-capable"),
    ("coral-only", "Coral-only"), ("ground", "Ground intake"), ("deep climb", "Deep climb"),
]

# Rank <= this gets a full "feature" row in the deep-dive; the rest are the bonus pool.
FEATURE_RANK_CUTOFF = 30

# ---- derived (rarely touch) ------------------------------------------------
TITLE         = f"FRC {YEAR} {GAME}"
DASH_TITLE    = f"{TITLE} — Robot Study Dashboard"
DEEPDIVE_TITLE= f"{TITLE} — Top Robot Design Deep Dive"
DASH_FILE     = f"FRC{YEAR}_{GAME.title()}_Robot_Study_Dashboard.html"
DEEPDIVE_HTML = f"FRC{YEAR}_{GAME.title()}_TopTeams_DeepDive.html"
DEEPDIVE_PDF  = f"FRC{YEAR}_{GAME.title()}_TopTeams_DeepDive.pdf"


CREDIT_NAME = "Dwight Meglan · FRC 1757/8567 · linkedin.com/in/dmeglan"  # footer name inside the linkedin anchor; blank or change per user

def statbotics_team(t): return f"https://api.statbotics.io/v3/team_year/{t}/{YEAR}"
def statbotics_link(t): return f"https://www.statbotics.io/team/{t}/{YEAR}"
def tba_link(t):        return f"https://www.thebluealliance.com/team/{t}/{YEAR}"
