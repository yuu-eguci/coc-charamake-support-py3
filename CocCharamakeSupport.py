"""CocCharamakeSupport

tkinterを使ってるのでpython3専用。
CoC TRPG キャラメイク用ツール。
"""

import contextlib
import random
import tkinter as tk
from typing import NamedTuple

# 能力値と、ダイスロールで振るダイス (個数, 面数, 足す数) です。
STATUS_DICE = {
    "STR": (3, 6, 0),
    "CON": (3, 6, 0),
    "POW": (3, 6, 0),
    "DEX": (3, 6, 0),
    "APP": (3, 6, 0),
    "SIZ": (2, 6, 6),
    "INT": (2, 6, 6),
    "EDU": (3, 6, 3),
}

PROFILE_LABELS = (
    "キャラ名",
    "職業",
    "年齢",
    "性別",
    "出身",
    "持ち物",
    "",
    "",
    "",
    "メモ",
    "",
    "",
    "",
)
PROFILE_DEFAULTS = {5: " ---", 9: " ---"}


class Skill(NamedTuple):
    name: str
    initial: int
    # None なら技能名は固定です。文字列なら技能名を入力でき、出力では「prefix 技能名」になります。
    prefix: str | None = None

    def label(self, name):
        return f"{self.prefix} {name}" if self.prefix else name


class Category(NamedTuple):
    # 画面での位置です。 column は技能表の何列目に置くかです。
    column: int
    row: int
    sticky: str
    skills: tuple[Skill, ...]


SKILL_CATEGORIES = {
    "探索系技能": Category(
        0,
        0,
        "ewn",
        (
            Skill("応急手当", 30),
            Skill("鍵開け", 1),
            Skill("隠す", 15),
            Skill("隠れる", 10),
            Skill("聞き耳", 25),
            Skill("忍び歩き", 10),
            Skill("写真術", 10),
            Skill("精神分析", 1),
            Skill("追跡", 10),
            Skill("登攀", 40),
            Skill("図書館", 25),
            Skill("目星", 25),
        ),
    ),
    "戦闘系技能": Category(
        0,
        1,
        "ewn",
        (
            Skill("回避", 0),  # DEX * 2
            Skill("キック", 25),
            Skill("組付き", 25),
            Skill("こぶし(パンチ)", 50),
            Skill("頭突き", 10),
            Skill("投擲", 25),
            Skill("マーシャルアーツ", 1),
            Skill("拳銃", 20),
            Skill("サブマシンガン", 15),
            Skill("ショットガン", 30),
            Skill("マシンガン", 15),
            Skill("ライフル", 25),
        ),
    ),
    "交渉系技能": Category(
        1,
        0,
        "ewn",
        (
            Skill("言いくるめ", 5),
            Skill("信用", 15),
            Skill("説得", 15),
            Skill("値切り", 5),
            Skill("心理学", 5),
            Skill("--母国語--", 0, "母国語"),  # EDU * 5
            Skill("--外国語--", 0, "外国語"),
        ),
    ),
    "知識系技能": Category(
        1,
        1,
        "ew",
        (
            Skill("医学", 5),
            Skill("オカルト", 5),
            Skill("科学", 1),
            Skill("クトゥルフ神話", 0),
            Skill("経理", 10),
            Skill("考古学", 1),
            Skill("コンピュータ", 1),
            Skill("人類学", 1),
            Skill("生物学", 1),
            Skill("地質学", 1),
            Skill("電子工学", 1),
            Skill("天文学", 1),
            Skill("博物学", 10),
            Skill("物理学", 1),
            Skill("法律", 5),
            Skill("薬学", 1),
            Skill("歴史", 20),
            Skill("--芸術--", 5, "芸術"),
        ),
    ),
    "行動系技能": Category(
        2,
        0,
        "ewn",
        (
            Skill("運転", 20),
            Skill("機械修理", 20),
            Skill("重機械操作", 1),
            Skill("乗馬", 5),
            Skill("水泳", 25),
            Skill("跳躍", 25),
            Skill("電気修理", 10),
            Skill("ナビゲート", 10),
            Skill("変装", 1),
            Skill("--制作--", 5, "制作"),
            Skill("--操縦--", 1, "操縦"),
        ),
    ),
    "任意の技能": Category(
        2,
        1,
        "ew",
        (
            Skill("--お好きに--", 0, ""),
            Skill("", 0, ""),
            Skill("", 0, ""),
        ),
    ),
}
SKILL_HEADERS = ("     技能名     ", "初期値", "職業P", "興味P", "合計")


