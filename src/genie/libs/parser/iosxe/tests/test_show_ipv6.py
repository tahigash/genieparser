import re
import unittest
from unittest.mock import Mock

from pyats.topology import Device

from genie.metaparser.util.exceptions import SchemaEmptyParserError, \
                                             SchemaMissingKeyError

from genie.libs.parser.iosxe.show_ipv6 import ShowIpv6Neighbors,\
                                              ShowIpv6NeighborsDetail


#############################################################################
# Unittest For:
#          'show ipv6 neighbors'
#          'show ipv6 neighbors vrf {vrf}'
#          'show ipv6 neighbors {interface}'
#          'show ipv6 neighbors detail'
#          'show ipv6 neighbors vrf {vrf} detail'
#############################################################################

class test_show_ipv6_neighborrs(unittest.TestCase):
    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output1 = {
        'interface': {
            'GigabitEthernet2': {
                'interface': 'GigabitEthernet2',
                'neighbors': {
                    '2001:db8:8548:1::2': {
                        'age': '0',
                        'ip': '2001:db8:8548:1::2',
                        'link_layer_address': 'fa16.3eff.09c8',
                        'neighbor_state': 'REACH'},
                    '2001:db8:8548:1::11': {
                        'age': '-',
                        'ip': '2001:db8:8548:1::11',
                        'link_layer_address': 'aaaa.beff.bcbc',
                        'neighbor_state': 'REACH'},
                    'FE80::F816:3EFF:FEFF:9C8': {
                        'age': '1',
                        'ip': 'FE80::F816:3EFF:FEFF:9C8',
                        'link_layer_address': 'fa16.3eff.09c8',
                        'neighbor_state': 'STALE'}}},
            'GigabitEthernet4': {
                'interface': 'GigabitEthernet4',
                'neighbors': {
                    '2001:db8:c56d:1::3': {
                        'age': '0',
                        'ip': '2001:db8:c56d:1::3',
                        'link_layer_address': '5e01.c0ff.0209',
                        'neighbor_state': 'STALE'},
                    'FE80::5C01:C0FF:FEFF:209': {
                        'age': '2',
                        'ip': 'FE80::5C01:C0FF:FEFF:209',
                        'link_layer_address': '5e01.c0ff.0209',
                        'neighbor_state': 'STALE'}}}}}

    golden_output1 = {'execute.return_value': '''
        csr1kv-1#show ipv6 neighbors 
        IPv6 Address                              Age Link-layer Addr State Interface
        2001:db8:8548:1::2                                 0 fa16.3eff.09c8  REACH Gi2
        2001:db8:8548:1::11                                - aaaa.beff.bcbc  REACH Gi2
        FE80::F816:3EFF:FEFF:9C8                   1 fa16.3eff.09c8  STALE Gi2
        2001:db8:c56d:1::3                                 0 5e01.c0ff.0209  STALE Gi4
        FE80::5C01:C0FF:FEFF:209                      2 5e01.c0ff.0209  STALE Gi4
    '''}

    golden_parsed_output2 = {
        'interface': {
            'GigabitEthernet3': {
                'interface': 'GigabitEthernet3',
                'neighbors': {
                    '2001:db8:888c:1::2': {
                        'age': '0',
                        'ip': '2001:db8:888c:1::2',
                        'link_layer_address': 'fa16.3eff.1b7b',
                        'neighbor_state': 'REACH'},
                    '2001:db8:c8d1:1::11': {
                        'age': '-',
                        'ip': '2001:db8:c8d1:1::11',
                        'link_layer_address': 'bbbb.beff.bcbc',
                        'neighbor_state': 'REACH'},
                    'FE80::F816:3EFF:FEFF:1B7B': {
                        'age': '0',
                        'ip': 'FE80::F816:3EFF:FEFF:1B7B',
                        'link_layer_address': 'fa16.3eff.1b7b',
                        'neighbor_state': 'REACH'}}},
            'GigabitEthernet5': {
                'interface': 'GigabitEthernet5',
                'neighbors': {
                    '2001:db8:c8d1:1::3': {
                        'age': '0',
                        'ip': '2001:db8:c8d1:1::3',
                        'link_layer_address': '5e01.c0ff.0209',
                        'neighbor_state': 'REACH'},
                    'FE80::5C01:C0FF:FEFF:209': {
                        'age': '1',
                        'ip': 'FE80::5C01:C0FF:FEFF:209',
                        'link_layer_address': '5e01.c0ff.0209',
                        'neighbor_state': 'STALE'}}}}}

    golden_output2 = {'execute.return_value': '''
        csr1kv-1#show ipv6 neighbors vrf vrf1
        IPv6 Address                              Age Link-layer Addr State Interface
        2001:db8:888c:1::2                                 0 fa16.3eff.1b7b  REACH Gi3
        2001:db8:c8d1:1::11                                - bbbb.beff.bcbc  REACH Gi3
        FE80::F816:3EFF:FEFF:1B7B                   0 fa16.3eff.1b7b  REACH Gi3
        2001:db8:c8d1:1::3                                 0 5e01.c0ff.0209  REACH Gi5
        FE80::5C01:C0FF:FEFF:209                      1 5e01.c0ff.0209  STALE Gi5
    '''}

    golden_parsed_output3 = {
        "interface": {
            "GigabitEthernet3.90": {
                "interface": "GigabitEthernet3.90",
                "neighbors": {
                    "FE80::5C00:40FF:FEFF:209": {
                        "age": "22",
                        "ip": "FE80::5C00:40FF:FEFF:209",
                        "link_layer_address": "5e00.40ff.0209",
                        "neighbor_state": "STALE"
                    }
                }
            }
        }
    }
    golden_output3 = {'execute.return_value': '''
        show ipv6 neighbors Gi3.90
        IPv6 Address                              Age Link-layer Addr State Interface
        FE80::5C00:40FF:FEFF:209                     22 5e00.40ff.0209  STALE Gi3.90
    '''}

    golden_parsed_output4 = {
        "interface": {
            "GigabitEthernet3.420": {
                "interface": "GigabitEthernet3.420",
                "neighbors": {
                    "FE80::5C00:40FF:FEFF:209": {
                        "age": "7",
                        "ip": "FE80::5C00:40FF:FEFF:209",
                        "link_layer_address": "5e00.40ff.0209",
                        "neighbor_state": "STALE"
                    }
                }
            }
        }
    }
    golden_output4 = {'execute.return_value': '''
        R1_xe#show ipv6 neighbors vrf VRF1 Gi3.420
        IPv6 Address                              Age Link-layer Addr State Interface
        FE80::5C00:40FF:FEFF:209                      7 5e00.40ff.0209  STALE Gi3.420
    '''}

    def test_show_ipv6_neighbors_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowIpv6Neighbors(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_show_ipv6_neighbors_golden1(self):
        self.device = Mock(**self.golden_output1)
        obj = ShowIpv6Neighbors(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output1)

    def test_show_ipv6_neighbors_vrf_golden2(self):
        self.device = Mock(**self.golden_output2)
        obj = ShowIpv6Neighbors(device=self.device)
        parsed_output = obj.parse(vrf='vrf1')
        self.assertEqual(parsed_output, self.golden_parsed_output2)

    def test_show_ipv6_neighbors_vrf_golden3(self):
        self.device = Mock(**self.golden_output3)
        obj = ShowIpv6Neighbors(device=self.device)
        parsed_output = obj.parse(interface='Gi3.90')
        self.assertEqual(parsed_output, self.golden_parsed_output3)

    def test_show_ipv6_neighbors_vrf_golden4(self):
        self.device = Mock(**self.golden_output3)
        obj = ShowIpv6Neighbors(device=self.device)
        parsed_output = obj.parse(vrf='VRF1', interface='Gi3.420')
        self.assertEqual(parsed_output, self.golden_parsed_output3)


class test_show_ipv6_neighbors_detail(unittest.TestCase):

    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}    

    golden_parsed_output1 = {
        'interface': {
            'GigabitEthernet2.110': {
                'interface': 'GigabitEthernet2.110',
                'neighbors': {
                    'FE80::F816:3EFF:FEFF:F3DC': {
                        'age': '0',
                        'ip': 'FE80::F816:3EFF:FEFF:F3DC',
                        'link_layer_address': 'fa16.3eff.f3dc',
                        'neighbor_state': 'REACH',
                        'trlv': '0'}}},
            'GigabitEthernet2.115': {
                'interface': 'GigabitEthernet2.115',
                    'neighbors': {
                        'FE80::F816:3EFF:FEFF:F3DC': {
                            'age': '2',
                            'ip': 'FE80::F816:3EFF:FEFF:F3DC',
                            'link_layer_address': 'fa16.3eff.f3dc',
                            'neighbor_state': 'STALE',
                            'trlv': '0'}}},
            'GigabitEthernet2.90': {
                'interface': 'GigabitEthernet2.90',
                    'neighbors': {
                        'FE80::F816:3EFF:FEFF:F3DC': {
                            'age': '0',
                            'ip': 'FE80::F816:3EFF:FEFF:F3DC',
                            'link_layer_address': 'fa16.3eff.f3dc',
                            'neighbor_state': 'REACH',
                            'trlv': '0'}}},
            'GigabitEthernet3.110': {
                'interface': 'GigabitEthernet3.110',
                    'neighbors': {
                        'FE80::5C00:C0FF:FEFF:209': {
                            'age': '4',
                            'ip': 'FE80::5C00:C0FF:FEFF:209',
                            'link_layer_address': '5e00.c0ff.0209',
                            'neighbor_state': 'STALE',
                            'trlv': '0'}}},
            'GigabitEthernet3.115': {
                'interface': 'GigabitEthernet3.115',
                    'neighbors': {
                        'FE80::5C00:C0FF:FEFF:209': {
                            'age': '20',
                            'ip': 'FE80::5C00:C0FF:FEFF:209',
                            'link_layer_address': '5e00.c0ff.0209',
                            'neighbor_state': 'STALE',
                            'trlv': '0'}}},
            'GigabitEthernet3.120': {
                'interface': 'GigabitEthernet3.120',
                    'neighbors': {
                        'FE80::5C00:C0FF:FEFF:209': {
                            'age': '5',
                            'ip': 'FE80::5C00:C0FF:FEFF:209',
                            'link_layer_address': '5e00.c0ff.0209',
                            'neighbor_state': 'STALE',
                            'trlv': '0'}}},
            'GigabitEthernet3.90': {
                'interface': 'GigabitEthernet3.90',
                    'neighbors': {
                        'FE80::5C00:C0FF:FEFF:209': {
                            'age': '0',
                            'ip': 'FE80::5C00:C0FF:FEFF:209',
                            'link_layer_address': '5e00.c0ff.0209',
                            'neighbor_state': 'STALE',
                            'trlv': '0'}}}}}

    golden_output1 = {'execute.return_value': '''
        show ipv6 neighbors detail
        IPv6 Address                              TRLV Age Link-layer Addr State Interface
        FE80::F816:3EFF:FEFF:F3DC                   0    0 fa16.3eff.f3dc  REACH Gi2.90
        FE80::F816:3EFF:FEFF:F3DC                   0    0 fa16.3eff.f3dc  REACH Gi2.110
        FE80::F816:3EFF:FEFF:F3DC                   0    2 fa16.3eff.f3dc  STALE Gi2.115
        FE80::5C00:C0FF:FEFF:209                      0    0 5e00.c0ff.0209  STALE Gi3.90
        FE80::5C00:C0FF:FEFF:209                      0    4 5e00.c0ff.0209  STALE Gi3.110
        FE80::5C00:C0FF:FEFF:209                      0   20 5e00.c0ff.0209  STALE Gi3.115
        FE80::5C00:C0FF:FEFF:209                      0    5 5e00.c0ff.0209  STALE Gi3.120
'''}

    def test_show_ipv6_neighbors_detail_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowIpv6NeighborsDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_show_ipv6_neighbors_detail_golden1(self):
        self.device = Mock(**self.golden_output1)
        obj = ShowIpv6NeighborsDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output1)


if __name__ == '__main__':
    unittest.main()