# ============================================================================
#  SHARED DATA LAYER (game-agnostic)
#  - link_type(): classify a CAD/design URL for color-coding
#  - DEEP_PROFILES: all per-subsystem profiles (from deepdive_extra.NEW_PROFILES)
#  - TEAMS / BONUS: feature vs. additional split, derived by rank (config cutoff)
#  - META: deep-dive doc header, derived from config
#  Per-team profile fields: rank, team, name, robot, region, epa, record,
#  archetype, shooter, intake, indexer, drivetrain, vision, cad_label, cad_url,
#  lessons[], sources[(label,url)]
# ============================================================================
import config
from deepdive_extra import NEW_PROFILES, STUDY_PICKS, STUDY_PICK_WHY, DROP, CONF_HIGH, CAD_FIX, ENRICH


def link_type(url, label=""):
    """Classify a design/source URL -> (type, short_label) for the link chips.
    Types: cad (green) / binder / code / thread / dds / video / stats / site / none.
    The CAD heuristics are game-agnostic (Onshape/GrabCAD/STEP, or a Chief Delphi
    thread whose slug says CAD release/CAD+code/CAD+documentation)."""
    if not url:
        return ("none", "No link")
    u = url.lower()
    if "onshape.com" in u: return ("cad", "Onshape CAD")
    if "grabcad.com" in u: return ("cad", "GrabCAD")
    import re as _re
    if _re.search(r"/20\d\dcad", u) or u.rstrip("/").endswith("/cad"): return ("cad", "CAD release")
    if "techbinder" in u: return ("binder", "Tech binder")
    if "drive.google.com" in u or "docs.google.com" in u: return ("binder", "Tech binder (Drive)")
    if "github.com" in u: return ("code", "Code (GitHub)")
    if "discord.com" in u: return ("dds", "DDS thread")
    if "chiefdelphi.com" in u:
        if "cad" in u and ("release" in u or "binder" in u or "documentation" in u or "code" in u):
            return ("cad", "CAD release")
        return ("thread", "CD thread")
    if "youtube.com" in u or "youtu.be" in u: return ("video", "Video")
    if "thebluealliance.com" in u or "statbotics" in u: return ("stats", "Stats/TBA")
    return ("site", "Team site")


# All deep profiles come from deepdive_extra.NEW_PROFILES; split into the
# "feature" set (printed as full rows in the deep-dive doc) and the bonus pool,
# purely by rank so the split retunes itself as ranks change.
_profiles = sorted(NEW_PROFILES, key=lambda t: -t.get("epa", 0))
# When real EPA ranks exist, split feature vs. bonus by the config cutoff.
# When they don't yet (e.g. Statbotics outage -> all rank 0), treat every
# profile as a feature row so the deep-dive still renders meaningfully.
_have_rank = any((t.get("rank") or 0) for t in _profiles)
if _have_rank:
    TEAMS = [t for t in _profiles if (t.get("rank") or 9999) <= config.FEATURE_RANK_CUTOFF]
    BONUS = [t for t in _profiles if (t.get("rank") or 9999) > config.FEATURE_RANK_CUTOFF]
else:
    TEAMS = list(_profiles); BONUS = []


def _apply_enrich(team_list):
    for t in team_list:
        e = ENRICH.get(t["team"])
        if not e:
            continue
        for k, v in e.items():
            if k == "sources_add":
                have = {u for _, u in t.get("sources", [])}
                t.setdefault("sources", [])
                for lbl, url in v:
                    if url not in have:
                        t["sources"].append((lbl, url)); have.add(url)
            else:
                t[k] = v
_apply_enrich(TEAMS); _apply_enrich(BONUS)


META = {
    "title": f"{config.TITLE} — Top Robot Design Deep Dive",
    "subtitle": ("A study reference for effective REEFSCAPE design & implementation, drawn from the "
                 "Spectrum 3847 CAD Collection, team CAD/code releases (Onshape / GrabCAD), and each "
                 "team's Chief Delphi reveal / CAD-release thread."),
    "overview": [
        ("The game", config.GAME_BLURB or f"FRC {config.YEAR} {config.GAME}."),
        ("How to use this document",
         "These are the most thoroughly-documented REEFSCAPE robots from the CAD-release set, each with real "
         "subsystem detail mined from the team's Chief Delphi reveal/release thread. For every team we capture "
         "archetype, the four subsystems (scoring / intake / elevator-lift / drivetrain), vision, public CAD "
         "availability, and 'lessons for students'. ★ marks the curated study picks with the richest reproducible "
         "documentation. EPA / rank are pending a Statbotics API outage and will be backfilled when it recovers."),
    ],
}
