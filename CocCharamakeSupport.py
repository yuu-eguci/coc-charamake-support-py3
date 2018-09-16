# coding: utf-8

'''CocCharamakeSupport

tkinterを使ってるのでpython3専用。
CoC TRPG キャラメイク用ツール。
'''

import tkinter as Tk
import sys, random, math

class GCCS(Tk.Frame):
    def __init__(self, master = None):
        Tk.Frame.__init__(self, master)
        self.master.geometry('1400x1000')
        self.master.title('Green CoC CharacterMaking Support')

        # StringVar たち
        (a, b, c, d, e, f, g, h, i, j, k, l, m, strs, con, pow, dex, app, siz, int, edu, hp, 
                mp, san, idea, luck, knowledge, edu_point, int_point, edu_point_total, 
                int_point_total, db, w00, w01, w02, w03, w10, w11, w12, w13, w20, w21, w22, w23, 
                w30, w31, w32, w33, w40, w41, w42, w43) = (Tk.StringVar(), Tk.StringVar(), 
                Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), 
                Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), 
                Tk.StringVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), 
                Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), 
                Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), 
                Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), 
                Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), 
                Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), 
                Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), Tk.StringVar(), 
                Tk.StringVar(), Tk.StringVar(), Tk.StringVar())
        f.set(' ---')
        j.set(' ---')
        strs.set(0); con.set(0); pow.set(0); dex.set(0); app.set(0); siz.set(0); int.set(0); edu.set(0)

        def output():
            # 振った技能には★をつける
            se1, se2, se3, se4, se5, se6, se7, se8, se9, se10, se11, se12 = ('', 
                '', '', '', '', '', '', '', '', '', '', '')
            be1, be2, be3, be4, be5, be6, be7, be8, be9, be10, be11, be12 = ('', 
                '', '', '', '', '', '', '', '', '', '', '')
            ne1, ne2, ne3, ne4, ne5, ne6, ne7 = ('', '', '', '', '', '', '')
            (ke1, ke2, ke3, ke4, ke5, ke6, ke7, ke8, ke9, ke10, ke11, ke12, 
                ke13, ke14, ke15, ke16, ke17, ke18) = ('', '', '', '', '', '', 
                '', '', '', '', '', '', '', '', '', '', '', '')
            ae1, ae2, ae3, ae4, ae5, ae6, ae7, ae8, ae9, ae10, ae11 = ('', '', 
                '', '', '', '', '', '', '', '', '')
            oe1, oe2, oe3 = ('', '', '')
            se_list = [se1, se2, se3, se4, se5, se6, se7, se8, se9, se10, se11, se12]
            be_list = [be1, be2, be3, be4, be5, be6, be7, be8, be9, be10, be11, be12]
            ne_list = [ne1, ne2, ne3, ne4, ne5, ne6, ne7]
            ke_list = [ke1, ke2, ke3, ke4, ke5, ke6, ke7, ke8, ke9, ke10, ke11, ke12, 
            ke13, ke14, ke15, ke16, ke17, ke18]
            ae_list = [ae1, ae2, ae3, ae4, ae5, ae6, ae7, ae8, ae9, ae10, ae11]
            oe_list = [oe1, oe2, oe3]
            for foo in range(12):
                if sb_list[foo].get() or sc_list[foo].get() != 0:
                    se_list[foo] = '★'
            for foo in range(12):
                if bb_list[foo].get() or bc_list[foo].get() != 0:
                    be_list[foo] = '★'
            for foo in range(7):
                if nb_list[foo].get() or nc_list[foo].get() != 0:
                    ne_list[foo] = '★'
            for foo in range(18):
                if kb_list[foo].get() or kc_list[foo].get() != 0:
                    ke_list[foo] = '★'
            for foo in range(11):
                if ab_list[foo].get() or ac_list[foo].get() != 0:
                    ae_list[foo] = '★'
            for foo in range(3):
                if ob_list[foo].get() or oc_list[foo].get() != 0:
                    oe_list[foo] = '★'
            content1 = ('\nキャラ名: %s\n職業: %s / 年齢: %s / 性別: %s / 出身: %s \n\n● 持ち物 ●\n %s\n %s\n %s\n %s\n● メモ ●\n %s\n %s\n %s\n %s\n' % (a.get(), 
                    b.get(), c.get(), d.get(), e.get(), f.get(), g.get(), h.get(), i.get(), 
                    j.get(), k.get(), l.get(), m.get()))
            content2 = ('\n● 能力値 ●\n HP:%s\n MP:%s\n SAN:%s\n\n STR:%s  CON:%s  POW:%s  DEX:%s  APP:%s  SIZ:%s  INT:%s  EDU:%s\n\n' % (hp.get(), mp.get(), 
                    san.get(), strs.get(), con.get(), pow.get(), dex.get(), app.get(), 
                    siz.get(), int.get(), edu.get()))
            content3 = ('●　技能　●\n アイデア:%s%%   幸運:%s%%   知識:%s%%\n\n' % (idea.get(), 
                luck.get(), knowledge.get()))
            content_s = ('''
------------------------ 探索系技能 ------------------------
 %s<応急手当:%s%%>   %s<鍵開け:%s%%>   %s<隠す:%s%%>
 %s<隠れる:%s%%>   %s<聞き耳:%s%%>   %s<忍び歩き:%s%%>
 %s<写真術:%s%%>   %s<精神分析:%s%%>   %s<追跡:%s%%>
 %s<登攀:%s%%>   %s<図書館:%s%%>   %s<目星:%s%%>

------------------------ 戦闘系技能 ------------------------
 %s<回避:%s%%>   %s<キック:%s%%>   %s<組付き:%s%%>
 %s<こぶし(パンチ):%s%%>   %s<頭突き:%s%%>   %s<投擲:%s%%>
 %s<マーシャルアーツ:%s%%>   %s<拳銃:%s%%>   %s<サブマシンガン:%s%%>
 %s<ショットガン:%s%%>   %s<マシンガン:%s%%>   %s<ライフル:%s%%>

------------------------ 交渉系技能 ------------------------
 %s<言いくるめ:%s%%>   %s<信用:%s%%>   %s<説得:%s%%>
 %s<値切り:%s%%>   %s<心理学:%s%%>   %s<母国語 %s:%s%%>
 %s<外国語 %s:%s%%>

------------------------ 知識系技能 ------------------------
 %s<医学:%s%%>   %s<オカルト:%s%%>   %s<科学:%s%%>
 %s<クトゥルフ神話:%s%%>   %s<経理:%s%%>   %s<考古学:%s%%>
 %s<コンピュータ:%s%%>   %s<人類学:%s%%>   %s<生物学:%s%%>
 %s<地質学:%s%%>   %s<電子工学:%s%%>   %s<天文学:%s%%>
 %s<博物学:%s%%>   %s<物理学:%s%%>   %s<法律:%s%%>
 %s<薬学:%s%%>   %s<歴史:%s%%>   %s<芸術 %s:%s%%>

------------------------ 行動系技能 ------------------------
 %s<運転:%s%%>   %s<機械修理:%s%%>   %s<重機械操作:%s%%>
 %s<乗馬:%s%%>   %s<水泳:%s%%>   %s<跳躍:%s%%>
 %s<電気修理:%s%%>   %s<ナビゲート:%s%%>   %s<変装:%s%%>
 %s<制作 %s:%s%%>   %s<操縦 %s:%s%%>

------------------------ 任意の技能 ------------------------
 %s<%s:%s%%>   %s<%s:%s%%>   %s<%s:%s%%>

''' % (se_list[0], sd1.get(), se_list[1], sd2.get(), se_list[2], sd3.get(), se_list[3], 
    sd4.get(), se_list[4], sd5.get(), se_list[5], sd6.get(), se_list[6], sd7.get(), 
    se_list[7], sd8.get(), se_list[8], sd9.get(), se_list[9], sd10.get(), se_list[10], 
    sd11.get(), se_list[11], sd12.get(), be_list[0], bd1.get(), be_list[1], bd2.get(), 
    be_list[2], bd3.get(), be_list[3], bd4.get(), be_list[4], bd5.get(), be_list[5], 
    bd6.get(), be_list[6], bd7.get(), be_list[7], bd8.get(), be_list[8], bd9.get(), 
    be_list[9], bd10.get(), be_list[10], bd11.get(), be_list[11], bd12.get(), 
    ne_list[0], nd1.get(), ne_list[1], nd2.get(), ne_list[2], nd3.get(), ne_list[3], 
    nd4.get(), ne_list[4], nd5.get(), ne_list[5], bokokugo.get(), nd6.get(), ne_list[6], 
    gaikokugo.get(), nd7.get(), ke_list[0], kd1.get(), ke_list[1], kd2.get(), ke_list[2], 
    kd3.get(), ke_list[3], kd4.get(), ke_list[4], kd5.get(), ke_list[5], kd6.get(), 
    ke_list[6], kd7.get(), ke_list[7], kd8.get(), ke_list[8], kd9.get(), ke_list[9], 
    kd10.get(), ke_list[10], kd11.get(), ke_list[11], kd12.get(), ke_list[12], 
    kd13.get(), ke_list[13], kd14.get(), ke_list[14], kd15.get(), ke_list[15], 
    kd16.get(), ke_list[16], kd17.get(), ke_list[17], geijutsu.get(), kd18.get(), 
    ae_list[0], ad1.get(), ae_list[1], ad2.get(), ae_list[2], ad3.get(), ae_list[3], 
    ad4.get(), ae_list[4], ad5.get(), ae_list[5], ad6.get(), ae_list[6], ad7.get(), 
    ae_list[7], ad8.get(), ae_list[8], ad9.get(), ae_list[9], seisaku.get(), ad10.get(), 
    ae_list[10], soujuu.get(), ad11.get(), oe_list[0], option_namae1.get(), od1.get(), 
    oe_list[1], option_namae2.get(), od2.get(), oe_list[2], option_namae3.get(), od3.get()))
            content4 = ('●　武器　●\n ダメージボーナス:%s\n 【名称 成功率 ダメージ 備考】\n %s %s%% %s %s\n %s %s%% %s %s\n %s %s%% %s %s\n %s %s%% %s %s\n %s %s%% %s %s\n\n' % (db.get(), w00.get(), w01.get(), w02.get(), 
                    w03.get(), w10.get(), w11.get(), w12.get(), w13.get(), w20.get(), 
                    w21.get(), w22.get(), w23.get(), w30.get(), w31.get(), w32.get(), 
                    w33.get(), w40.get(), w41.get(), w42.get(), w43.get()))
            w = open(output_name.get() + '.txt', 'a')
            w.write(content1)
            w.write(content2)
            w.write(content3)
            w.write(content_s)
            w.write(content4)
            w.close()

        def damage_bonus(strs, siz):
            x = strs + siz
            if 1 < x < 13:
                return '-1D6'
            elif 12 < x < 17:
                return '-1D4'
            elif 16 < x < 25:
                return '0'
            elif 24 < x < 33:
                return '+1D4'
            elif 32 < x < 41:
                return '+1D6'
            elif 40 < x < 57:
                return '+2D6'
            else:
                return '+3D6'

        def dice_roll(a, b, e = 0): # aDb の結果を出す
            d = 0
            for i in range(a):
                c = random.randint(1, b)
                d += c
            return d + e

        def dice_button():
            strs.set(dice_roll(3, 6))
            con.set(dice_roll(3, 6))
            pow.set(dice_roll(3, 6))
            dex.set(dice_roll(3, 6))
            app.set(dice_roll(3, 6))
            siz.set(dice_roll(2, 6) + 6)
            int.set(dice_roll(2, 6) + 6)
            edu.set(dice_roll(3, 6) + 3)
            reload()

        # 全体のフレーム
        main_frame = Tk.Frame(self, relief = 'groove', borderwidth = 2)
        main_frame.grid(row = 0, column = 0, sticky = Tk.W + Tk.E)

        # プロフ欄と武器情報が入る左半分のフレーム
        left_frame = Tk.Frame(main_frame, height = 600)
        left_frame.grid(row = 0, column = 0, sticky = Tk.W, rowspan = 5)

        # ボタン1
        button_frame = Tk.Frame(left_frame, relief = 'groove', borderwidth = 2)
        button_frame.grid(row = 0, column = 0, sticky = Tk.W + Tk.E, pady = 10)
        # ステータス欄に数字を自動的にハメるボタン
        dice_button = Tk.Button(button_frame, command = dice_button, 
            text = 'DICE ROLL\nステータスをランダム作成する', height = 4)
        dice_button.pack()

        # プロフィール欄が入るフレーム
        profile_frame = Tk.Frame(left_frame, relief = 'groove', borderwidth = 2)
        profile_frame.grid(row = 1, column = 0, sticky = Tk.W + Tk.E, pady = 5)
        # プロフィール欄の項目リスト
        profile_list = ('キャラ名', '職業', '年齢', '性別', '出身', '持ち物', '', 
            '', '', 'メモ', '', '', '')
        # プロフィール欄の textvariable を受け取る変数リスト
        profile_list2 = (a, b, c, d, e, f, g, h, i, j, k, l, m)
        # プロフィール欄のラベルとエントリーを配置する
        for foo in range(13):
            profile_label = Tk.Label(profile_frame, text = profile_list[foo])
            profile_label.grid(row = foo, column = 0, sticky = Tk.W)
            profile_entry = Tk.Entry(profile_frame, textvariable = profile_list2[foo])
            profile_entry.grid(row = foo, column = 1, sticky = Tk.E)

        # 武器情報とかが入るフレーム
        weapon_db_frame = Tk.Frame(left_frame, relief = 'groove', borderwidth = 2)
        weapon_db_frame.grid(row = 2, column = 0, sticky = Tk.W, pady = 5)
        # DBが入るフレーム
        db_frame = Tk.Frame(weapon_db_frame)
        db_frame.grid(row = 0, column = 0, sticky = Tk.W + Tk.E)
        db_label = Tk.Label(db_frame, text = 'DB: ')
        db_label.grid(row = 0, column = 0, sticky = Tk.W)
        db_label2 = Tk.Label(db_frame, textvariable = db)
        db_label2.grid(row = 0, column = 1, sticky = Tk.W)
        # 武器情報が入るフレーム
        weapon_frame = Tk.Frame(weapon_db_frame)
        weapon_frame.grid(row = 1, column = 0, sticky = Tk.W + Tk.E)
        # フレームの0行目に名前のラベルをよっつ
        weapon_name_list = ('名称', '成功率', 'ダメージ', '備考')
        for foo in range(4):
            weapon_4labels = Tk.Label(weapon_frame, text = weapon_name_list[foo])
            weapon_4labels.grid(row = 0, column = foo)
        # フレームの0-5行にエントリーを4個ずつ
        weapon_entry_textvariable_list0 = (0, w00, w01, w02, w03)
        weapon_entry_textvariable_list1 = (0, w10, w11, w12, w13)
        weapon_entry_textvariable_list2 = (0, w20, w21, w22, w23)
        weapon_entry_textvariable_list3 = (0, w30, w31, w32, w33)
        weapon_entry_textvariable_list4 = (0, w40, w41, w42, w43)

        def baz(a):
            if a == 1: return 10
            elif a == 2: return 6 
            elif a == 3: return 6
            else: return 10

        for foo in range(1, 5):
            weapon_entry1 = Tk.Entry(weapon_frame, 
                textvariable = weapon_entry_textvariable_list0[foo], width = baz(foo))
            weapon_entry1.grid(row = 1, column = foo - 1)
        for foo in range(1, 5):
            weapon_entry2 = Tk.Entry(weapon_frame, 
                textvariable = weapon_entry_textvariable_list1[foo], width = baz(foo))
            weapon_entry2.grid(row = 2, column = foo - 1)
        for foo in range(1, 5):
            weapon_entry3 = Tk.Entry(weapon_frame, 
                textvariable = weapon_entry_textvariable_list2[foo], width = baz(foo))
            weapon_entry3.grid(row = 3, column = foo - 1)
        for foo in range(1, 5):
            weapon_entry4 = Tk.Entry(weapon_frame, 
                textvariable = weapon_entry_textvariable_list3[foo], width = baz(foo))
            weapon_entry4.grid(row = 4, column = foo - 1)
        for foo in range(1, 5):
            weapon_entry5 = Tk.Entry(weapon_frame, 
                textvariable = weapon_entry_textvariable_list4[foo], width = baz(foo))
            weapon_entry5.grid(row = 5, column = foo - 1)

        # ボタン2
        button2_frame = Tk.Frame(left_frame, relief = 'groove', borderwidth = 2)
        button2_frame.grid(row = 3, column = 0, sticky = Tk.W + Tk.E, pady = 10)
        # 出力ファイル名入力欄
        output_name = Tk.StringVar()
        output_name.set(' ---')
        output_entry = Tk.Entry(button2_frame, textvariable = output_name)
        output_entry.pack()
        output_label = Tk.Label(button2_frame, text = '\n↑ 出力ファイル名入力欄 ↑\n')
        output_label.pack()
        # 出力ボタン
        output_button = Tk.Button(button2_frame, command = output, 
            text = 'OUTPUT\n作成したデータをテキストに出力する', height = 4)
        output_button.pack()

        # 右の上のフレーム
        empty_frame = Tk.Frame(main_frame, height = 10)
        empty_frame.grid(row = 0, column = 1, sticky = Tk.E)

        # ステータスが入るフレーム
        status_frame = Tk.Frame(main_frame)
        status_frame.grid(row = 1, column = 1, sticky = Tk.W, pady = 5)
        # ステータス欄の項目リスト
        status_list = (' STR:', ' CON:', ' POW:', ' DEX:', ' APP:', ' SIZ:', ' INT:', ' EDU:')
        # ステータス欄の textvariable を受け取る変数リスト
        status_list2 = (strs, con, pow, dex, app, siz, int, edu)
        # ステータス欄のラベルとエントリーを配置する
        foo = bar = 0
        while foo < 16:
            status_label = Tk.Label(status_frame, text = status_list[foo - bar])
            status_label.grid(row = 0, column = foo)
            foo += 2
            bar += 1
        foo = bar = 1
        while foo < 17:
            status_entry = Tk.Entry(status_frame, textvariable = status_list2[foo - bar], width = 5)
            status_entry.grid(row = 0, column = foo)
            foo += 2
            bar += 1

        # ステータスその2が入るフレーム
        status2_frame = Tk.Frame(main_frame)
        status2_frame.grid(row = 2, column = 1, sticky = Tk.W)
        # ステータスその2の項目リスト
        status2_list = (' HP:', ' MP:', ' SAN:', ' アイデア:', ' 幸運:', ' 知識:')
        # ステータスその2の textvariable を受け取る変数リスト
        status2_list2 = (hp, mp, san, idea, luck, knowledge)
        # ステータスその2のラベルと変数ラベルを配置する
        foo = bar = 0
        while foo < 12:
            status2_label = Tk.Label(status2_frame, text = status2_list[foo - bar])
            status2_label.grid(row = 0, column = foo)
            foo += 2
            bar += 1
        foo = bar = 1
        while foo < 13:
            status2_label2 = Tk.Label(status2_frame, textvariable = status2_list2[foo - bar])
            status2_label2.grid(row = 0, column = foo)
            foo += 2
            bar += 1

        # 職業ポイント、興味ポイントが入るフレーム
        point_frame = Tk.Frame(main_frame)
        point_frame.grid(row = 3, column = 1, sticky = Tk.W)
        # 変化のないラベルのリスト
        point_list = (' 職業ポイント:', '/', '興味ポイント:', '/')
        # 変化するラベルのリスト
        point_list2 = (edu_point_total, edu_point, int_point_total, int_point)
        # ラベルを配置する
        foo = bar = 0
        while foo < 8:
            point_label = Tk.Label(point_frame, text = point_list[foo - bar])
            point_label.grid(row = 0, column = foo)
            foo += 2
            bar += 1
        foo = bar = 1
        while foo < 9:
            point_label2 = Tk.Label(point_frame, textvariable = point_list2[foo - bar])
            point_label2.grid(row = 0, column = foo)
            foo += 2
            bar += 1

        # いよいよやってきたぜ、技能入力フレーム
        ability_frame = Tk.Frame(main_frame, relief = 'groove', borderwidth = 2)
        ability_frame.grid(row = 4, column = 1, sticky = Tk.W + Tk.N)
        frame_for_search_battle = Tk.Frame(ability_frame)
        frame_for_search_battle.grid(row = 0, column = 0, sticky = Tk.N)
        frame_for_negotiation_knowledge = Tk.Frame(ability_frame)
        frame_for_negotiation_knowledge.grid(row = 0, column = 1, sticky = Tk.N)
        frame_for_action_option = Tk.Frame(ability_frame)
        frame_for_action_option.grid(row = 0, column = 2, sticky = Tk.N + Tk.S)
        # ラベル5つ
        ability_label_list = ('     技能名     ', '初期値', '職業P', '興味P', '合計')

        # 探索系技能のフレーム
        search_frame = Tk.LabelFrame(frame_for_search_battle, text = '探索系技能', 
            relief = 'groove', borderwidth = 2)
        search_frame.grid(row = 0, column = 0, sticky = Tk.E + Tk.W + Tk.N)
        # 探索系技能用の変数
        # 初期値
        sa1, sa2, sa3, sa4, sa5, sa6, sa7, sa8, sa9, sa10, sa11, sa12 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 職業ポイント
        sb1, sb2, sb3, sb4, sb5, sb6, sb7, sb8, sb9, sb10, sb11, sb12 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 興味ポイント
        sc1, sc2, sc3, sc4, sc5, sc6, sc7, sc8, sc9, sc10, sc11, sc12 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 合計
        sd1, sd2, sd3, sd4, sd5, sd6, sd7, sd8, sd9, sd10, sd11, sd12 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 探索系技能の種類
        search_name_list = ('応急手当', '鍵開け', '隠す', '隠れる', '聞き耳', '忍び歩き', '写真術', '精神分析', '追跡', '登攀', '図書館', '目星')
        # まず上の5ラベル
        for foo in range(5):
            search_5labels = Tk.Label(search_frame, text = ability_label_list[foo])
            search_5labels.grid(row = 0, column = foo)
        # 探索系技能の種類のラベル
        for foo in range(1, 13):
            search_name_label = Tk.Label(search_frame, text = search_name_list[foo - 1])
            search_name_label.grid(row = foo, column = 0)
        # 初期値のラベル
        sa_list = (sa1, sa2, sa3, sa4, sa5, sa6, sa7, sa8, sa9, sa10, sa11, sa12)
        sa_list2 = (30, 1, 15, 10, 25, 10, 10, 1, 10, 40, 25, 25)
        for foo in range(12):
            sa_list[foo].set(sa_list2[foo])
        for foo in range(1, 13):
            search_ini_label = Tk.Label(search_frame, textvariable = sa_list[foo - 1])
            search_ini_label.grid(row = foo, column = 1)
        # 職Pのエントリー
        sb_list = (sb1, sb2, sb3, sb4, sb5, sb6, sb7, sb8, sb9, sb10, sb11, sb12)
        for foo in range(1, 13):
            search_edu_entry = Tk.Entry(search_frame, textvariable = sb_list[foo - 1], width = 5)
            search_edu_entry.grid(row = foo, column = 2)
        # 興味Pのエントリー
        sc_list = (sc1, sc2, sc3, sc4, sc5, sc6, sc7, sc8, sc9, sc10, sc11, sc12)
        for foo in range(1, 13):
            search_int_entry = Tk.Entry(search_frame, textvariable = sc_list[foo - 1], width = 5)
            search_int_entry.grid(row = foo, column = 3)
        # 合計のラベル
        sd_list = (sd1, sd2, sd3, sd4, sd5, sd6, sd7, sd8, sd9, sd10, sd11, sd12)
        for foo in range(1, 13):
            search_total_label = Tk.Label(search_frame, textvariable = sd_list[foo - 1])
            search_total_label.grid(row = foo, column = 4)

        # 戦闘系技能のフレーム
        battle_frame = Tk.LabelFrame(frame_for_search_battle, text = '戦闘系技能', relief = 'groove', borderwidth = 2)
        battle_frame.grid(row = 1, column = 0, sticky = Tk.E + Tk.W + Tk.N)
        # 戦闘系技能の変数
        # 初期値
        ba1, ba2, ba3, ba4, ba5, ba6, ba7, ba8, ba9, ba10, ba11, ba12 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 職業ポイント
        bb1, bb2, bb3, bb4, bb5, bb6, bb7, bb8, bb9, bb10, bb11, bb12 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 興味ポイント
        bc1, bc2, bc3, bc4, bc5, bc6, bc7, bc8, bc9, bc10, bc11, bc12 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 合計
        bd1, bd2, bd3, bd4, bd5, bd6, bd7, bd8, bd9, bd10, bd11, bd12 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 戦闘系技能の種類
        battle_name_list = ('回避', 'キック', '組付き', 'こぶし(パンチ)', '頭突き', '投擲', 'マーシャルアーツ', '拳銃', 'サブマシンガン', 'ショットガン', 'マシンガン', 'ライフル')
        for foo in range(5):
            battle_5labels = Tk.Label(battle_frame, text = ability_label_list[foo])
            battle_5labels.grid(row = 0, column = foo)
        # 探索系技能の種類のラベル
        for foo in range(1, 13):
            battle_name_label = Tk.Label(battle_frame, text = battle_name_list[foo - 1])
            battle_name_label.grid(row = foo, column = 0)
        # 初期値のラベル
        ba_list = (ba1, ba2, ba3, ba4, ba5, ba6, ba7, ba8, ba9, ba10, ba11, ba12)
        ba_list2 = (0, 25, 25, 50, 10, 25, 1, 20, 15, 30, 15, 25)
        for foo in range(12):
            ba_list[foo].set(ba_list2[foo])
        for foo in range(1, 13):
            battle_ini_label = Tk.Label(battle_frame, textvariable = ba_list[foo - 1])
            battle_ini_label.grid(row = foo, column = 1)
        # 職Pのエントリー
        bb_list = (bb1, bb2, bb3, bb4, bb5, bb6, bb7, bb8, bb9, bb10, bb11, bb12)
        for foo in range(1, 13):
            battle_edu_entry = Tk.Entry(battle_frame, textvariable = bb_list[foo - 1], width = 5)
            battle_edu_entry.grid(row = foo, column = 2)
        # 興味Pのエントリー
        bc_list = (bc1, bc2, bc3, bc4, bc5, bc6, bc7, bc8, bc9, bc10, bc11, bc12)
        for foo in range(1, 13):
            battle_int_entry = Tk.Entry(battle_frame, textvariable = bc_list[foo - 1], width = 5)
            battle_int_entry.grid(row = foo, column = 3)
        # 合計のラベル
        bd_list = (bd1, bd2, bd3, bd4, bd5, bd6, bd7, bd8, bd9, bd10, bd11, bd12)
        for foo in range(1, 13):
            battle_total_label = Tk.Label(battle_frame, textvariable = bd_list[foo - 1])
            battle_total_label.grid(row = foo, column = 4)

        # 交渉系技能のフレーム
        negotiation_frame = Tk.LabelFrame(frame_for_negotiation_knowledge, text = '交渉系技能', relief = 'groove', borderwidth = 2)
        negotiation_frame.grid(row = 0, column = 0, sticky = Tk.E + Tk.W + Tk.N)
        # 交渉系技能の変数
        # 初期値
        na1, na2, na3, na4, na5, na6, na7 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 職業ポイント
        nb1, nb2, nb3, nb4, nb5, nb6, nb7 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 興味ポイント
        nc1, nc2, nc3, nc4, nc5, nc6, nc7 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 合計
        nd1, nd2, nd3, nd4, nd5, nd6, nd7 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 交渉系技能の種類
        negotiation_name_list = ('言いくるめ', '信用', '説得', '値切り', '心理学')
        for foo in range(5):
            negotiation_5labels = Tk.Label(negotiation_frame, text = ability_label_list[foo])
            negotiation_5labels.grid(row = 0, column = foo)
        # 交渉系技能の種類のラベル
        for foo in range(1, 6):
            negotiation_name_label = Tk.Label(negotiation_frame, text = negotiation_name_list[foo - 1])
            negotiation_name_label.grid(row = foo, column = 0)
        # プラス、一番下の母国語・外国語
        bokokugo, gaikokugo = Tk.StringVar(), Tk.StringVar()
        gogaku = (bokokugo, gaikokugo)
        bokokugo.set('--母国語--')
        gaikokugo.set('--外国語--')
        for foo in range(2):
            negotiation_name_label2 = Tk.Entry(negotiation_frame, textvariable = gogaku[foo], width = 10)
            negotiation_name_label2.grid(row = foo + 6, column = 0)
        # 初期値のラベル
        na_list = (na1, na2, na3, na4, na5, na6, na7)
        na_list2 = (5, 15, 15, 5, 5, 0, 0)
        for foo in range(7):
            na_list[foo].set(na_list2[foo])
        for foo in range(1, 8):
            negotiation_ini_label = Tk.Label(negotiation_frame, textvariable = na_list[foo - 1])
            negotiation_ini_label.grid(row = foo, column = 1)
        # 職Pのエントリー
        nb_list = (nb1, nb2, nb3, nb4, nb5, nb6, nb7)
        for foo in range(1, 8):
            negotiation_edu_entry = Tk.Entry(negotiation_frame, textvariable = nb_list[foo - 1], width = 5)
            negotiation_edu_entry.grid(row = foo, column = 2)
        # 興味Pのエントリー
        nc_list = (nc1, nc2, nc3, nc4, nc5, nc6, nc7)
        for foo in range(1, 8):
            negotiation_int_entry = Tk.Entry(negotiation_frame, textvariable = nc_list[foo - 1], width = 5)
            negotiation_int_entry.grid(row = foo, column = 3)
        # 合計のラベル
        nd_list = (nd1, nd2, nd3, nd4, nd5, nd6, nd7)
        for foo in range(1, 8):
            negotiation_total_label = Tk.Label(negotiation_frame, textvariable = nd_list[foo - 1])
            negotiation_total_label.grid(row = foo, column = 4)

        # 知識系技能のフレーム
        knowledge_frame = Tk.LabelFrame(frame_for_negotiation_knowledge, text = '知識系技能', relief = 'groove', borderwidth = 2)
        knowledge_frame.grid(row = 1, column = 0, sticky = Tk.E + Tk.W)
        # 知識系技能の変数
        # 初期値
        ka1, ka2, ka3, ka4, ka5, ka6, ka7, ka8, ka9, ka10, ka11, ka12, ka13, ka14, ka15, ka16, ka17, ka18 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 職業ポイント
        kb1, kb2, kb3, kb4, kb5, kb6, kb7, kb8, kb9, kb10, kb11, kb12, kb13, kb14, kb15, kb16, kb17, kb18 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 興味ポイント
        kc1, kc2, kc3, kc4, kc5, kc6, kc7, kc8, kc9, kc10, kc11, kc12, kc13, kc14, kc15, kc16, kc17, kc18 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 合計
        kd1, kd2, kd3, kd4, kd5, kd6, kd7, kd8, kd9, kd10, kd11, kd12, kd13, kd14, kd15, kd16, kd17, kd18 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 知識系技能の種類
        knowledge_name_list = ('医学', 'オカルト', '科学', 'クトゥルフ神話', '経理', '考古学', 'コンピュータ', '人類学', '生物学', '地質学', '電子工学', '天文学', '博物学', '物理学', '法律', '薬学', '歴史')
        for foo in range(5):
            knowledge_5labels = Tk.Label(knowledge_frame, text = ability_label_list[foo])
            knowledge_5labels.grid(row = 0, column = foo)
        # 知識系技能の種類のラベル
        for foo in range(1, 18):
            knowledge_name_label = Tk.Label(knowledge_frame, text = knowledge_name_list[foo - 1])
            knowledge_name_label.grid(row = foo, column = 0)
        # プラス、一番下の芸術
        geijutsu = Tk.StringVar()
        geijutsu.set('--芸術--')
        knowledge_name_label2 = Tk.Entry(knowledge_frame, textvariable = geijutsu, width = 10)
        knowledge_name_label2.grid(row = 18, column = 0)
        # 初期値のラベル
        ka_list = (ka1, ka2, ka3, ka4, ka5, ka6, ka7, ka8, ka9, ka10, ka11, ka12, ka13, ka14, ka15, ka16, ka17, ka18)
        ka_list2 = (5, 5, 1, 0, 10, 1, 1, 1, 1, 1, 1, 1, 10, 1, 5, 1, 20, 5)
        for foo in range(18):
            ka_list[foo].set(ka_list2[foo])
        for foo in range(1, 19):
            knowledge_ini_label = Tk.Label(knowledge_frame, textvariable = ka_list[foo - 1])
            knowledge_ini_label.grid(row = foo, column = 1)
        # 職Pのエントリー
        kb_list = (kb1, kb2, kb3, kb4, kb5, kb6, kb7, kb8, kb9, kb10, kb11, kb12, kb13, kb14, kb15, kb16, kb17, kb18)
        for foo in range(1, 19):
            knowledge_edu_entry = Tk.Entry(knowledge_frame, textvariable = kb_list[foo - 1], width = 5)
            knowledge_edu_entry.grid(row = foo, column = 2)
        # 興味Pのエントリー
        kc_list = (kc1, kc2, kc3, kc4, kc5, kc6, kc7, kc8, kc9, kc10, kc11, kc12, kc13, kc14, kc15, kc16, kc17, kc18)
        for foo in range(1, 19):
            knowledge_int_entry = Tk.Entry(knowledge_frame, textvariable = kc_list[foo - 1], width = 5)
            knowledge_int_entry.grid(row = foo, column = 3)
        # 合計のラベル
        kd_list = (kd1, kd2, kd3, kd4, kd5, kd6, kd7, kd8, kd9, kd10, kd11, kd12, kd13, kd14, kd15, kd16, kd17, kd18)
        for foo in range(1, 19):
            knowledge_total_label = Tk.Label(knowledge_frame, textvariable = kd_list[foo - 1])
            knowledge_total_label.grid(row = foo, column = 4)

        # 行動系技能のフレーム
        action_frame = Tk.LabelFrame(frame_for_action_option, text = '行動系技能', relief = 'groove', borderwidth = 2)
        action_frame.grid(row = 0, column = 0, sticky = Tk.E + Tk.W + Tk.N)
        # 行動系技能の変数
        # 初期値
        aa1, aa2, aa3, aa4, aa5, aa6, aa7, aa8, aa9, aa10, aa11 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 職業ポイント
        ab1, ab2, ab3, ab4, ab5, ab6, ab7, ab8, ab9, ab10, ab11 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 興味ポイント
        ac1, ac2, ac3, ac4, ac5, ac6, ac7, ac8, ac9, ac10, ac11 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 合計
        ad1, ad2, ad3, ad4, ad5, ad6, ad7, ad8, ad9, ad10, ad11 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 行動系技能の種類
        action_name_list = ('運転', '機械修理', '重機械操作', '乗馬', '水泳', '跳躍', '電気修理', 'ナビゲート', '変装')
        for foo in range(5):
            action_5labels = Tk.Label(action_frame, text = ability_label_list[foo])
            action_5labels.grid(row = 0, column = foo)
        # 行動系技能の種類のラベル
        for foo in range(1, 10):
            action_name_label = Tk.Label(action_frame, text = action_name_list[foo - 1])
            action_name_label.grid(row = foo, column = 0)
        # プラス、一番下の制作・操縦
        seisaku, soujuu = Tk.StringVar(), Tk.StringVar()
        koudou = (seisaku, soujuu)
        seisaku.set('--制作--')
        soujuu.set('--操縦--')
        for foo in range(2):
            action_name_label2 = Tk.Entry(action_frame, textvariable = koudou[foo], width = 10)
            action_name_label2.grid(row = foo + 10, column = 0)
        # 初期値のラベル
        aa_list = (aa1, aa2, aa3, aa4, aa5, aa6, aa7, aa8, aa9, aa10, aa11)
        aa_list2 = (20, 20, 1, 5, 25, 25, 10, 10, 1, 5, 1)
        for foo in range(11):
            aa_list[foo].set(aa_list2[foo])
        for foo in range(1, 12):
            action_ini_label = Tk.Label(action_frame, textvariable = aa_list[foo - 1])
            action_ini_label.grid(row = foo, column = 1)
        # 職Pのエントリー
        ab_list = (ab1, ab2, ab3, ab4, ab5, ab6, ab7, ab8, ab9, ab10, ab11)
        for foo in range(1, 12):
            action_edu_entry = Tk.Entry(action_frame, textvariable = ab_list[foo - 1], width = 5)
            action_edu_entry.grid(row = foo, column = 2)
        # 興味Pのエントリー
        ac_list = (ac1, ac2, ac3, ac4, ac5, ac6, ac7, ac8, ac9, ac10, ac11)
        for foo in range(1, 12):
            action_int_entry = Tk.Entry(action_frame, textvariable = ac_list[foo - 1], width = 5)
            action_int_entry.grid(row = foo, column = 3)
        # 合計のラベル
        ad_list = (ad1, ad2, ad3, ad4, ad5, ad6, ad7, ad8, ad9, ad10, ad11)
        for foo in range(1, 12):
            action_total_label = Tk.Label(action_frame, textvariable = ad_list[foo - 1])
            action_total_label.grid(row = foo, column = 4)

        # 任意系技能のフレーム
        option_frame = Tk.LabelFrame(frame_for_action_option, text = '任意の技能', relief = 'groove', borderwidth = 2)
        option_frame.grid(row = 1, column = 0, sticky = Tk.E + Tk.W)
        # 任意の変数
        # 初期値
        oa1, oa2, oa3 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 職業ポイント
        ob1, ob2, ob3 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 興味ポイント
        oc1, oc2, oc3 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 合計
        od1, od2, od3 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar()
        # 任意の技能の種類
        for foo in range(5):
            option_5labels = Tk.Label(option_frame, text = ability_label_list[foo])
            option_5labels.grid(row = 0, column = foo)
        # 任意系技能の種類のエントリー
        option_namae1, option_namae2, option_namae3 = Tk.StringVar(), Tk.StringVar(), Tk.StringVar()
        option_name_list = (option_namae1, option_namae2, option_namae3)
        option_namae1.set('--お好きに--')
        for foo in range(1, 4):
            option_name_entry = Tk.Entry(option_frame, textvariable = option_name_list[foo - 1], width = 10)
            option_name_entry.grid(row = foo, column = 0)
        # 初期値のラベル
        oa_list = (oa1, oa2, oa3)
        for foo in range(1, 4):
            option_ini_label = Tk.Label(option_frame, textvariable = oa_list[foo - 1])
            option_ini_label.grid(row = foo, column = 1)
        # 職Pのエントリー
        ob_list = (ob1, ob2, ob3)
        for foo in range(1, 4):
            option_edu_entry = Tk.Entry(option_frame, textvariable = ob_list[foo - 1], width = 5)
            option_edu_entry.grid(row = foo, column = 2)
        # 興味Pのエントリー
        oc_list = (oc1, oc2, oc3)
        for foo in range(1, 4):
            option_int_entry = Tk.Entry(option_frame, textvariable = oc_list[foo - 1], width = 5)
            option_int_entry.grid(row = foo, column = 3)
        # 合計のラベル
        od_list = (od1, od2, od3)
        for foo in range(1, 4):
            option_total_label = Tk.Label(option_frame, textvariable = od_list[foo - 1])
            option_total_label.grid(row = foo, column = 4)

        # 常時 .get() .set() を繰り返す方法を考えるのに疲れたので気晴らしにダイスロールエリアを作る
        dice_roll_frame = Tk.LabelFrame(frame_for_action_option, text = u'(オマケ)簡易ダイスロール', relief = 'ridge', borderwidth = 2)
        dice_roll_frame.grid(row = 2, column = 0, pady = 50)
        dice_roll1, dice_roll2, dice_roll3, dice_roll4 = Tk.IntVar(), Tk.IntVar(), Tk.IntVar(), Tk.StringVar()
        dice_roll_entry1 = Tk.Entry(dice_roll_frame, textvariable = dice_roll1, width = 5)
        dice_roll_entry1.grid(row = 0, column = 0, pady = 5)
        dice_roll_label1 = Tk.Label(dice_roll_frame, text = 'D')
        dice_roll_label1.grid(row = 0, column = 1, pady = 5)
        dice_roll_entry2 = Tk.Entry(dice_roll_frame, textvariable = dice_roll2, width = 5)
        dice_roll_entry2.grid(row = 0, column = 2, pady = 5)
        dice_roll_label2 = Tk.Label(dice_roll_frame, text = '+')
        dice_roll_label2.grid(row = 0, column = 3, pady = 5)
        dice_roll_entry3 = Tk.Entry(dice_roll_frame, textvariable = dice_roll3, width = 5)
        dice_roll_entry3.grid(row = 0, column = 4, pady = 5)
        dice_roll_entry4 = Tk.Entry(dice_roll_frame, textvariable = dice_roll4)
        dice_roll4.set(u'result: ')
        dice_roll_entry4.grid(row = 1, column = 0, columnspan = 5)
        # バインディング
        def dice_roll_for_kanni(event):
            a, b, e = dice_roll1.get(), dice_roll2.get(), dice_roll3.get()
            c = dice_roll(a, b, e)
            dice_roll4.set(u'result: %d' % c)
        dice_roll_entry1.bind('<Return>', dice_roll_for_kanni)
        dice_roll_entry2.bind('<Return>', dice_roll_for_kanni)
        dice_roll_entry3.bind('<Return>', dice_roll_for_kanni)
        dice_roll_label3 = Tk.Label(dice_roll_frame, text = u' 数値を打ち込んだらエンターキーを押してね。')
        dice_roll_label3.grid(row = 2, column = 0, columnspan = 6)

        def reload():
            x = (con.get() + siz.get()) // 2
            if (con.get() + siz.get()) % 2:
                x += 1
            hp.set(x)
            mp.set(pow.get())
            san.set(pow.get() * 5)
            idea.set(int.get() * 5)
            luck.set(pow.get() * 5)
            knowledge.set(edu.get() * 5)
            edu_point.set(edu.get() * 20)
            int_point.set(int.get() * 10)
            db.set(damage_bonus(strs.get(), siz.get()))
            # 職業ポイントの合計
            edu_point_list = (sb1.get(), sb2.get(), sb3.get(), sb4.get(), sb5.get(), sb6.get(), sb7.get(), sb8.get(), sb9.get(), sb10.get(), sb11.get(), sb12.get(), bb1.get(), bb2.get(), bb3.get(), bb4.get(), bb5.get(), bb6.get(), bb7.get(), bb8.get(), bb9.get(), bb10.get(), bb11.get(), bb12.get(), nb1.get(), nb2.get(), nb3.get(), nb4.get(), nb5.get(), nb6.get(), nb7.get(), kb1.get(), kb2.get(), kb3.get(), kb4.get(), kb5.get(), kb6.get(), kb7.get(), kb8.get(), kb9.get(), kb10.get(), kb11.get(), kb12.get(), kb13.get(), kb14.get(), kb15.get(), kb16.get(), kb17.get(), kb18.get(), ab1.get(), ab2.get(), ab3.get(), ab4.get(), ab5.get(), ab6.get(), ab7.get(), ab8.get(), ab9.get(), ab10.get(), ab11.get(), ob1.get(), ob2.get(), ob3.get())
            edu_point_total.set(sum(edu_point_list))
            # 興味ポイントの合計
            int_point_list = (sc1.get(), sc2.get(), sc3.get(), sc4.get(), sc5.get(), sc6.get(), sc7.get(), sc8.get(), sc9.get(), sc10.get(), sc11.get(), sc12.get(), bc1.get(), bc2.get(), bc3.get(), bc4.get(), bc5.get(), bc6.get(), bc7.get(), bc8.get(), bc9.get(), bc10.get(), bc11.get(), bc12.get(), nc1.get(), nc2.get(), nc3.get(), nc4.get(), nc5.get(), nc6.get(), nc7.get(), kc1.get(), kc2.get(), kc3.get(), kc4.get(), kc5.get(), kc6.get(), kc7.get(), kc8.get(), kc9.get(), kc10.get(), kc11.get(), kc12.get(), kc13.get(), kc14.get(), kc15.get(), kc16.get(), kc17.get(), kc18.get(), ac1.get(), ac2.get(), ac3.get(), ac4.get(), ac5.get(), ac6.get(), ac7.get(), ac8.get(), ac9.get(), ac10.get(), ac11.get(), oc1.get(), oc2.get(), oc3.get())
            int_point_total.set(sum(int_point_list))
            # 回避, 母国語, 
            ba1.set(dex.get() * 2)
            na6.set(edu.get() * 5)
            # 技能の合計値
            for foo in range(12):
                sd_list[foo].set(sa_list[foo].get() + sb_list[foo].get() + sc_list[foo].get())
            for foo in range(12):
                bd_list[foo].set(ba_list[foo].get() + bb_list[foo].get() + bc_list[foo].get())
            for foo in range(7):
                nd_list[foo].set(na_list[foo].get() + nb_list[foo].get() + nc_list[foo].get())
            for foo in range(18):
                kd_list[foo].set(ka_list[foo].get() + kb_list[foo].get() + kc_list[foo].get())
            for foo in range(11):
                ad_list[foo].set(aa_list[foo].get() + ab_list[foo].get() + ac_list[foo].get())
            for foo in range(3):
                od_list[foo].set(oa_list[foo].get() + ob_list[foo].get() + oc_list[foo].get())

        def entry_check():
            try:
                reload()
            except ValueError:
                print('type:' + str(type(e)))
            self.after(500, entry_check)
        entry_check()


if __name__ == '__main__':
    gccs = GCCS()
    gccs.pack()
    gccs.mainloop()
