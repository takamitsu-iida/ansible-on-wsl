# ping_loop

Cisco IOS装置にSSH接続してpingコマンドを実行します。結果をHTMLで可視化します。

このロールは`ctrl-c + a`で止めるまで永遠にループします。

<br>

# Requirements

制御ノード上にpython3のtextfsmモジュールが必要です。

<br>

# Role Variables

`defaults/main.yml`に定義された変数を利用します。

<br>

# Dependencies

他のロールへの依存はありません。

<br>

# Example Playbook

```yml
- name: Create log directory
  hosts: localhost
  gather_facts: false
  strategy: linear
  serial: 0
  tasks:
    - name: Create log directory if not exists
      local_action:
        module: file
        path: "{{ LOG_DIR }}"
        state: directory
        recurse: true
      changed_when: false
      run_once: true
      vars:
        LOG_DIR: "{{ lookup('env', 'PWD') }}/log"

- name: ping
  hosts: iosxr_routers
  gather_facts: false
  strategy: linear
  serial: 0
  tasks:
    - include_role:
        name: ping_loop
      vars:
        PAUSE: 60
        LOG_DIR: "{{ lookup('env', 'PWD') }}/log"
```

プレイブックを実行すると、同じロールを繰り返し実行します。
途中60秒間のインターバルを設けていますので、そのタイミングで`ctrl-c a`を打ち込めば停止します。

```bash
TASK [../../ping_loop : save ping result summary] ***
ok: [pe1 -> localhost]

TASK [../../ping_loop : pause] ***
Pausing for 60 seconds
(ctrl+C then 'C' = continue early, ctrl+C then 'A' = abort)
```

<br>

# License

BSD

# Author Information

takamitsu-iida
