# -*- coding: utf-8 -*-
# ============================================================================
#  CURATION + DEEP PROFILES — human-curated layer on top of codex_data.json.
#  FRC 2025 REEFSCAPE. Subsystem fields are repurposed for this game:
#    shooter    -> coral / algae SCORING mechanism (end effector)
#    intake     -> coral / algae INTAKE (ground / station)
#    indexer    -> ELEVATOR / LIFT / superstructure
#    drivetrain -> drivetrain
#  EPA / rank are 0 pending a Statbotics API outage (backfill later); the
#  feature/bonus split therefore puts every profile in the feature set for now.
# ============================================================================

def _cd(t): return f"https://www.chiefdelphi.com/t/{t}"

NEW_PROFILES = [
 dict(rank=0, team=1690, name="Orbit", robot="WHISPER", region="ISR", epa=0, record="",
   archetype="Closed-belt differential elevator; elite-speed coral cycle",
   shooter="Coral end-effector fed off the differential elevator for L1-L4 placement; among the fastest cycles in the world that season.",
   intake="Coral handling tuned for a rapid, repeatable cycle (see CAD).",
   indexer="Closed-belt DIFFERENTIAL elevator — two motors drive a closed belt loop so the carriage height and a second axis are co-controlled; credited to a community design Orbit adapted.",
   drivetrain="Swerve.",
   vision="Unconfirmed (check CAD)",
   cad_label="Onshape CAD", cad_url="https://cad.onshape.com/documents/76609fe05a6594c5f9c4062a/w/437a97728f1629348e9dd7cf/e/465d3a35c190dab8355f1e5c",
   lessons=["A closed-belt differential elevator couples two motions through one belt loop — compact and stiff.",
            "World-class results come from cycle-time obsession, not feature count."],
   sources=[("CD reveal — WHISPER", _cd(492064)), ("CD CAD release", _cd(501057))]),

 dict(rank=0, team=1114, name="Simbotics", robot="Simbot Suzuki", region="CAN", epa=0, record="",
   archetype="Coral-only, station-intake elevator (deliberately minimal scope)",
   shooter="Coral end-effector placing on the reef; team explicitly chose NOT to do ground algae or floor coral.",
   intake="Human-player STATION intake for coral (no floor intake by design).",
   indexer="Elevator superstructure; manipulator position recovery was a known failure mode they discuss in the release.",
   drivetrain="Swerve.",
   vision="Unconfirmed (check CAD)",
   cad_label="Onshape CAD", cad_url="https://cad.onshape.com/documents/8782ccd3db870fc41090b5e6/w/88d1084497e586d2c58a4051/e/f1dc3344d36d78907a60d4d9",
   lessons=["Scope discipline: dropping deep climb, ground algae and floor coral let them perfect one cycle.",
            "Document your failure modes (lost manipulator position) — it teaches more than a highlight reel."],
   sources=[("CD CAD release", _cd(500046))]),

 dict(rank=0, team=695, name="Bison Robotics", robot="Goldfish", region="", epa=0, record="",
   archetype="Fully-autonomous coral scorer; repulsion-field auto-align",
   shooter="Coral end-effector with fully autonomous scoring across reef levels.",
   intake="Autonomous feeder-station pickup (no driver input needed for the cycle).",
   indexer="Elevator superstructure; all mechanism control loops run on-board the motor controllers.",
   drivetrain="Full Kraken-X60 swerve drivebase.",
   vision="Dual Limelight 4 running MegaTag2; 200 Hz odometry fused with a NavX2 for robust localization.",
   cad_label="Onshape CAD", cad_url="https://cad.onshape.com/documents/952ba22fa909a3d0882388da/w/94a37671574438408b83a5fc/e/97e98c3970941d33c368b387",
   lessons=["MegaTag2 + high-rate odometry (200 Hz) makes full-auto scoring practical.",
            "A repulsion (potential) field is a clean way to auto-align while avoiding field collisions.",
            "Running control loops on the motor controllers offloads the roboRIO."],
   sources=[("CD CAD & code release", _cd(503259))]),

 dict(rank=0, team=341, name="Miss Daisy", robot="(2025)", region="USA-PA", epa=0, record="",
   archetype="Floor-intake continuous elevator; lantern-gear shoulder + wrist; deep climb",
   shooter="Coral end-effector on a lantern-gear-driven SHOULDER with a 180-degree WRIST for multi-level reef placement.",
   intake="Coral FLOOR intake.",
   indexer="Continuous (single-stage continuous) elevator; a software 'superstructure' supervises arm/elevator states to prevent self-collision.",
   drivetrain="Swerve.",
   vision="Unconfirmed (check CAD/code)",
   cad_label="CD CAD/Code/Docs release", cad_url=_cd(500739),
   lessons=["A state-supervising 'superstructure' layer prevents the arm from colliding with the robot — model your mechanism states explicitly.",
            "Floor intake + continuous elevator + 180-degree wrist is a flexible multi-level coral solution."],
   sources=[("CD CAD, code & documentation release", _cd(500739)),
            ("Onshape CAD", "https://cad.onshape.com/documents/2d1e3ac103dba342712c2c99/w/060f69714e723dd87d33ba97/e/bbd3959b191284cc99eb4f56")]),

 dict(rank=0, team=1086, name="Blue Cheese", robot="Stingray", region="USA-VA", epa=0, record="",
   archetype="Full-capability: 4-level coral, algae net+processor, deep climb",
   shooter="Coral on all four reef levels; algae removed from the reef and scored in both the net and the processor.",
   intake="Coral from the human station; algae off the reef.",
   indexer="Elevator superstructure carrying the coral/algae effector.",
   drivetrain="Swerve.",
   vision="Unconfirmed (check CAD/code)",
   cad_label="CD CAD & code release", cad_url=_cd(506376),
   lessons=["A genuine do-everything robot (4-level coral + algae net/processor + deep climb) is achievable but demands tight packaging.",
            "Releasing CAD + code together makes the whole system reproducible."],
   sources=[("CD CAD & code release", _cd(506376)),
            ("Onshape CAD", "https://henrico.onshape.com/documents/4298135b1628b8946460de4d/w/4d0457fe199dcea6e0e957c8/e/a2d3bdc8542a373f596b09b2")]),

 dict(rank=0, team=1153, name="Timberwolves", robot="Lagotto", region="", epa=0, record="",
   archetype="1-stage elevator (L1-L3) + algae; ground algae; sub-15 s deep climb",
   shooter="Coral on L1-L3; algae scored into the processor and barge.",
   intake="Ground ALGAE intake (plus coral handling).",
   indexer="Single-stage elevator — simpler than multi-stage rivals, traded top-level reach for reliability.",
   drivetrain="Swerve.",
   vision="Unconfirmed (check CAD)",
   cad_label="CD CAD release", cad_url=_cd(502263),
   lessons=["A 1-stage elevator can win districts if the rest of the cycle is fast and reliable.",
            "A sub-15-second deep climb is a strong endgame insurance policy."],
   sources=[("CD CAD release", _cd(502263)),
            ("Onshape CAD", "https://cad.onshape.com/documents/0c941b8ba82f0478778218c8/w/869934382d3f497294f1e886/e/0accb6313ed5fe4afa0c8d8a")]),

 dict(rank=0, team=3005, name="RoboChargers", robot="Relay", region="USA-TX", epa=0, record="",
   archetype="3-stage elevator + 'laterator' end-effector (coral ejector + algae gripper)",
   shooter="A 'laterator' carries both a coral ejector and an algae gripper; coral is routed THROUGH the elevator to the effector.",
   intake="Funnel-assisted coral handling; algae gripper for reef/processor.",
   indexer="3-stage elevator carrying the laterator.",
   drivetrain="Swerve.",
   vision="Unconfirmed (check CAD)",
   cad_label="CD reveal — Relay", cad_url=_cd(493529),
   lessons=["Routing the game piece through the elevator saves a separate hand-off path.",
            "A 'laterator' (lateral translator) end-effector neatly combines two scoring jobs."],
   sources=[("CD reveal — Relay", _cd(493529)),
            ("Onshape CAD", "https://cad.onshape.com/documents/be7ecb57773083221899273d/w/3ffbf14ecde31212fdcb4a6a/e/fe6648ecf44d2b65b2b452a4")]),

 dict(rank=0, team=2930, name="Sonic Squirrels", robot="(2025)", region="USA-WA", epa=0, record="",
   archetype="Coral robot; deep Choreo auto library + PhotonVision",
   shooter="Coral end-effector for reef placement.",
   intake="Coral intake (see CAD).",
   indexer="Elevator superstructure.",
   drivetrain="Swerve.",
   vision="PhotonVision on two Orange Pi 5 coprocessors; 100+ short Choreo paths stitched into driver-selectable autos.",
   cad_label="CD CAD & code release", cad_url=_cd(505039),
   lessons=["Build autos from many SHORT Choreo paths so the drive team can compose routines on the fly.",
            "Dual coprocessors give you redundant / wider-FOV PhotonVision coverage."],
   sources=[("CD CAD & code release", _cd(505039)),
            ("Onshape CAD", "https://cad.onshape.com/documents/031bb7cc6f7ddc530d4778f1/w/667b243ea0c6188633e5d992/e/8bf82e4f98b2523855e4c640")]),

 dict(rank=0, team=1732, name="Hilltopper Robotics", robot="(2025)", region="USA-KY", epa=0, record="",
   archetype="Coral arm/claw; 4x-L4 autonomous; algae handoff to processor",
   shooter="Coral claw placing on the reef (up to four L4 in auto); algae handed down into the processor.",
   intake="Coral intake feeding the claw; algae path with added guarding to keep coral out.",
   indexer="Arm/lift superstructure.",
   drivetrain="Swerve.",
   vision="QuestNav (Meta Quest headset) used for localization in the 4x-L4 auto.",
   cad_label="CD reveal (4x L4 QuestNav auto)", cad_url=_cd(492785),
   lessons=["QuestNav (a VR headset's inside-out tracking) is a low-cost, high-rate localization source for autos.",
            "Design the algae path so it can't accidentally ingest coral."],
   sources=[("CD reveal — 4x L4 QuestNav auto", _cd(492785)),
            ("Onshape CAD", "https://cad.onshape.com/documents/39e02e7c3e67fe63d706d23a/w/599feda2281071a3b9d02adb/e/f0d7233aecb37fcf95f6520f")]),

 dict(rank=0, team=2910, name="Jack in the Bot", robot="Spectre", region="USA-WA", epa=0, record="",
   archetype="Very compact self-aligning ground coral intake; fast cycle",
   shooter="Coral end-effector for reef placement; high throughput (paired with 9442 at events).",
   intake="One of the smallest self-aligning GROUND coral intakes in the game — centers the coral as it ingests.",
   indexer="Elevator superstructure.",
   drivetrain="Swerve.",
   vision="Unconfirmed (check CAD)",
   cad_label="CD CAD release", cad_url=_cd(500310),
   lessons=["Passive geometry can self-center a game piece, shrinking the intake envelope.",
            "A small, reliable ground intake enables a faster, more flexible cycle."],
   sources=[("CD reveal — Spectre", _cd(494648)), ("CD CAD release", _cd(500310)),
            ("Onshape CAD", "https://2910.onshape.com/documents/f33ab032b00dc4b711aa86a6/w/951c0955d38b370eab02b587/e/415a66cb7efdf4aba6199086")]),

 dict(rank=0, team=8159, name="Golden Horn", robot="Serpentheim", region="TUR", epa=0, record="",
   archetype="Coral robot, dual Limelight; 2 regional wins + first Impact Award",
   shooter="Coral end-effector for reef placement.",
   intake="Coral intake (see CAD).",
   indexer="Elevator superstructure.",
   drivetrain="Swerve.",
   vision="Two Limelight cameras (discussed in the release Q&A).",
   cad_label="CD CAD, code & strategy release", cad_url=_cd(509509),
   lessons=["Pairing CAD + code + STRATEGY documents is rare and valuable — study how strategy drove their design.",
            "Strong engineering and outreach can come together (2 regionals + first Impact Award)."],
   sources=[("CD CAD, code & strategy release", _cd(509509)),
            ("Onshape CAD", "https://cad.onshape.com/documents/9b4847a461c2a185e6ff320a/w/6df8cee50adeaba604998544/e/ed071581b5e32ec2f2371cae")]),

 dict(rank=0, team=190, name="Gompei and the HERD", robot="(2025 V2)", region="USA-MA", epa=0, record="",
   archetype="6-motor elevator; star-wheel outtake flips coral up onto L4",
   shooter="Outtake with STAR WHEELS that flip the coral upward as it leaves, seating it on L4; a ramp straightens/holds the coral instead of a powered belt.",
   intake="Coral intake feeding the ramp.",
   indexer="6-motor elevator (high power for fast, repeatable height changes).",
   drivetrain="Swerve.",
   vision="Unconfirmed (check CAD)",
   cad_label="CD CAD release", cad_url=_cd(503355),
   lessons=["Star wheels can re-orient a game piece during ejection (flip coral up for L4).",
            "Sometimes a passive ramp beats a powered belt for straightening/holding a piece."],
   sources=[("CD CAD release", _cd(503355)),
            ("Onshape CAD", "https://frc190.onshape.com/documents/b6c840749d995b1ac1b29215/v/c2f65e25658d56c674449d2f/e/271cc80064eb69c77815f945")]),

 dict(rank=0, team=1156, name="Under Control", robot="(2025)", region="BRA", epa=0, record="",
   archetype="Swerve coral robot; permanent orientation-PID heading hold; tech binder",
   shooter="Coral end-effector for reef placement.",
   intake="Coral intake (see CAD/binder).",
   indexer="Elevator superstructure.",
   drivetrain="Swerve that always runs with an orientation (heading) PID engaged.",
   vision="Unconfirmed (check binder)",
   cad_label="CD CAD, code & tech-binder release", cad_url=_cd(505398),
   lessons=["Always-on heading PID makes driving and auto-aim more deterministic.",
            "A released technical binder is the gold standard for reproducibility."],
   sources=[("CD CAD, code & tech binder", _cd(505398)),
            ("Onshape CAD", "https://cad.onshape.com/documents/6e3b7e0b9e9abe53ea984480/w/70c43f2512c4ee937087fd79/e/86286eb9c833cb428656891e")]),
]

