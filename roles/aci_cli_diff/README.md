# aci_cli_diff

cli_commandでネットワーク機器にコマンドを打ち込み、最新のログ・ファイルと過去のログ・ファイルでdiffをとります。

このロールでは独自のモジュールを利用します。
pythonの標準ライブラリdifflibを用いて文字列を比較してHTMLのテーブルを生成しています。

<br>

# Requirements

特別な要件はありません。

<br>

# Role Variables

`defaults/main.yml` に記載の変数を利用します。

<br>

# Dependencies

他のロールへの依存はありません。

<br>

# Example Playbook

NOTE: 少なくとも2回、実行しないとdiffがとれません。


```yml
  tasks:
    - import_role:
        name: aci_cli_diff
      vars:
        EXCLUDE_HOSTS: []
        LOG_DIR: "{{ lookup('env', 'PWD') }}/log"
        COMMANDS:
          - show inventory
          - show lldp neighbors
          - show hardware
          - show module
          - show cores
```

差分があれば色付きで表示されます。

![キャプチャ](https://user-images.githubusercontent.com/21165341/125151610-556ae900-e182-11eb-9c0b-2041f1ed4f2a.PNG)


<br>

# License

BSD

<br>

# Author Information

takamitsu-iida
