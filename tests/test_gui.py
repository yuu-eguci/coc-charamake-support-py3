from pathlib import Path

import pytest

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


def test_recalculation_continues_after_entry_is_blanked(gccs):
    gccs.type_into(gccs.status_entry("STR"), "")
    gccs.pump()
    gccs.type_into(gccs.status_entry("STR"), "9")
    gccs.type_into(gccs.skill_cell("探索系技能", 2, 2), "40")
    gccs.pump()
    assert gccs.skill_total("探索系技能", 2) == "41"


def test_numbers_with_leading_zero_are_decimal(gccs):
    # 初期値の "0" の後ろに続けて打つと "012" のようになります。
    gccs.type_into(gccs.skill_cell("探索系技能", 1, 2), "012")
    gccs.type_into(gccs.status_entry("DEX"), "09")
    gccs.pump()
    assert gccs.skill_total("探索系技能", 1) == "42"
    assert gccs.skill_total("戦闘系技能", 1) == "18"


def test_tab_moves_down_the_occupation_column(gccs):
    entry = gccs.skill_cell("探索系技能", 1, 2)
    assert entry.tk_focusNext() is gccs.skill_cell("探索系技能", 2, 2)


def test_invalid_app_does_not_stop_recalculation(gccs):
    gccs.type_into(gccs.status_entry("APP"), "")
    gccs.type_into(gccs.skill_cell("探索系技能", 2, 2), "40")
    gccs.pump()
    assert gccs.skill_total("探索系技能", 2) == "41"


def test_output_uses_values_typed_just_before(gccs, tmp_path):
    gccs.type_into(gccs.output_name_entry(), "quick")
    gccs.type_into(gccs.skill_cell("探索系技能", 2, 2), "40")
    gccs.press("OUTPUT")
    assert "<鍵開け:41%>" in (tmp_path / "quick.txt").read_text(encoding="utf-8")
    assert gccs.output_message() == "quick.txt に書き出したよ"


def test_output_trims_spaces_from_file_name(gccs, tmp_path):
    gccs.press("OUTPUT")
    assert [path.name for path in tmp_path.iterdir()] == ["---.txt"]


def test_output_refuses_non_numbers(gccs, tmp_path):
    gccs.type_into(gccs.status_entry("STR"), "abc")
    gccs.press("OUTPUT")
    assert list(tmp_path.iterdir()) == []
    assert gccs.output_message() == "数字の欄に数字以外が入っているよ"


@pytest.mark.parametrize("name", ["", "  ", "../escape", "sub/dir", "a\\b", "a\0b"])
def test_output_refuses_bad_file_names(gccs, tmp_path, name):
    gccs.type_into(gccs.output_name_entry(), name)
    gccs.press("OUTPUT")
    assert list(tmp_path.iterdir()) == []
    assert gccs.output_message() == "ファイル名を入れてね (/ と \\ は使えないよ)"


def test_output_reports_write_errors(gccs, tmp_path):
    gccs.type_into(gccs.output_name_entry(), "x" * 300)
    gccs.press("OUTPUT")
    assert list(tmp_path.iterdir()) == []
    assert gccs.output_message().startswith("書き出せなかったよ: ")


def test_mini_dice_roll(gccs):
    result = gccs.roll_mini_dice(3, 6, 2)
    assert result.startswith("result: ")
    assert 5 <= int(result.removeprefix("result: ")) <= 20
    assert gccs.roll_mini_dice(0, 6, 4) == "result: 4"
    assert gccs.roll_mini_dice(1000, 1, 0) == "result: 1000"


@pytest.mark.parametrize(
    ("count", "sides", "bonus"),
    [
        (1, 0, 0),
        (-1, 6, 0),
        (1001, 6, 0),
        ("x", 6, 0),
        (1, "", 0),
        (1, 6, "1.5"),
        pytest.param(1, 6, "9" * 4300, id="huge-bonus"),
    ],
)
def test_mini_dice_rejects_bad_input(gccs, count, sides, bonus):
    assert gccs.roll_mini_dice(count, sides, bonus) == "result: 入力エラー"


def test_dice_roll_while_a_skill_entry_is_blank(gccs):
    # 主に確かめているのは、ボタンの処理で例外が出ないことです (fixture で検出します)。
    gccs.type_into(gccs.skill_cell("探索系技能", 1, 2), "")
    gccs.press("DICE ROLL")
    con = int(gccs.status_entry("CON").get())
    siz = int(gccs.status_entry("SIZ").get())
    assert gccs.status_value("HP") == str((con + siz + 1) // 2)


def test_long_file_name_message_does_not_widen_the_window(gccs, tmp_path):
    left = gccs.output_name_entry().master.master
    width = left.winfo_reqwidth()
    gccs.type_into(gccs.output_name_entry(), "x" * 200)
    gccs.press("OUTPUT")
    gccs.root.update()
    assert (tmp_path / ("x" * 200 + ".txt")).exists()
    assert gccs.output_message() == "x" * 23 + "….txt に書き出したよ"
    assert left.winfo_reqwidth() == width
