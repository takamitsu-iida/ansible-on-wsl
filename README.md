# WSL上でAnsibleを動かす

Windows端末でAnsibleのプレイブック作成を快適に行うためにはWSLを利用すると便利です。
WSL内の環境をどれだけいじってもWindowsそのものが汚れることはありません。

しかしながら、つまづきやすいポイントもありますので、環境作りや制限事項といったノウハウをまとめます。

<BR>

# ツール群

<BR>

## WSL Ubuntu 20.04

【重要】WSL2ではなく、WSLを利用します。

WSL2の場合はホストマシンとなるWindowsでVPN接続を行うとインタフェースメトリックが操作されて通信できなくなる事象が発生します。
WSLならそのようなことは起こりません。

ディストリビューションはUbuntuを利用します。
Microsoft Storeが利用できない場合は個別にダウンロードして、PowerShellで以下のコマンドを実行します。

<https://docs.microsoft.com/ja-jp/windows/wsl/install-manual#installing-your-distro>


```bash
Add-AppxPackage .\app_name.appx
```

Ubuntuをインストールできたらそれを最新化します。

ですが、プロキシサーバを経由しないとインターネットに接続できない環境の場合はプロキシの設定を先に済ませます。

`~/.bashrc`の最後に以下を追記します。

```bash
## proxy setting
export http_proxy="http://username:password@proxy-server.address:8080"
export https_proxy="http://username:password@proxy-server.address:8080"
export no_proxy="127.0.0.1,localhost,10.*,172.16.*,192.168.*,your-company.com,your-company.co.jp,your-company.local"
```

`/etc/apt/apt.conf`を作成します。

```bash
Acquire::http::Proxy "http://username:password@proxy-server.address:8080";
Acquire::https::Proxy "http://username:password@proxy-server.address:8080";
```

インターネット上のgithubにアクセスするには以下のコマンドで`~/.gitconfig`を作成します。

```bash
git config --global http.proxy http://username:password@proxy-server.address:8080
git config --global https.proxy http://username:password@proxy-server.address:8080
```

`~/.gitconifg`をエディタで作成しても構いません。このような設定になると思います。

URLごとに設定を入れられる模様。

```ini
[user]
  name = ______
  email = ______@gmail.com

[core]
  quotepath = false
  autoCRLF = false

[commit]
  template = ~/.gitmessage

[http]
  proxy = http://username:password@proxy-server.address:8080

[https]
  proxy = http://username:password@proxy-server.address:8080
```

インターネットとの接続ができたらUbuntuを最新化します。

```bash
sudo apt update
sudo apt upgrade
sudo apt dist-upgrade
sudo apt autoremove
```

Python3をインストールします。

```bash
sudo apt install python3 python3-pip -y
sudo pip3 install pip -U
```

Ansibleをインストールします。

【重要】pipで個人環境に入れるのではなくaptで導入します。pipで入れた場合、踏み台経由のSSHが動作しない事象が発生しました。

```bash
sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
```

<BR>

## SSHの設定

`~/.ssh/config` に接続先の情報を記述します。
踏み台となるサーバには鍵認証でログインできるように自分の公開鍵を格納しておきます。

その踏み台の先にいる機器にはProxyCommandを設定します。

相手が古い装置の場合はSSHのアルゴリズムを追加する必要があります。

```ini
Host bastion_host
  User root
  HostName a.b.c.d
  Port 22

Host pe1
  User admin
  HostName 172.20.0.31
  Port 22
  ProxyCommand ssh -W %h:%p bastion_host

Host ce1
  User admin
  HostName 172.20.0.41
  Port 22
  ProxyCommand ssh -W %h:%p eve
  KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
  Ciphers aes128-ctr,aes192-ctr,aes256-ctr

Host x.x.x.x
  User cisco
  KexAlgorithms +diffie-hellman-group1-sha1
  Ciphers aes128-cbc,3des-cbc,aes192-cbc,aes256-cbc
```

<BR>

## アンチウィルスソフトの設定追加

WSLを導入するとWindowsの中に独立したネットワークが作られ、NATして外部と通信するようになります。
Windowsのアンチウィルスソフトからすると、知らないネットワークからの通信が出入りすることになりますので、ファイアウォール・ルールを追加しないと通信を遮断されてしまいます。
Symantec Endpoint Protectionの場合、「不一致IPトラフィックの設定」を「IPトラフィックを許可する」にした上で、以下のルールを追加します。

- 22番ポート宛の発信通信を許可
- 22番ポート着の着信通信を許可
- 23番ポート宛の発信通信を許可
- 23番ポート宛の着信通信を許可

HTTP系の通信は対処不要でした。
WSLから外部にでる通信がうまくいかない場合、まずはアンチウィルスソフトのファイアウォール・ルールを疑ってみましょう。

<BR>

## Visual Studio Code

WindowsにVisual Studio Codeを導入します。

<BR>

### 拡張機能 WSL

拡張機能WSLを導入すると、Windows上のVisual Studio Codeから直接WSLのシェルを利用できます。

