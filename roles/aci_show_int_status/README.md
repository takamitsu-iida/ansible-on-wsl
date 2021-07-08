# aci_show_int_status

Cisco ACIのスイッチにSSH接続してiShell上のコマンドshow interface statusを実行します。

<br>

# Requirements

Cisco ACIのスイッチにSSH接続できる環境が必要です。

制御ノード上にPythonのTextFSMモジュールが必要です。

<br>

# Role Variables

`defaults/main.py`に記載の変数を利用します。

<br>

# Dependencies

他のロールへの依存はありません。

<br>

# Example Playbook

`show interface status`コマンドを実行した結果をログ・ファイルとして残します。

過去のログも含めて分析し、HTMLファイルで可視化します。

![キャプチャ](https://user-images.githubusercontent.com/21165341/124870226-5292bb80-dffd-11eb-8445-6ad8dc945389.PNG)

<br>

# License

BSD

# Author Information

takamitsu-iida