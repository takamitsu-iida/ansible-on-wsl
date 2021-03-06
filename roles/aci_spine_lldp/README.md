# aci_spine_lldp

Cisco ACIのSpineスイッチにSSH接続してiShell上のコマンド`show lldp neighbors`の実行結果を採取します。

このロールでは独自のアクションプラグインを使って実行結果を分析します。

`aci_spine_lldp`はコマンド出力の加工とjsonファイルの保存までを実行します。

`aci_spine_lldp_diff`は`files/diff_source.json`との差分を確認し、CSSのクラスを付与する処理を行います。
追加や削除があれば色で分かるようになっています。

<br>

# Requirements

特にありません。

<br>

# Role Variables

`defaults/main.yml`に記載の変数を利用します。

`DIFF_SOURCE_JSON_FILE`はロールの`files`ディレクトリからの相対パスです。

<br>

# Dependencies

他のロールへの依存はありません。

<br>

# Example Playbook

`tests/test.yml`が例です。

```yml
- name: gather lldp info
  hosts: spine_switches
  gather_facts: false
  strategy: linear
  serial: 0

  tasks:
    - import_role:
        name: aci_spine_lldp
      vars:
        LOG_DIR: "{{ lookup('env', 'PWD') }}/log"
        DIFF_SOURCE_JSON_FILE: aci_spine_lldp_20210718_174749.json
```

<br>

[出力例](https://takamitsu-iida.github.io/ansible-on-wsl/aci_spine_lldp.html)

<br>

# License

BSD

<br>

# Author Information

takamitsu-iida