MINI_DICE_MAX_COUNT = 1000


def dice_roll(count, sides, bonus=0):
    """countDsides + bonus の結果を返します。"""
    return sum(random.randint(1, sides) for _ in range(count)) + bonus


# STR + SIZ の上限と、そのときのダメージボーナスです。 56 を超えると 16 ごとに +1D6 増えます。
DAMAGE_BONUS_TABLE = (
    (12, "-1D6"),
    (16, "-1D4"),
    (24, "0"),
    (32, "+1D4"),
    (40, "+1D6"),
    (56, "+2D6"),
)


def damage_bonus(strs, siz):
    total = strs + siz
    if total < 2:  # まだ能力値を決めていないとき
        return "---"
    for upper, bonus in DAMAGE_BONUS_TABLE:
        if total <= upper:
            return bonus
    return f"+{(total - 57) // 16 + 3}D6"


class DecimalIntVar(tk.IntVar):
    """先頭が 0 の数字 ("012" など) も 10 進数として読む IntVar です。

    tk.IntVar は Tcl の規則で "012" を 8 進数 (10) として読み、 "09" ではエラーになります。
    """

    def get(self):
        return int(self._tk.globalgetvar(self._name))


class SkillRow:
    """技能表の 1 行分の変数です。"""

    def __init__(self, skill):
        self.skill = skill
        self.name = tk.StringVar(value=skill.name)
        self.initial = DecimalIntVar(value=skill.initial)
        self.occupation = DecimalIntVar()
        self.interest = DecimalIntVar()
        self.total = DecimalIntVar()

    def recalculate(self):
        self.total.set(self.initial.get() + self.occupation.get() + self.interest.get())

    def sheet_entry(self):
        mark = "★" if self.occupation.get() or self.interest.get() != 0 else ""
        return f"{mark}<{self.skill.label(self.name.get())}:{self.total.get()}%>"


