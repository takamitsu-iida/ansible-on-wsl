# apic_fabric_show_int_status
=============================

Cisco ACIのAPICにSSH接続して`fabric xx show interface status`コマンドを実行し、その結果をパースしてHTMLファイルにします。

<BR><BR>

# Requirements

制御ノード上にPythonのTextFSMモジュールが必要です。

<BR><BR>

# Role Variables
----------------

`defaults/main.yml`に記載の変数を利用します。

下記の設定では実行した場所に`log`ディレクトリを作成し、そこに実行結果のログを作成します。


```yml
LOG_DIR: "{{ lookup('env', 'PWD') + '/log' }}"
```

<BR><BR>

# Dependencies
--------------

他のロールへの依存はありません。

<BR><BR>

# Example Playbook
------------------

実行すると指定したログディレクトリにテキストファイルとHTMLファイルが生成されます。
HTMLファイルはこのようなイメージで表示します。

![fig_fabric_show_int_status](https://user-images.githubusercontent.com/21165341/124449324-4e2c8f80-ddbe-11eb-8c23-182289e2cb5b.PNG)


<BR><BR>

# License
---------

BSD

<BR><BR>

# Author Information
--------------------

takamitsu-iida
