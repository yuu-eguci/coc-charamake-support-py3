from pathlib import Path

GOLDEN = Path(__file__).parent / "golden" / "midorikawa.txt"


def test_initial_screen(gccs):
    assert gccs.skill_total("探索系技能", 1) == "30"
    assert gccs.skill_total("戦闘系技能", 4) == "50"
    assert gccs.skill_total("知識系技能", 17) == "20"
    assert gccs.status_value("HP") == "0"


def test_dice_roll_fills_status_within_dice_ranges(gccs):
    gccs.press("DICE ROLL")
    ranges = {"STR": (3, 18), "SIZ": (8, 18), "INT": (8, 18), "EDU": (6, 21)}
    for name, (low, high) in ranges.items():
        assert low <= int(gccs.status_entry(name).get()) <= high
    con = int(gccs.status_entry("CON").get())
    siz = int(gccs.status_entry("SIZ").get())
    assert gccs.status_value("HP") == str((con + siz + 1) // 2)


def test_sample_character_derived_values(gccs):
    gccs.fill_sample_character()
    gccs.pump()
    assert gccs.status_value("HP") == "12"
    assert gccs.status_value("SAN") == "65"
    assert gccs.status_value("知識") == "90"
    assert gccs.skill_total("探索系技能", 12) == "75"
    assert gccs.skill_total("戦闘系技能", 1) == "48"
    assert gccs.skill_total("交渉系技能", 6) == "90"


def test_output_matches_golden(gccs, tmp_path):
    gccs.fill_sample_character()
    gccs.pump()
    gccs.press("OUTPUT")
    written = (tmp_path / "midorikawa.txt").read_text(encoding="utf-8")
    assert written == GOLDEN.read_text(encoding="utf-8")

