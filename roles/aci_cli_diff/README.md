# aci_cli_diff

cli_commandでネットワーク機器にコマンドを打ち込み、最新のログ・ファイルと過去のログ・ファイルでdiffをとります。

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

```yml
  tasks:
    - import_role:
        name: diff
      vars:
        EXCLUDE_HOSTS: []
        LOG_DIR: "{{ lookup('env', 'PWD') + '/log' }}"
        COMMANDS:
          - show inventory
          - show lldp neighbors
          - show hardware
          - show module
          - show cores
```

<br>

# License

BSD

<br>

# Author Information

takamitsu-iida