<BR>

## Windows Terminal

【おすすめ】WSLのターミナルはデフォルトのままだと使いづらいので、Windows Terminalを別途導入します。

<https://github.com/microsoft/terminal>

Windows Terminalを開いたときに開くシェルをWSLにするには、JSONの設定ファイルを開いてdefaultProfileをインストールしたUbuntuのGUIDに置き換えるだけです。

<https://qiita.com/hotaru51/items/8a5904301e2427862fb8>

<BR>

## ntc-templates

<https://github.com/networktocode/ntc-templates>

pipでインストールすることもできますが、
肝心のtextfsmファイルがどこに配置されたのか分かりづらいので`git clone`するかzipでダウンロードして必要なテンプレートだけを利用します。

といっても、簡単なものはそのまま利用できますが、
`show bgp neighbors`コマンドの出力のように複雑な構造のものは自前で作ることが多いです。

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

<BR><BR>

# EVE-NG関連

ネットワーク機器をansibleで操作することを想定して、仮想のネットワーク環境をEVE-NGで整えます。

サーバを1台調達して、そこにVMwareを入れて、VMwareの上にEVE-NGを導入します。

＜追記予定＞


<BR><BR>

# Ansible関連

WSLに特化した留意事項は特にありません。普通に動きます。

## ansible.cfgの場所

ansible.cfgファイルの場所は以下の順番で読み込まれます。共通的な設定がほとんどなので`~/.ansible.cfg`で設定しています。

- ANSIBLE_CONFIG (環境変数が設定されている場合)
- ansible.cfg (現在のディレクトリー)
- ~/.ansible.cfg (ホームディレクトリー)
- /etc/ansible/ansible.cfg

現時点のansible.cfgは以下の通り。

```ini
#
# ansible.cfg
# https://github.com/ansible/ansible/blob/devel/examples/ansible.cfg
#

[inventory]

# List of enabled inventory plugins and the order in which they are used.
# enable_plugins = host_list, script, auto, yaml, ini, toml
enable_plugins = ini, yaml, host_list

[defaults]

# ansible-vaultコマンドで使うパスワードはgitに含めない場所に保管
vault_password_file = ~/.vault_password

inventory = ./inventories/dev
# inventory = ./inventories/home
# inventory = ./inventories/dynamic

# library = ./library
# module_utils = ./module_utils
# roles_path = ./roles

# Paths to search for collections, colon separated
# collections_paths = ~/.ansible/collections:/usr/share/ansible/collections:/home/iida/.local/lib/python3.8/site-packages/ansible_collections

# ログファイルの指定をすると、実行ログが残る
# 巨大になるので、定期的に削除すること

log_path = {{CWD}}/log/ansible.log

# smart - gather by default, but don't regather if already gathered
# implicit - gather by default, turn off with gather_facts: False
# explicit - do not gather by default, must say gather_facts: True
gathering = implicit

# Host key checking is enabled by default
# SSH接続時のリモートホストの鍵をローカルのknown_hostsと比較するか
# Vagrant環境やEVE-NG、VIRL、CMLではFalseにしておく
host_key_checking = False

# 画面表示の形式
# debugにすると\nがちゃんと改行される
stdout_callback = debug
# stdout_callback = default
# stdout_callback = yaml

# 同一タスクを複数ホストに適用する場合の同時実行数
forks = 10

# 非同期実行時のポーリング間隔
# poll_interval   = 0.001

# SSH接続方式
transport = smart

[ssh_connection]

# network_cliには適用されない
# ssh_args = -F ssh_config

[paramiko_connection]

# キーを探さない
look_for_keys = False

# known_hostsにない場合に自動で追加
host_key_auto_add = True

[persistent_connection]

#
# https://docs.ansible.com/ansible/latest/network/user_guide/network_debug_troubleshooting.html#network-delegate-to-vs-proxycommand
#
# network_cliを使う場合、レスポンスが分割して戻ってくるとプロンプトとの一致に失敗する。
# ansible 2.7.1以降は待ち時間buffer_read_timeoutが導入された。既定は0.2秒。
# タスク単位で変えることもできる。
# - name: gather ios facts
#   cisco.ios.ios_facts:
#     gather_subset: all
#   register: result
#   vars:
#     ansible_buffer_read_timeout: 2
# ansible.cfgで設定することでグローバルに値を適用することもできる。
buffer_read_timeout = 2

#
# ansible 2.9以降では、接続のリトライ回数を指定できる
#
network_cli_retries = 3

#
# network_cliを使う場合のコマンドタイムアウト
# タスクごとにも変えられるので、show techの採取やファイルコピー操作をするときにはタイムアウトを長くする
# - name: save running-config
#   cisco.ios.ios_command:
#     commands: copy running-config startup-config
#     vars:
#       ansible_command_timeout: 30
#
# 古いバージョンのansibleでは既定値10秒
# ansible2.9では既定値30秒
# command_timeout = 10
```
