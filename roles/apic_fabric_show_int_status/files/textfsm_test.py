#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""textfsmで加工できるかテストするスクリプト

依存ライブラリ
  textfsm
  tabulate
"""

__author__ = "takamitsu-iida"
__version__ = "0.0"
__date__ = "2021/06/15"

#
# 標準ライブラリのインポート
#
import logging
import os
import sys


def here(path=''):
  """相対パスを絶対パスに変換して返却します"""
  return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

# アプリケーションのホームディレクトリ
app_dir = here(".")

# 自身の名前から拡張子を除いてプログラム名を得る
app_name = os.path.splitext(os.path.basename(__file__))[0]

# ロギングの設定
# レベルはこの順で下にいくほど詳細になる
#   logging.CRITICAL
#   logging.ERROR
#   logging.WARNING --- 初期値はこのレベル
#   logging.INFO
#   logging.DEBUG
#
# ログの出力方法
# logger.debug("debugレベルのログメッセージ")
# logger.info("infoレベルのログメッセージ")
# logger.warning("warningレベルのログメッセージ")

# default setting
logging.basicConfig()

# ロガーを取得
logger = logging.getLogger(__name__)

# ログレベル設定
logger.setLevel(logging.INFO)

# フォーマット
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 標準出力へのハンドラ
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
stdout_handler.setLevel(logging.INFO)
logger.addHandler(stdout_handler)

#
# 外部ライブラリのインポート
#
try:
  import textfsm
except ImportError as e:
  logger.exception("textfsmモジュールのインポートに失敗しました: %s", e)
  sys.exit(1)

try:
  from tabulate import tabulate
  HAS_TABULATE = True
except ImportError:
  HAS_TABULATE = False

#
# ここからスクリプト
#
if __name__ == '__main__':

  def main():
    """メイン関数

    Returns:
      int -- 正常終了は0、異常時はそれ以外を返却
    """

    LOGFILE1 = 'apic1_apic_fabric_show_int_status.1.txt'

    TEXTFSM = 'apic_fabric_show_interface_status.textfsm'

    input_path = os.path.join(app_dir, LOGFILE1)
    try:
      with open(input_path, 'r') as f:
        data = f.read()
    except FileNotFoundError:
      print("{0}が見つかりません".format(input_path))
      return 1
    except Exception as e:
      logger.exception(e.__class__.__name__)
      return 1

    textfsm_path = os.path.join(app_dir, TEXTFSM)
    try:
      with open(textfsm_path) as f:
        table = textfsm.TextFSM(f)
        header = table.header
        result = table.ParseText(data)
    except FileNotFoundError:
      print("{0}が見つかりません".format(textfsm_path))
      return 1
    except Exception as e:
      logger.exception(e.__class__.__name__)
      return 1

    if HAS_TABULATE:
      print(tabulate(result, headers=header))

    return 0

  # 実行
  sys.exit(main())