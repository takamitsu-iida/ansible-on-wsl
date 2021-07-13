#!/usr/bin/python
from ansible.errors import AnsibleError

from io import StringIO
from textfsm import TextFSM


class FilterModule(object):
    def filters(self):
        #
        # { "filter name": function}
        #
        return {"parse_ios_ping": self.parse_ios_ping}


    def parse_ios_ping(self, cli_results):
        result_list = []
        if not cli_results:
            result_list

        # cli_result is a list of dict
        #   "r.results": [
        #        {
        #            "ansible_facts": {
        #                "discovered_interpreter_python": "/usr/bin/python3"
        #            },
        #            "ansible_loop_var": "item",
        #            "changed": false,
        #            "failed": false,
        #            "invocation": {
        #                "module_args": {
        #                    "answer": null,
        #                    "check_all": false,
        #                    "command": "ping 172.20.0.41",
        #                    "newline": true,
        #                    "prompt": null,
        #                    "sendonly": false
        #                }
        #            },
        #            "item": "172.20.0.41",
        #            "stdout": "Type escape sequence to abort.\nSending 5, 100-byte ICMP Echos to 172.20.0.41, timeout is 2 seconds:\n!!!!!\nSuccess rate is 100 percent (5/5), round-trip min/avg/max = 2/3/5 ms",
        #            "stdout_lines": [
        #                "Type escape sequence to abort.",
        #                "Sending 5, 100-byte ICMP Echos to 172.20.0.41, timeout is 2 seconds:",
        #                "!!!!!",
        #                "Success rate is 100 percent (5/5), round-trip min/avg/max = 2/3/5 ms"
        #            ]
        #        },

        for cli_result in cli_results:
            stdout = cli_result.get('stdout', None)
            if stdout is None:
                continue

            # parse by textfsm
            table = self.get_table()
            parsed_list = table.ParseText(stdout)
            if not parsed_list:
                continue

            # parsed_list is a list of list, in this case only one content should be parsed
            parsed = parsed_list[0]

            header = table.header
            # convert list to dict
            d = {
                'TO': parsed[header.index('TO')],
                'RATE': parsed[header.index('RATE')],
                'RECEIVED': parsed[header.index('RECEIVED')],
                'TRANSMITTED': parsed[header.index('TRANSMITTED')],
                'RTT_MIN': parsed[header.index('RTT_MIN')],
                'RTT_AVG': parsed[header.index('RTT_AVG')],
                'RTT_MAX': parsed[header.index('RTT_MAX')]
            }
            result_list.append(d)
        return result_list


    def get_table(self):
        # Type escape sequence to abort.
        # Sending 5, 100-byte ICMP Echos to 172.20.0.44, timeout is 2 seconds:
        # !!!!!
        # Success rate is 100 percent (5/5), round-trip min/avg/max = 1/2/6 ms

        #
        # textfsmのテンプレートは別ファイルにするほどのものでもないので文字列で定義する
        #
        TEMPLATE = """
Value TO (\S+)
Value RATE (\d+)
Value RECEIVED (\d+)
Value TRANSMITTED (\d+)
Value RTT_MIN (\d+)
Value RTT_AVG (\d+)
Value RTT_MAX (\d+)

Start
  ^Type escape sequence to abort
  ^Sending \d+, \d+-byte ICMP Echos to ${TO}, timeout is \d+ seconds
  ^Success rate is\s+${RATE}\s+percent\s+\(${RECEIVED}/${TRANSMITTED}\),\s+round-trip min/avg/max =\s+${RTT_MIN}/${RTT_AVG}/${RTT_MAX}\s+ms -> Record

EOF
    """

        f = StringIO(TEMPLATE.strip())
        return TextFSM(f)
