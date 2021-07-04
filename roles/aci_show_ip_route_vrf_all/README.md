aci_show_ip_route_vrf_all
=========================

Cisco ACIの各スイッチにSSH接続してiShell上のコマンド `show ip route vrf all` を実行してルーティングテーブルを採取します。

Requirements
------------

SSHでCisco ACIの各スイッチに接続できる環境が必要です。踏み台(bastionホスト)経由で構いません。

制御ノード上にPython3のtextfsmモジュールが必要です。

ACIの各スイッチはnetwork_osをnxosとして設定しますが、実際にはACI独自のiShellですので、terminal_pluginsで挙動を変更する必要があります。このロールに同梱しています。


Role Variables
--------------

defaults/main.ymlに記載の変数を利用します。

## ログディレクトリの指定

この設定ではプレイブックを実行したその場所に`log`ディレクトリを作成します

```yml
LOG_DIR: "{{ lookup('env', 'PWD') + '/log' }}"
```

Dependencies
------------

他のロールへの依存はありません。

Example Playbook
----------------

初回実行時と、二回目以降の実行で挙動が変わります。

## 初回実行時

ACIのスイッチにログインして`show ip route vrf all`を実行し、それを`LOG_DIR`（ここでは./log/）にファイルとして保存します。

4台のLeafスイッチをターゲットにした場合の例です。

```bash
iida@FCCLS0008993-00:~/git/ansible-on-wsl/roles/aci_show_ip_route_vrf_all/tests$ ./test.sh

PLAY [test] ***

TASK [../../aci_show_ip_route_vrf_all : Create log directory if not exists] ***
ok: [leaf4 -> localhost]
ok: [leaf1 -> localhost]
ok: [leaf3 -> localhost]
ok: [leaf2 -> localhost]

TASK [../../aci_show_ip_route_vrf_all : show ip route vrf all] ***
ok: [leaf2]
ok: [leaf4]
ok: [leaf3]
ok: [leaf1]

TASK [../../aci_show_ip_route_vrf_all : debug] ***
skipping: [leaf1]
skipping: [leaf2]
skipping: [leaf3]
skipping: [leaf4]

TASK [../../aci_show_ip_route_vrf_all : Save command output] ***
changed: [leaf1 -> localhost]
changed: [leaf3 -> localhost]
changed: [leaf4 -> localhost]
changed: [leaf2 -> localhost]

TASK [../../aci_show_ip_route_vrf_all : run log analizer script] ***
changed: [leaf1 -> localhost]
changed: [leaf2 -> localhost]
changed: [leaf3 -> localhost]
changed: [leaf4 -> localhost]

TASK [../../aci_show_ip_route_vrf_all : debug] ***
ok: [leaf1] => {}
ok: [leaf2] => {}
ok: [leaf3] => {}
ok: [leaf4] => {}

PLAY RECAP ***
leaf1                      : ok=5    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
leaf2                      : ok=5    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
leaf3                      : ok=5    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
leaf4                      : ok=5    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

iida@FCCLS0008993-00:~/git/ansible-on-wsl/roles/aci_show_ip_route_vrf_all/tests$
```

指定したログディレクトリ（./log/）に対象ノードごとにファイルができています。

```bash
iida@FCCLS0008993-00:~/git/ansible-on-wsl/roles/aci_show_ip_route_vrf_all/tests$ ls -l log
total 216
-rw-r--r-- 1 iida 19176 Jul  4 14:38 ansible.log
-rw-r--r-- 1 iida 48173 Jul  4 14:38 leaf1_aci_show_ip_route_vrf_all_20210704_143851.txt
-rw-r--r-- 1 iida 48169 Jul  4 14:38 leaf2_aci_show_ip_route_vrf_all_20210704_143851.txt
-rw-r--r-- 1 iida 48175 Jul  4 14:38 leaf3_aci_show_ip_route_vrf_all_20210704_143851.txt
-rw-r--r-- 1 iida 48171 Jul  4 14:38 leaf4_aci_show_ip_route_vrf_all_20210704_143851.txt
iida@FCCLS0008993-00:~/git/ansible-on-wsl/roles/aci_show_ip_route_vrf_all/tests$
```

## 二度目以降の実行

二度目以降の実行では、最新のログファイルと過去のログファイルで差分がないかを確認します。

