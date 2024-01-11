import sys
# passの設定 (pip showで出てきた、LocationのPASSを以下に設定)
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.meld import Meld
from mahjong.constants import EAST, SOUTH, WEST, NORTH

calculator = HandCalculator()

def print_hand_result(hand_result):
    print(f"翻数: {hand_result.han}, 符数: {hand_result.fu}")
    if hand_result.han >= 1:
        print(f"点数(ツモアガリの場合): 親 {hand_result.cost['main'][0]} 点, 子 {hand_result.cost['additional'][0]} 点")
    else:
        print(f"点数(ツモアガリの場合): {hand_result.cost['main'][0]} 点")
    print(f"役: {hand_result.yaku}")
    print("符数の詳細:")
    for fu_item in hand_result.fu_details:
        print(fu_item)
    print('')

man_input = input("萬子を入力してください (例: 123): ")
pin_input = input("筒子を入力してください (例: 123): ")
sou_input = input("索子を入力してください (例: 123): ")
honors_input = input("字牌を入力してください (例: 11122): ")

tiles = TilesConverter.string_to_136_array(man=man_input, pin=pin_input, sou=sou_input, honors=honors_input)

win_tile_input = input("アガリ牌を入力してください (例: pin 1): ")
if win_tile_input:
    suit, number = win_tile_input.strip().split()
    win_tile = None
    if suit == 'man':
        win_tile = TilesConverter.string_to_136_array(man=number)[0]
    elif suit == 'pin':
        win_tile = TilesConverter.string_to_136_array(pin=number)[0]
    elif suit == 'sou':
        win_tile = TilesConverter.string_to_136_array(sou=number)[0]
    elif suit == 'honors':
        win_tile = TilesConverter.string_to_136_array(honors=number)[0]
    else:
        print("無効なアガリ牌のスートです。man, pin, sou, honors のいずれかを指定してください。")
else:
    win_tile = None

melds_input = input("鳴きを入力してください (例: man111sou222; コンマで区切ってください): ").split(',')
melds = []
for meld_str in melds_input:
    if meld_str.strip():  # 空でない場合のみ処理
        suit = meld_str[:3]  # 牌のスート
        numbers = meld_str[3:]  # 牌の数字

        # suitに応じて牌を指定
        tiles = []
        for number in numbers:
            if suit == 'man':
                tiles.append(TilesConverter.string_to_136_array(man=number)[0])
            elif suit == 'pin':
                tiles.append(TilesConverter.string_to_136_array(pin=number)[0])
            elif suit == 'sou':
                tiles.append(TilesConverter.string_to_136_array(sou=number)[0])
            elif suit == 'honors':
                tiles.append(TilesConverter.string_to_136_array(honors=number)[0])
            else:
                print("無効な牌のスートです。man, pin, sou, honors のいずれかを指定してください。")

        if tiles:
            melds.append(Meld(Meld.KAN if len(tiles) == 4 else Meld.PON, tiles, False))

dora_input = input("ドラ表示牌を入力してください (例: man1 sou2 pin3; スペースで区切ってください): ").split()
dora_indicators = []
for dora_str in dora_input:
    suit = dora_str[:-1]  # 牌のスート
    number = int(dora_str[-1])  # 牌の数字
    tile = None

    # suitに応じて牌を指定
    if suit == 'man':
        tile = TilesConverter.string_to_136_array(man=str(number))[0]
    elif suit == 'pin':
        tile = TilesConverter.string_to_136_array(pin=str(number))[0]
    elif suit == 'sou':
        tile = TilesConverter.string_to_136_array(sou=str(number))[0]
    elif suit == 'honors':
        tile = TilesConverter.string_to_136_array(honors=str(number))[0]
    else:
        print("無効なドラ表示牌のスートです。man, pin, sou, honors のいずれかを指定してください。")

    if tile is not None:
        dora_indicators.append(tile)

is_riichi = input("リーチしている場合は 'yes' を入力してください。それ以外は 'no': ").strip().lower() == 'yes'
player_wind_input = input("自風を入力してください (例: EAST, SOUTH, WEST, NORTH): ").strip().upper()
round_wind_input = input("場風を入力してください (例: EAST, SOUTH, WEST, NORTH): ").strip().upper()

player_wind = None
round_wind = None

# 自風、場風を指定
if player_wind_input in ['EAST', 'SOUTH', 'WEST', 'NORTH']:
    player_wind = eval(player_wind_input)
else:
    print("無効な自風です。EAST, SOUTH, WEST, NORTH のいずれかを指定してください。")

if round_wind_input in ['EAST', 'SOUTH', 'WEST', 'NORTH']:
    round_wind = eval(round_wind_input)
else:
    print("無効な場風です。EAST, SOUTH, WEST, NORTH のいずれかを指定してください。")

config = HandConfig(is_riichi=is_riichi)
config.player_wind = player_wind
config.round_wind = round_wind
config.has_open_tanyao = True  # なるべく副露せずに手牌だけで和了る場合

result = calculator.estimate_hand_value(tiles, win_tile, dora_indicators, config)
print_hand_result(result)