class GCCS(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.geometry("1400x1000")
        self.master.title("Green CoC CharacterMaking Support")

        self.profile = [
            tk.StringVar(value=PROFILE_DEFAULTS.get(row, "")) for row in range(len(PROFILE_LABELS))
        ]
        self.status = {name: DecimalIntVar() for name in STATUS_DICE}
        self.derived = {
            name: tk.StringVar() for name in ("HP", "MP", "SAN", "アイデア", "幸運", "知識")
        }
        self.points = {
            name: tk.StringVar() for name in ("職業P合計", "職業P上限", "興味P合計", "興味P上限")
        }
        self.db = tk.StringVar()
        self.weapons = [[tk.StringVar() for _ in range(4)] for _ in range(5)]
        self.output_name = tk.StringVar(value=" ---")
        self.mini_dice = [DecimalIntVar() for _ in range(3)]
        self.mini_dice_result = tk.StringVar(value="result: ")
        self.skills = {
            category: [SkillRow(skill) for skill in skills]
            for category, (*_, skills) in SKILL_CATEGORIES.items()
        }
        # 初期値が能力値で決まる技能です。
        self.dodge = self.skills["戦闘系技能"][0]
        self.native_language = self.skills["交渉系技能"][5]

        main_frame = tk.Frame(self, relief="groove", borderwidth=2)
        main_frame.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.build_left(main_frame)
        self.build_status(main_frame)
        self.build_skills(main_frame)

        self.recalculate_periodically()

    def build_left(self, main_frame):
        """ダイスボタン、プロフィール、武器、出力ボタンが入る左半分を作ります。"""
        left_frame = tk.Frame(main_frame, height=600)
        left_frame.grid(row=0, column=0, sticky=tk.W, rowspan=5)

        button_frame = tk.Frame(left_frame, relief="groove", borderwidth=2)
        button_frame.grid(row=0, column=0, sticky=tk.W + tk.E, pady=10)
        tk.Button(
            button_frame,
            command=self.roll_status,
            text="DICE ROLL\nステータスをランダム作成する",
            height=4,
        ).pack()

        profile_frame = tk.Frame(left_frame, relief="groove", borderwidth=2)
        profile_frame.grid(row=1, column=0, sticky=tk.W + tk.E, pady=5)
        for row, (text, variable) in enumerate(zip(PROFILE_LABELS, self.profile, strict=True)):
            tk.Label(profile_frame, text=text).grid(row=row, column=0, sticky=tk.W)
            tk.Entry(profile_frame, textvariable=variable).grid(row=row, column=1, sticky=tk.E)

        weapon_db_frame = tk.Frame(left_frame, relief="groove", borderwidth=2)
        weapon_db_frame.grid(row=2, column=0, sticky=tk.W, pady=5)
        db_frame = tk.Frame(weapon_db_frame)
        db_frame.grid(row=0, column=0, sticky=tk.W + tk.E)
        tk.Label(db_frame, text="DB: ").grid(row=0, column=0, sticky=tk.W)
        tk.Label(db_frame, textvariable=self.db).grid(row=0, column=1, sticky=tk.W)
        weapon_frame = tk.Frame(weapon_db_frame)
        weapon_frame.grid(row=1, column=0, sticky=tk.W + tk.E)
        for column, text in enumerate(("名称", "成功率", "ダメージ", "備考")):
            tk.Label(weapon_frame, text=text).grid(row=0, column=column)
        for row, weapon in enumerate(self.weapons, start=1):
            for column, (variable, width) in enumerate(zip(weapon, (10, 6, 6, 10), strict=True)):
                tk.Entry(weapon_frame, textvariable=variable, width=width).grid(
                    row=row, column=column
                )

        button2_frame = tk.Frame(left_frame, relief="groove", borderwidth=2)
        button2_frame.grid(row=3, column=0, sticky=tk.W + tk.E, pady=10)
        tk.Entry(button2_frame, textvariable=self.output_name).pack()
        tk.Label(button2_frame, text="\n↑ 出力ファイル名入力欄 ↑\n").pack()
        tk.Button(
            button2_frame,
            command=self.output,
            text="OUTPUT\n作成したデータをテキストに出力する",
            height=4,
        ).pack()
        # 長いファイル名でも左の列の幅が変わらないよう折り返します。
        self.output_message = tk.Label(button2_frame, wraplength=250)
        self.output_message.pack()

    def build_status(self, main_frame):
        """能力値、派生値、職業ポイントと興味ポイントの欄を作ります。"""
        tk.Frame(main_frame, height=10).grid(row=0, column=1, sticky=tk.E)

        status_frame = tk.Frame(main_frame)
        status_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        for i, (name, variable) in enumerate(self.status.items()):
            tk.Label(status_frame, text=f" {name}:").grid(row=0, column=i * 2)
            tk.Entry(status_frame, textvariable=variable, width=5).grid(row=0, column=i * 2 + 1)

        derived_frame = tk.Frame(main_frame)
        derived_frame.grid(row=2, column=1, sticky=tk.W)
        for i, (name, variable) in enumerate(self.derived.items()):
            tk.Label(derived_frame, text=f" {name}:").grid(row=0, column=i * 2)
            tk.Label(derived_frame, textvariable=variable).grid(row=0, column=i * 2 + 1)

        point_frame = tk.Frame(main_frame)
        point_frame.grid(row=3, column=1, sticky=tk.W)
        texts = (" 職業ポイント:", "/", "興味ポイント:", "/")
        self.point_labels = {}
        for i, (text, (name, variable)) in enumerate(zip(texts, self.points.items(), strict=True)):
            tk.Label(point_frame, text=text).grid(row=0, column=i * 2)
            self.point_labels[name] = tk.Label(point_frame, textvariable=variable)
            self.point_labels[name].grid(row=0, column=i * 2 + 1)
        self.normal_fg = self.point_labels["職業P合計"].cget("fg")

    def build_skills(self, main_frame):
        """技能表と簡易ダイスロールを作ります。"""
        ability_frame = tk.Frame(main_frame, relief="groove", borderwidth=2)
        ability_frame.grid(row=4, column=1, sticky=tk.W + tk.N)
        columns = [tk.Frame(ability_frame) for _ in range(3)]
        for column, (frame, sticky) in enumerate(zip(columns, ("n", "n", "ns"), strict=True)):
            frame.grid(row=0, column=column, sticky=sticky)

        for category, (column, row, sticky, _) in SKILL_CATEGORIES.items():
            frame = tk.LabelFrame(columns[column], text=category, relief="groove", borderwidth=2)
            frame.grid(row=row, column=0, sticky=sticky)
            for i, text in enumerate(SKILL_HEADERS):
                tk.Label(frame, text=text).grid(row=0, column=i)
            # 列ごとに作ります。 Tab キーでは職業P、興味P の列を上から順に移動します。
            rows = list(enumerate(self.skills[category], start=1))
            for i, skill_row in rows:
                if skill_row.skill.prefix is None:
                    tk.Label(frame, text=skill_row.skill.name).grid(row=i, column=0)
                else:
                    tk.Entry(frame, textvariable=skill_row.name, width=10).grid(row=i, column=0)
            for i, skill_row in rows:
                tk.Label(frame, textvariable=skill_row.initial).grid(row=i, column=1)
            for i, skill_row in rows:
                tk.Entry(frame, textvariable=skill_row.occupation, width=5).grid(row=i, column=2)
            for i, skill_row in rows:
                tk.Entry(frame, textvariable=skill_row.interest, width=5).grid(row=i, column=3)
            for i, skill_row in rows:
                tk.Label(frame, textvariable=skill_row.total).grid(row=i, column=4)

        self.build_mini_dice(columns[2])

    def build_mini_dice(self, master):
        """(オマケ) 簡易ダイスロールの欄を作ります。"""
        frame = tk.LabelFrame(
            master, text="(オマケ)簡易ダイスロール", relief="ridge", borderwidth=2
        )
        frame.grid(row=2, column=0, pady=50)
        for i, variable in enumerate(self.mini_dice):
            entry = tk.Entry(frame, textvariable=variable, width=5)
            entry.grid(row=0, column=i * 2, pady=5)
            entry.bind("<Return>", self.roll_mini_dice)
        tk.Label(frame, text="D").grid(row=0, column=1, pady=5)
        tk.Label(frame, text="+").grid(row=0, column=3, pady=5)
        tk.Entry(frame, textvariable=self.mini_dice_result).grid(row=1, column=0, columnspan=5)
        tk.Label(frame, text=" 数値を打ち込んだらエンターキーを押してね。").grid(
            row=2, column=0, columnspan=6
        )

    def roll_status(self):
        for name, dice in STATUS_DICE.items():
            self.status[name].set(dice_roll(*dice))
        self.recalculate_if_possible()

    def roll_mini_dice(self, event):
        try:
            count, sides, bonus = (variable.get() for variable in self.mini_dice)
            # 個数が多すぎると画面が固まるので上限を設けます。
            if not (0 <= count <= MINI_DICE_MAX_COUNT and sides >= 1):
                raise ValueError
            # 桁数が大きすぎる数は文字列にするときに ValueError になります。
            result = f"result: {dice_roll(count, sides, bonus)}"
        except ValueError:
            result = "result: 入力エラー"
        self.mini_dice_result.set(result)

    def recalculate(self):
        con, siz, pow_, dex, int_, edu = (
            self.status[name].get() for name in ("CON", "SIZ", "POW", "DEX", "INT", "EDU")
        )
        self.derived["HP"].set((con + siz + 1) // 2)
        self.derived["MP"].set(pow_)
        self.derived["SAN"].set(pow_ * 5)
        self.derived["アイデア"].set(int_ * 5)
        self.derived["幸運"].set(pow_ * 5)
        self.derived["知識"].set(edu * 5)
        occupation_limit, interest_limit = edu * 20, int_ * 10
        self.points["職業P上限"].set(occupation_limit)
        self.points["興味P上限"].set(interest_limit)
        self.db.set(damage_bonus(self.status["STR"].get(), siz))
        rows = [row for category in self.skills.values() for row in category]
        occupation_used = sum(row.occupation.get() for row in rows)
        interest_used = sum(row.interest.get() for row in rows)
        self.points["職業P合計"].set(occupation_used)
        self.points["興味P合計"].set(interest_used)
        # 上限より多く振ったときは赤くして知らせます (振ること自体は止めません)。
        for name, over in (
            ("職業P合計", occupation_used > occupation_limit),
            ("興味P合計", interest_used > interest_limit),
        ):
            self.point_labels[name].config(fg="red" if over else self.normal_fg)
        self.dodge.initial.set(dex * 2)
        self.native_language.initial.set(edu * 5)
        for row in rows:
            row.recalculate()

    def recalculate_if_possible(self):
        # 入力途中で欄が空や数字以外のときは計算しません (次の周期で計算し直します)。
        with contextlib.suppress(ValueError):
            self.recalculate()

    def recalculate_periodically(self):
        self.recalculate_if_possible()
        self.after(500, self.recalculate_periodically)

    def sheet_text(self):
        """OUTPUT で書き出すキャラシートのテキストを返します。"""
        p = [variable.get() for variable in self.profile]
        d = {name: variable.get() for name, variable in self.derived.items()}
        s = {name: variable.get() for name, variable in self.status.items()}
        text = (
            f"\nキャラ名: {p[0]}\n職業: {p[1]} / 年齢: {p[2]} / 性別: {p[3]} / 出身: {p[4]} \n\n"
            "● 持ち物 ●\n"
            + "".join(f" {line}\n" for line in p[5:9])
            + "● メモ ●\n"
            + "".join(f" {line}\n" for line in p[9:13])
        )
        text += f"\n● 能力値 ●\n HP:{d['HP']}\n MP:{d['MP']}\n SAN:{d['SAN']}\n\n "
        text += "  ".join(f"{name}:{value}" for name, value in s.items()) + "\n\n"
        text += (
            f"●　技能　●\n アイデア:{d['アイデア']}%   幸運:{d['幸運']}%   知識:{d['知識']}%\n\n"
        )
        text += "\n"
        for category, rows in self.skills.items():
            text += f"------------------------ {category} ------------------------\n"
            entries = [row.sheet_entry() for row in rows]
            for i in range(0, len(entries), 3):
                text += " " + "   ".join(entries[i : i + 3]) + "\n"
            text += "\n"
        text += f"●　武器　●\n ダメージボーナス:{self.db.get()}\n 【名称 成功率 ダメージ 備考】\n"
        for name, rate, damage, note in self.weapons:
            text += f" {name.get()} {rate.get()}% {damage.get()} {note.get()}\n"
        return text + "\n"

    def output(self):
        name = self.output_name.get().strip()
        if not name or any(c in name for c in "/\\\0"):
            self.show_output_message("ファイル名を入れてね (/ と \\ は使えないよ)", error=True)
            return
        try:
            self.recalculate()
            text = self.sheet_text()
        except ValueError:
            self.show_output_message("数字の欄に数字以外が入っているよ", error=True)
            return
        try:
            with open(f"{name}.txt", "a", encoding="utf-8") as w:
                w.write(text)
        except OSError as e:
            self.show_output_message(f"書き出せなかったよ: {e.strerror}", error=True)
            return
        shown = name if len(name) <= 24 else name[:23] + "…"
        self.show_output_message(f"{shown}.txt に書き出したよ")

    def show_output_message(self, text, error=False):
        self.output_message.config(text=text, fg="red" if error else self.normal_fg)


if __name__ == "__main__":
    gccs = GCCS()
    gccs.pack()
    gccs.mainloop()
