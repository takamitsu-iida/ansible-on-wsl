# aci_show_int_status

Cisco ACIのスイッチにSSH接続してiShell上のコマンドshow interface statusを実行します。

このロールでは独自のアクションプラグイン`aci_show_int_status`を利用してコマンド出力を加工します。

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

プレイブックの例は`tests/test.yml`にあります。

```yml
- name: test
  hosts: leaf_switches
  gather_facts: false
  strategy: linear
  serial: 0

  tasks:
    - import_role:
        name: aci_show_int_status
      vars:
        EXCLUDE_HOSTS: []
        LOG_DIR: "{{ lookup('env', 'PWD') }}/log"
```

`show interface status`コマンドを実行した結果をログ・ファイルとして残します。

過去のログも含めて分析し、HTMLファイルで可視化します。

![キャプチャ](https://user-images.githubusercontent.com/21165341/124870226-5292bb80-dffd-11eb-8445-6ad8dc945389.PNG)

<br>

[出力例](https://takamitsu-iida.github.io/ansible-on-wsl/aci_show_int_status.html)

<br>

# License

BSD

# Author Information

takamitsu-iida
