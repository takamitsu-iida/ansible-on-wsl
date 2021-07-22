#!/usr/bin/python
from ansible.errors import AnsibleError

from io import StringIO
from textfsm import TextFSM

class FilterModule(object):
    def filters(self):
        #
        # { "filter name": function}
        #
        return {"parse_show_version": self.parse_show_version}


    def parse_show_version(self, cli_output):
        result = {}
        if not cli_output:
            return result

        table = self.get_table()

        # parse by textfsm
        parsed_list = table.ParseText(cli_output)

        # parsed_list is a list of list, in this case only one content should be parsed
        parsed = parsed_list[0]

        # convert list to dict
        header = table.header
        result['Version'] = parsed[header.index('VERSION')]
        return result


    def get_table(self):
        # textfsmのテンプレートは別ファイルにするほどのものでもないので文字列で定義する
        # 分析するのは1行だけ
        # Cisco IOS Software, 3800 Software (C3845-IPBASEK9-M), Version 15.1(4)M12a, RELEASE SOFTWARE (fc1)
        TEMPLATE = """
Value VERSION (\S+)

Start
  ^Cisco IOS Software, \S+ Software \(\S+\), Version ${VERSION}, RELEASE SOFTWARE \(fc1\) -> Record

EOF
    """

        f = StringIO(TEMPLATE.strip())
        return TextFSM(f)
