import os
import time
import colorsys
import shutil
import glob

minimum_ssr = 5

def click(x, y, times=1, sleep=1.2):
    for _ in range(times):
        os.system(f'cliclick c:{x},{y}')
        time.sleep(sleep)

def color(x, y):
    r, g, b = map(int, os.popen(f'cliclick cp:{x},{y}').read().split())
    return (r, g, b)

def enter(keystroke):
    os.system(f'osascript -e \'tell application "System Events" to keystroke "{keystroke}"\'')
    time.sleep(1)

def activate():
    os.system(f'osascript -e \'tell application "ウマ娘" to activate\'')

def screenshot(path, index):
    if index == 0:
        os.system(f'screencapture -R 115,134,96,125 {path}')
    elif index == 1:
        os.system(f'screencapture -R 247,134,96,125 {path}')
    elif index == 2:
        os.system(f'screencapture -R 380,134,96,125 {path}')
    elif index == 3:
        os.system(f'screencapture -R 181,281,96,125 {path}')
    elif index == 4:
        os.system(f'screencapture -R 315,281,96,125 {path}')
    elif index == 5:
        os.system(f'screencapture -R 115,431,96,125 {path}')
    elif index == 6:
        os.system(f'screencapture -R 248,431,96,125 {path}')
    elif index == 7:
        os.system(f'screencapture -R 380,431,96,125 {path}')
    elif index == 8:
        os.system(f'screencapture -R 182,580,96,125 {path}')
    elif index == 9:
        os.system(f'screencapture -R 314,580,96,125 {path}')
    elif index == -1:
        os.system(f'screencapture -R 248,340,96,125 {path}')
    else:
        os.system(f'screencapture -l`getwindowid ウマ娘 ウマ娘` {path}')

def rgb2hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return (h, s, v)

def ssr(path, ssr_count):
    count = 0
    pos_list = [(163, 257), (295, 257), (427, 257)]
    pos_list += [(225, 404), (361, 404)]
    pos_list += [(163, 554), (295, 554), (427, 554)]
    pos_list += [(225, 703), (361, 703)]
    for index, pos in enumerate(pos_list):
        h, s, v = rgb2hsv(*color(pos[0], pos[1]))
        if h < 0.6 and h > 0.3:
            count += 1
            screenshot(f'{path}_SSR{ssr_count + count}.png', index)
    return count

def get_start():
    return max([int(path.split('/')[1].split('_')[0]) for path in glob.glob(f'umamusume/*')]) + 1

activate()
for i in range(get_start(), 10000):
    print(f'Reset Marathon {i:04}')
    if os.path.exists(f'umamusume/{i:04}'):
        shutil.rmtree(f'umamusume/{i:04}')
    os.makedirs(f'umamusume/{i:04}')
    while color(550, 803) != (178, 118, 71):
        click(556, 810) # タイトル画面のメニュー
    click(556, 810)
    click(279, 693) # ユーザーデータ削除
    click(391, 564, times=2) # ユーザーデータ削除
    click(294, 564) # 閉じる

    click(300, 746, times=3) # Tap to start
    click(395, 780) # 同意する
    click(395, 780, sleep=1.5) # 同意する
    click(199, 566, times=2) # キャンセル
    click(388, 562) # 後でする
    click(305, 409) # トレーナー名クリック
    enter('a')
    click(300, 567) # 登録する
    click(391, 566) # OK

    while color(314, 779) != (113, 67, 32):
        click(556, 810) # ログボスキップ

    click(300, 780, sleep=1.5) # お知らせ閉じる
    click(300, 566, sleep=1.5) # メインストーリー解放閉じる
    click(300, 780, sleep=1.5) # ウマ娘ストーリー解放閉じる

    click(475, 615) # プレゼントボックス
    click(396, 780) # 一括受け取り
    click(300, 780) # 閉じる
    click(200, 780) # 閉じる

    click(470, 804, sleep=2) # ガチャ
    click(485, 530) # サポートカードガチャ
    click(430, 685) # 10回引く

    ssr_count = 0
    for j in range(8):
        click(394, 566) # ガチャを引く
        while color(380, 723) != (171, 144, 121):
            click(556, 810)
        
        current_ssr = ssr(f'umamusume/{i:04}/gacha', ssr_count)
        ssr_count += current_ssr
        print(f'  [Gacha {j+1}] SSR: {current_ssr}')
        if j < 7:
            click(399, 789) # もう一回引く

    click(200, 789, sleep=4.5) # 戻る

    if ssr_count >= minimum_ssr:
        click(50, 535, times=2) # メイクデビューチケット
        click(294, 687) # 1回引く
        click(395, 554) # ガチャを引く
        for j in range(3):
            while color(242, 266) != (154, 212, 82):
                click(556, 810)
            screenshot(f'umamusume/{i:04}/gacha_{ssr_count + j + 1}.png', -1) # スクショ
            print(f'  Gacha SSR{j+1}: screenshot saved')
            if j < 2:
                click(391, 612) # もう一回引く
                click(397, 562) # ガチャを引く
        click(300, 612, sleep=4.5) # OK

    click(300, 800) # ホーム

    os.rename(f'umamusume/{i:04}', f'umamusume/{i:04}_SSR{ssr_count}')
    if ssr_count >= minimum_ssr:
        click(511, 95) # メニュー
        click(411, 577) # データ連携
        click(400, 566) # データ連携
        click(444, 504) # 設定
        click(394, 564) # 設定
        click(300, 386) # パスワード入力開始
        enter('Uma6sume')
        click(300, 468) # 確認パスワード入力開始
        enter('Uma6sume')
        click(186, 560) # チェック
        click(400, 615) # OK
        screenshot(f'umamusume/{i:04}_SSR{ssr_count}/integration.png', -2) # スクショ
        print(f'  Integration: screenshot saved')
        click(300, 560) # 閉じる
    else:
        shutil.rmtree(f'umamusume/{i:04}_SSR{ssr_count}')

    click(511, 95) # メニュー
    click(400, 698) # タイトルへ