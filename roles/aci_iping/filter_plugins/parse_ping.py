#!/usr/bin/python
from ansible.errors import AnsibleError

from io import StringIO
from textfsm import TextFSM


class FilterModule(object):
    def filters(self):
        #
        # { "filter name": function}
        #
        return {"parse_ping": self.parse_ping}


    def parse_ping(self, cli_results):
        # cli_result is a list of dict
        # [
        #  {
        #      "ansible_facts": {
        #          "discovered_interpreter_python": "/usr/bin/python3"
        #      },
        #      "ansible_loop_var": "item",
        #      "changed": false,
        #      "failed": false,
        #      "invocation": {
        #          "module_args": {
        #              "answer": null,
        #              "check_all": false,
        #              "command": "iping -V overlay-1 nw-00-03-06-00",
        #              "newline": true,
        #              "prompt": null,
        #              "sendonly": false
        #          }
        #      },
        #      "item": "nw-00-03-06-00",
        #      "stdout": "PING 10.0.40.80 (10.0.40.80) from 10.0.40.87: 56 data bytes

        result_list = []
        if not cli_results:
            result_list

        for cli_result in cli_results:
            table = self.get_table()
            stdout = cli_result.get('stdout', None)
            if stdout is None:
                continue

            # parse by textfsm
            parsed_list = table.ParseText(stdout)

            if not parsed_list:
                continue

            # parsed_list is a list of list, in this case only one content should be parsed
            parsed = parsed_list[0]

            header = table.header
            # convert list to dict
            d = {
                'TO': parsed[header.index('TO')],
                'TRANSMITTED': parsed[header.index('TRANSMITTED')],
                'RECEIVED': parsed[header.index('RECEIVED')],
                'LOSS': parsed[header.index('LOSS')],
                'RTT_MIN': parsed[header.index('RTT_MIN')],
                'RTT_AVG': parsed[header.index('RTT_AVG')],
                'RTT_MAX': parsed[header.index('RTT_MAX')]
            }
            result_list.append(d)
        return result_list


    def get_table(self):
        # PING 10.0.40.67 (10.0.40.67) from 10.0.40.87: 56 data bytes
        # 64 bytes from 10.0.40.67: icmp_seq=0 ttl=64 time=1.247 ms
        # 64 bytes from 10.0.40.67: icmp_seq=1 ttl=64 time=0.393 ms
        # 64 bytes from 10.0.40.67: icmp_seq=2 ttl=64 time=0.413 ms
        # 64 bytes from 10.0.40.67: icmp_seq=3 ttl=64 time=0.286 ms
        # 64 bytes from 10.0.40.67: icmp_seq=4 ttl=64 time=0.294 ms
        #
        # --- 10.0.40.67 ping statistics ---
        # 5 packets transmitted, 5 packets received, 0.00% packet loss
        # round-trip min/avg/max = 0.286/0.526/1.247 ms

        # textfsmのテンプレートは別ファイルにするほどのものでもないので文字列で定義する
        TEMPLATE = """
Value TO (\S+)
Value TRANSMITTED (\d+)
Value RECEIVED (\d+)
Value LOSS (\d+(\.\d+){0,1})
Value RTT_MIN (\d+(\.\d+){0,1})
Value RTT_AVG (\d+(\.\d+){0,1})
Value RTT_MAX (\d+(\.\d+){0,1})

Start
  ^---\s+${TO}\s+ping\s+statistics\s+---
  ^${TRANSMITTED}\s+packets\s+transmitted,\s+${RECEIVED}\s+packets\s+received,\s+${LOSS}%\s+packet\s+loss
  ^round-trip\s+min/avg/max\s+=\s+${RTT_MIN}/${RTT_AVG}/${RTT_MAX}\s+ms -> Record

EOF
    """

        f = StringIO(TEMPLATE.strip())
        return TextFSM(f)
