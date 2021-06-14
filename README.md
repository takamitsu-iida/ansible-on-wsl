# ansible-in-wsl


# ツール群

## WSL Ubuntu 20.04

- 最新化しておく
  - sudo apt update
  - sudo apt upgrade
  - sudo apt dist-upgrade
  - sudo apt autoremove

- Python3が必要
  - sudo apt install python3 python3-pip -y
  - sudo pip3 install pip -U

- ansibleはpipではなくaptで入れる
  - sudo apt-get update
  - sudo apt-get install software-properties-common
  - sudo apt-add-repository ppa:ansible/ansible
  - sudo apt-get update
  - sudo apt-get install ansible

## Visual Studio Code

### 拡張機能 WSL

## Windows Terminal

## pyATS

- https://developer.cisco.com/docs/pyats-getting-started/

```bash
pip install "pyats[full]"
```

```bash
iida@FCCLS0008993-00:/mnt/c/Users/iida$ pyats version check
You are currently running pyATS version: 21.5
Python: 3.8.5 [64bit]

  Package                      Version
  ---------------------------- -------
  genie                        21.5
  genie.libs.clean             21.5
  genie.libs.conf              21.5
  genie.libs.filetransferutils 21.5.1
  genie.libs.health            21.5
  genie.libs.ops               21.5
  genie.libs.parser            21.5
  genie.libs.robot             21.5.1
  genie.libs.sdk               21.5.2
  genie.telemetry              21.5
  genie.trafficgen             21.5
  pyats                        21.5
  pyats.aereport               21.5
  pyats.aetest                 21.5
  pyats.async                  21.5
  pyats.connections            21.5
  pyats.contrib                21.5
  pyats.datastructures         21.5
  pyats.easypy                 21.5
  pyats.kleenex                21.5
  pyats.log                    21.5
  pyats.reporter               21.5
  pyats.results                21.5
  pyats.robot                  21.5.1
  pyats.tcl                    21.5
  pyats.topology               21.5
  pyats.utils                  21.5.2
  unicon                       21.5
  unicon.plugins               21.5
```

## ntc-templates

<https://github.com/networktocode/ntc-templates>

pipでインストールすることもできるけど、肝心のtextfsmファイルがどこに配置されたのか分かりづらいので`git clone`するか、zipでダウンロードする。

```bash
git clone https://github.com/networktocode/ntc-templates.git
Cloning into 'ntc-templates'...
remote: Enumerating objects: 9254, done.
remote: Counting objects: 100% (87/87), done.
remote: Compressing objects: 100% (66/66), done.
remote: Total 9254 (delta 44), reused 47 (delta 21), pack-reused 9167
Receiving objects: 100% (9254/9254), 2.53 MiB | 2.45 MiB/s, done.
Resolving deltas: 100% (5151/5151), done.
Updating files: 100% (1832/1832), done.
```

# Ansible関連

## ansible.cfgの場所

ansible.cfgファイルの場所は以下の順番で読み込まれる。共通的な設定がほとんどなので`~/.ansible.cfg`で設定するのがよい。

- ANSIBLE_CONFIG (環境変数が設定されている場合)
- ansible.cfg (現在のディレクトリー)
- ~/.ansible.cfg (ホームディレクトリー)
- /etc/ansible/ansible.cfg




## role

プレイブックを作るときにはロールを積極的に活用した方がよい。
ディレクトリ構造は`ansible-galaxy init`で作ると簡単。

```bash
iida@FCCLS0008993-00:~/git/ansible-in-wsl/roles$ ansible-galaxy init bgp_neighbors
- Role bgp_neighbors was created successfully

iida@FCCLS0008993-00:~/git/ansible-in-wsl/roles$ tree .
.
└── bgp_neighbors
    ├── README.md
    ├── defaults
    │   └── main.yml
    ├── files
    ├── handlers
    │   └── main.yml
    ├── meta
    │   └── main.yml
    ├── tasks
    │   └── main.yml
    ├── templates
    ├── tests
    │   ├── inventory
    │   └── test.yml
    └── vars
        └── main.yml

9 directories, 9 files
iida@FCCLS0008993-00:~/git/ansible-in-wsl/roles$ 
```

使いたいntc-templatesのtextfsmファイルはfilesあたりに格納しておけばよい。

defaults/main.ymlにはそのロールで使う静的変数を格納するので、textfsmファイルへのパスを変数として指定しておくと便利。

```yaml
---

# ntc-templatesのtextfsmファイル
NTC_PATH: "{{ role_path + 'files/cisco_xr_show_bgp_neighbors.textfsm' }}"
```


