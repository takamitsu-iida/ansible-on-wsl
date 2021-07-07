# aci_show_vpc_brief

Cisco ACIのスイッチにログインしてiShell上のコマンド `show vpc brief` を実行し、ログに保存します。

過去に採取したログと共に分析してポートの状態を可視化します。

<BR>

# Requirements

特別な要件はありません。

<BR>

# Role Variables

`defaults/main.yml` に記載の変数を利用します。

<BR>

# Dependencies

依存する他のロールはありません。

<BR>

# Example Playbook

プレイブックを実行するたびに`show vpc brief`の実行結果を記録したログファイルが残ります。
過去５世代までのログファイルをまとめて分析して、いつの時点でPortChannelの状態が変化したのかを可視化します。

![キャプチャ](https://user-images.githubusercontent.com/21165341/124754895-ae116a80-df65-11eb-95b8-0a4a65f215bb.PNG)

<BR>

# License

BSD

<BR>

# Author Information

takamitsu-iida