```bash
iida@FCCLS0008993-00:~/git/ansible-on-wsl/roles/aci_show_ip_route_vrf_all/tests$ ./test.sh

PLAY [test] ***

TASK [../../aci_show_ip_route_vrf_all : Create log directory if not exists] ***
ok: [leaf4 -> localhost]
ok: [leaf1 -> localhost]
ok: [leaf2 -> localhost]
ok: [leaf3 -> localhost]

TASK [../../aci_show_ip_route_vrf_all : show ip route vrf all] ***
ok: [leaf3]
ok: [leaf1]
ok: [leaf4]
ok: [leaf2]

TASK [../../aci_show_ip_route_vrf_all : debug] ***
skipping: [leaf1]
skipping: [leaf2]
skipping: [leaf3]
skipping: [leaf4]

TASK [../../aci_show_ip_route_vrf_all : Save command output] ***
changed: [leaf1 -> localhost]
changed: [leaf3 -> localhost]
changed: [leaf2 -> localhost]
changed: [leaf4 -> localhost]

TASK [../../aci_show_ip_route_vrf_all : run log analizer script] ***
changed: [leaf2 -> localhost]
changed: [leaf1 -> localhost]
changed: [leaf4 -> localhost]
changed: [leaf3 -> localhost]

TASK [../../aci_show_ip_route_vrf_all : debug] ***
ok: [leaf1] => {}

MSG:

newest file: leaf1_aci_show_ip_route_vrf_all_20210704_150704.txt
diff: 0   +: 0   -: 0     leaf1_aci_show_ip_route_vrf_all_20210704_150226.txt
diff: 0   +: 0   -: 0     leaf1_aci_show_ip_route_vrf_all_20210704_143851.txt
ok: [leaf2] => {}

MSG:

newest file: leaf2_aci_show_ip_route_vrf_all_20210704_150704.txt
diff: 0   +: 0   -: 0     leaf2_aci_show_ip_route_vrf_all_20210704_150226.txt
diff: 0   +: 0   -: 0     leaf2_aci_show_ip_route_vrf_all_20210704_143851.txt
ok: [leaf3] => {}

MSG:

newest file: leaf3_aci_show_ip_route_vrf_all_20210704_150704.txt
diff: 0   +: 0   -: 0     leaf3_aci_show_ip_route_vrf_all_20210704_150226.txt
diff: 0   +: 0   -: 0     leaf3_aci_show_ip_route_vrf_all_20210704_143851.txt
ok: [leaf4] => {}

MSG:

newest file: leaf4_aci_show_ip_route_vrf_all_20210704_150704.txt
diff: 0   +: 0   -: 0     leaf4_aci_show_ip_route_vrf_all_20210704_150226.txt
diff: 0   +: 0   -: 0     leaf4_aci_show_ip_route_vrf_all_20210704_143851.txt

PLAY RECAP ***
leaf1                      : ok=5    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
leaf2                      : ok=5    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
leaf3                      : ok=5    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
leaf4                      : ok=5    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

iida@FCCLS0008993-00:~/git/ansible-on-wsl/roles/aci_show_ip_route_vrf_all/tests$
```

## 差分の内容を知りたい場合

差分が見つかった場合、pythonスクリプトを直接叩いて、何が変更になったのかを表示します。
pythonスクリプトは`files`ディレクトリにあります。

何も差分がない場合。

```bash
iida@FCCLS0008993-00:~/git/ansible-on-wsl/roles/aci_show_ip_route_vrf_all/tests$ ../files/aci_show_ip_route_vrf_all.py -d ./log -p leaf1 -v
newest file: leaf1_aci_show_ip_route_vrf_all_20210704_150704.txt
diff: 0   +: 0   -: 0     leaf1_aci_show_ip_route_vrf_all_20210704_150226.txt


diff: 0   +: 0   -: 0     leaf1_aci_show_ip_route_vrf_all_20210704_143851.txt


iida@FCCLS0008993-00:~/git/ansible-on-wsl/roles/aci_show_ip_route_vrf_all/tests$
```

ログファイルを編集して、意図的に差分を作った場合。

```bash
iida@FCCLS0008993-00:~/git/ansible-on-wsl/roles/aci_show_ip_route_vrf_all/tests$ ../files/aci_show_ip_route_vrf_all.py -d ./log -p leaf1 -v
newest file: leaf1_aci_show_ip_route_vrf_all_20210704_143851.txt
diff: 4   +: 2   -: 2     leaf1_aci_show_ip_route_vrf_all_20210704_150704.txt

['+', overlay-1                      10.0.0.1         /32   via 10.0.64.93       eth1/51.9    isis-isis_infra]
['+', overlay-1                      10.0.0.1         /32   via 10.0.40.81       eth1/49.7    isis-isis_infra]
['-', overlay-1                      10.0.0.1         /32   via 10.0.64.92       eth1/51.9    isis-isis_infra]
['-', overlay-1                      10.0.0.1         /32   via 10.0.40.80       eth1/49.7    isis-isis_infra]

diff: 4   +: 2   -: 2     leaf1_aci_show_ip_route_vrf_all_20210704_150226.txt

['+', overlay-1                      10.0.0.1         /32   via 10.0.64.93       eth1/51.9    isis-isis_infra]
['+', overlay-1                      10.0.0.1         /32   via 10.0.40.81       eth1/49.7    isis-isis_infra]
['-', overlay-1                      10.0.0.1         /32   via 10.0.64.92       eth1/51.9    isis-isis_infra]
['-', overlay-1                      10.0.0.1         /32   via 10.0.40.80       eth1/49.7    isis-isis_infra]

iida@FCCLS0008993-00:~/git/ansible-on-wsl/roles/aci_show_ip_route_vrf_all/tests$
```

（作られた日付が）最新のファイルに対して、その他のファイルとの差分を取り、経路情報が増えていれば'+'を、減っていれば'-'で表示します。



License
-------

BSD

Author Information
------------------

takamitsu-iida