# ---- STUDY PICKS -----------------------------------------------------------
STUDY_PICKS = {1690, 1114, 695, 341, 1086, 1153, 3005, 2930, 1732, 2910, 8159, 190, 1156}

STUDY_PICK_WHY = {
 1690:"PICK (CAD): closed-belt differential elevator + world-class coral cycle; full Onshape release to reverse-engineer.",
 1114:"PICK (CAD): masterclass in scope discipline — a coral-only station-intake design that drops deep climb/ground algae on purpose; full CAD.",
 695:"PICK (CAD+code): dual-Limelight4 MegaTag2 localization at 200 Hz, fully autonomous scoring + repulsion-field auto-align; CAD and code public.",
 341:"PICK (CAD+code+docs): floor intake + continuous elevator + lantern-gear shoulder/180-degree wrist, with a state-supervising 'superstructure'; CAD, code AND docs.",
 1086:"PICK (CAD+code): true do-everything robot (4-level coral, algae net+processor, deep climb); CAD + code released.",
 1153:"PICK (CAD): 1-stage elevator + ground algae + sub-15s deep climb that captained every district event; full CAD.",
 3005:"PICK (CAD): clever 'laterator' end-effector (coral ejector + algae gripper) on a 3-stage elevator with coral routed through the elevator.",
 2930:"PICK (CAD+code): deep Choreo auto library (100+ short paths) + dual-Orange-Pi PhotonVision; great autonomy/vision study.",
 1732:"PICK (CAD): 4x-L4 QuestNav-localized auto and a coral-claw + algae-to-processor handoff — leading VR-odometry example.",
 2910:"PICK (CAD): one of the smallest self-aligning ground coral intakes in the game; reveal + CAD released.",
 8159:"PICK (CAD+code+strategy): rare CAD + code + strategy release from a 2x regional winner and first-time Impact Award team.",
 190:"PICK (CAD): 6-motor elevator with a star-wheel outtake that flips coral onto L4; instructive intake/outtake geometry.",
 1156:"PICK (CAD+binder): swerve with always-on heading PID, plus a released technical binder for full reproducibility.",
}

# ---- BADGE / CONFIDENCE CURATION ------------------------------------------
DROP = set()           # nothing dropped — every entry released downloadable CAD
CONF_HIGH = set()      # codex already marks all High (downloadable CAD located)
CAD_FIX = {}           # all audited as downloadable CAD = "Yes"

# ---- ENRICHMENT ------------------------------------------------------------
ENRICH = {}
