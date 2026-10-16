"""GUI テスト用のドライバです。

ウィジェットはラベルの文字列とグリッド位置で探します。
実装の変数名に依存しないので、リファクタリングの前後で同じテストを使えます。
"""

import time
import tkinter as tk

import pytest

from CocCharamakeSupport import GCCS

# 能力値ダイスを振ったあとに使うキャラクターの能力値です。
SAMPLE_STATUS = {
    "STR": 12,
    "CON": 11,
    "POW": 13,
    "DEX": 14,
    "APP": 9,
    "SIZ": 13,
    "INT": 16,
    "EDU": 18,
}


class Driver:
    def __init__(self, root, app):
        self.root = root
        self.app = app

    def pump(self, timeout=5.0):
        """いま予約されている after() (自動再計算) が一巡するまでイベントを処理します。"""
        pending = set(self.root.after_info())
        end = time.monotonic() + timeout
        while pending & set(self.root.after_info()):
            if time.monotonic() > end:
                raise TimeoutError("自動再計算が走りません")
            self.root.update()
            time.sleep(0.01)

    def widgets(self, widget=None):
        widget = widget or self.app
        for child in widget.winfo_children():
            yield child
            yield from self.widgets(child)

    def find(self, cls, text):
        for widget in self.widgets():
            if isinstance(widget, cls) and widget.cget("text") == text:
                return widget
        raise LookupError(f"{cls.__name__} {text!r} が見つかりません")

    @staticmethod
    def cell(frame, row, column):
        (widget,) = frame.grid_slaves(row=row, column=column)
        return widget

    @staticmethod
    def type_into(entry, value):
        entry.delete(0, "end")
        entry.insert(0, str(value))

    def status_entry(self, name):
        label = self.find(tk.Label, f" {name}:")
        return self.cell(label.master, 0, label.grid_info()["column"] + 1)

    def status_value(self, name):
        """HP や アイデア などの計算結果のラベルの値を返します。"""
        label = self.find(tk.Label, f" {name}:")
        return str(self.cell(label.master, 0, label.grid_info()["column"] + 1).cget("text"))

    def profile_entry(self, row):
        label = self.find(tk.Label, "キャラ名")
        return self.cell(label.master, row, 1)

    def weapon_entry(self, row, column):
        label = self.find(tk.Label, "名称")
        return self.cell(label.master, row, column)

    def skill_cell(self, category, row, column):
        """技能表のセルを返します。 column は 0: 技能名, 2: 職業P, 3: 興味P, 4: 合計 です。"""
        return self.cell(self.find(tk.LabelFrame, category), row, column)

    def skill_total(self, category, row):
        return str(self.skill_cell(category, row, 4).cget("text"))

    def output_name_entry(self):
        label = self.find(tk.Label, "\n↑ 出力ファイル名入力欄 ↑\n")
        return label.master.pack_slaves()[0]

    def output_message(self):
        """OUTPUT ボタンの下に出るメッセージを返します。"""
        label = self.find(tk.Label, "\n↑ 出力ファイル名入力欄 ↑\n")
        return label.master.pack_slaves()[3].cget("text")

    def press(self, text_prefix):
        for widget in self.widgets():
            if isinstance(widget, tk.Button) and widget.cget("text").startswith(text_prefix):
                widget.invoke()
                return
        raise LookupError(f"ボタン {text_prefix!r} が見つかりません")

    def mini_dice_entry(self, column):
        return self.cell(self.find(tk.LabelFrame, "(オマケ)簡易ダイスロール"), 0, column)

    def roll_mini_dice(self, count, sides, bonus):
        for column, value in zip((0, 2, 4), (count, sides, bonus), strict=True):
            self.type_into(self.mini_dice_entry(column), value)
        # キーイベントはフォーカスのある欄に届くので、先にフォーカスを当てます。
        self.mini_dice_entry(0).focus_force()
        self.root.update()
        self.mini_dice_entry(0).event_generate("<Return>")
        return self.mini_dice_result()

    def mini_dice_result(self):
        return self.cell(self.find(tk.LabelFrame, "(オマケ)簡易ダイスロール"), 1, 0).get()

    def fill_sample_character(self):
        """ゴールデンファイルを作ったときと同じ入力をします。"""
        for name, value in SAMPLE_STATUS.items():
            self.type_into(self.status_entry(name), value)
        profile = ("緑川 翠", "探偵", "27", "女", "沖縄", "ルーペ", "懐中電灯", "", "", "猫好き")
        for row, value in enumerate(profile):
            self.type_into(self.profile_entry(row), value)
        self.type_into(self.weapon_entry(1, 0), "こぶし")
        self.type_into(self.weapon_entry(1, 1), "50")
        self.type_into(self.weapon_entry(1, 2), "1D3+DB")
        self.type_into(self.weapon_entry(2, 0), "拳銃")
        self.type_into(self.weapon_entry(2, 1), "60")
        self.type_into(self.weapon_entry(2, 2), "1D10")
        self.type_into(self.weapon_entry(2, 3), ".38口径")
        points = (
            ("探索系技能", 1, 2, 20),
            ("探索系技能", 12, 2, 40),
            ("探索系技能", 12, 3, 10),
            ("戦闘系技能", 1, 3, 20),
            ("戦闘系技能", 8, 2, 40),
            ("交渉系技能", 3, 3, 15),
            ("交渉系技能", 7, 2, 30),
            ("知識系技能", 4, 3, 5),
            ("知識系技能", 18, 2, 20),
            ("行動系技能", 1, 2, 30),
            ("行動系技能", 10, 3, 20),
            ("行動系技能", 11, 2, 10),
            ("任意の技能", 1, 2, 25),
            ("任意の技能", 2, 3, 5),
        )
        for category, row, column, value in points:
            self.type_into(self.skill_cell(category, row, column), value)
        names = (
            ("交渉系技能", 6, "日本語"),
            ("交渉系技能", 7, "英語"),
            ("知識系技能", 18, "絵画"),
            ("行動系技能", 10, "料理"),
            ("行動系技能", 11, "船舶"),
            ("任意の技能", 1, "写真鑑定"),
            ("任意の技能", 2, "ダンス"),
        )
        for category, row, value in names:
            self.type_into(self.skill_cell(category, row, 0), value)
        self.type_into(self.output_name_entry(), "midorikawa")


@pytest.fixture
def gccs(monkeypatch, tmp_path):
    """アプリを起動し、 OUTPUT の出力先を tmp_path にします。"""
    monkeypatch.chdir(tmp_path)
    root = tk.Tk()
    # ボタンやキー入力から呼ばれた処理の例外は Tk が表示するだけで止まらないので、
    # 記録しておいてテストを失敗にします。
    callback_errors = []
    root.report_callback_exception = lambda *exc_info: callback_errors.append(exc_info[1])
    try:
        app = GCCS(root)
        app.pack()
        root.update()
        yield Driver(root, app)
        assert callback_errors == []
    finally:
        for after_id in root.after_info():
            root.tk.call("after", "cancel", after_id)
        root.destroy()
