# aci_show_vpc_brief

Cisco ACIのスイッチにログインしてiShell上のコマンド `show vpc brief` を実行してログに保存し、過去に採取したログと共に分析してポートの状態を可視化します。

このロールでは独自モジュール`aci_show_vpc_brief`を使ってコマンド出力を加工します。
実際にはモジュールは何もせず、同名のアクションプラグインによってコマンド出力を加工します。
モジュールは不要ですが、モジュールの書き方のテンプレとして残しています。

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

プレイブックの例は`tests/test.yml`にあります。

```yml
- name: test
  hosts: leaf_switches
  gather_facts: false
  strategy: linear
  serial: 0

  tasks:
    - import_role:
        name: aci_show_vpc_brief
      vars:
        EXCLUDE_HOSTS: []
        LOG_DIR: "{{ lookup('env', 'PWD') }}/log"
```

プレイブックを実行するたびに`show vpc brief`の実行結果を記録したログファイルが残ります。
過去５世代までのログファイルをまとめて分析して、いつの時点でPortChannelの状態が変化したのかを可視化します。

![キャプチャ](https://user-images.githubusercontent.com/21165341/124754895-ae116a80-df65-11eb-95b8-0a4a65f215bb.PNG)

<BR>

[出力例](https://takamitsu-iida.github.io/ansible-on-wsl/aci_show_vpc_brief.html)

<BR>

# License

BSD

<BR>

# Author Information

takamitsu-iida
