# apic_fabric_show_int_status

Cisco ACIのAPICにSSH接続して`fabric xx show interface status`コマンドを実行し、その結果をパースしてHTMLファイルにします。

このロールでは独自のフィルタープラグイン`split_by_node`を使ってリストを加工します。

<BR>

# Requirements

制御ノード上にPythonのTextFSMモジュールが必要です。

<BR>

# Role Variables

`defaults/main.yml`に記載の変数を利用します。

下記の設定では実行した場所に`log`ディレクトリを作成し、そこに実行結果のログを作成します。


```yml
LOG_DIR: "{{ lookup('env', 'PWD') + '/log' }}"
```

<BR>

# Dependencies

他のロールへの依存はありません。

<BR>

# Example Playbook

プレイブックの例は`tests/test.yml`にあります。

```yml

- name: test
  hosts: apic1
  gather_facts: false
  strategy: linear
  serial: 0

  tasks:
    - import_role:
        name: apic_fabric_show_int_status
      vars:
        EXCLUDE_HOSTS: []
        LOG_DIR: "{{ lookup('env', 'PWD') }}/log"
        FABRICS:
          - 101
          - 102
          - 103
          - 104
        DEBUG: false
```

実行すると指定したログディレクトリにテキストファイルとHTMLファイルが生成されます。
HTMLファイルはこのようなイメージで表示します。緑のポートは`connected`、黒は`notconnect`、グレーはそれ以外を表します。

![fig_fabric_show_int_status](https://user-images.githubusercontent.com/21165341/124450535-7f598f80-ddbf-11eb-8adc-af7f81aea576.PNG)

<BR>

[出力例](https://takamitsu-iida.github.io/ansible-on-wsl/apic_fabric_show_int_status.html)

<BR>

# License

BSD

<BR><BR>

# Author Information

takamitsu-iida
