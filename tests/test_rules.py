import pytest

from CocCharamakeSupport import damage_bonus, dice_roll


@pytest.mark.parametrize(
    ("total", "expected"),
    [
        (2, "-1D6"),
        (12, "-1D6"),
        (13, "-1D4"),
        (16, "-1D4"),
        (17, "0"),
        (24, "0"),
        (25, "+1D4"),
        (32, "+1D4"),
        (33, "+1D6"),
        (40, "+1D6"),
        (41, "+2D6"),
        (56, "+2D6"),
        (57, "+3D6"),
        (72, "+3D6"),
        (73, "+4D6"),
        (88, "+4D6"),
        (89, "+5D6"),
    ],
)
def test_damage_bonus_table(total, expected):
    assert damage_bonus(total - 1, 1) == expected


@pytest.mark.parametrize("total", [0, 1])
def test_damage_bonus_before_status_is_rolled(total):
    assert damage_bonus(total, 0) == "---"


def test_dice_roll_range():
    results = {dice_roll(3, 6, 3) for _ in range(5000)}
    assert min(results) == 6
    assert max(results) == 21
