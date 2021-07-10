# aci_iping

Cisco ACIのスイッチにSSHで接続し、ipingコマンドを実行します。

このロールでは独自のフィルタープラグインを利用します。

<br>

# Requirements

制御ノード上にPythonのtextfsmモジュールが必要です。

<br>

# Role Variables

`defaults/main.yml`に記載の変数を利用します。

下記の設定では、カレントディレクトリ直下のlogディレクトリにログを格納します。各ノード単位にipingの実行結果をファイルに追記していきます。

```
# ログファイルのディレクトリ
LOG_DIR: "{{ lookup('env', 'PWD') }}/log"
```

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
        name: aci_iping
      vars:
        EXCLUDE_HOSTS: []
        LOG_DIR: "{{ lookup('env', 'PWD') }}/log"
        TARGETS:
          - nw-00-03-06-00
          - nw-00-03-14-00
          - nw-00-03-22-00
```

実行後に`aci_iping_summary.html`というHTMLファイルが生成されます。
ipingの実行結果を一覧表示したものです。上から下に実行したノード、右から左にipingを打った先、を表します。ロス率によって背景色が変わります。

![キャプチャ](https://user-images.githubusercontent.com/21165341/125151152-0ae86d00-e180-11eb-8c19-77562c1780f5.PNG)

<br>

# License

BSD

<br>

# Author Information

takamitsu-iida