import unittest
from unittest.mock import Mock
from pyats.topology import Device

from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.parser.ios.cat6k.show_platform import ShowModule, \
                                                      ShowVersion, \
                                                      Dir, \
                                                      ShowRedundancy, \
                                                      ShowInventory


class TestShowVersion(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.maxDiff = None

    empty_output = {"execute.return_value": ""}
    
    output_cat6k = {'execute.return_value': '''
        cat6k_tb1#show version
        Cisco Internetwork Operating System Software 
        IOS (tm) s72033_rp Software (s72033_rp-ADVENTERPRISEK9_WAN-M), Version 12.2(18)SXF7, RELEASE SOFTWARE (fc1)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2006 by cisco Systems, Inc.
        Compiled Thu 23-Nov-06 06:26 by kellythw
        Image text-base: 0x40101040, data-base: 0x42D98000
        
        ROM: System Bootstrap, Version 12.2(17r)S4, RELEASE SOFTWARE (fc1)
        BOOTLDR: s72033_rp Software (s72033_rp-ADVENTERPRISEK9_WAN-M), Version 12.2(18)SXF7, RELEASE SOFTWARE (fc1)
        
        cat6k_tb1 uptime is 21 weeks, 5 days, 41 minutes
        Time since cat6k_tb1 switched to active is 21 weeks, 5 days, 40 minutes
        System returned to ROM by  power cycle at 21:57:23 UTC Sat Aug 28 2010 (SP by power on)
        System image file is "disk0:s72033-adventerprisek9_wan-mz.122-18.SXF7"
        
        
        This product contains cryptographic features and is subject to United
        States and local country laws governing import, export, transfer and
        use. Delivery of Cisco cryptographic products does not imply
        third-party authority to import, export, distribute or use encryption.
        Importers, exporters, distributors and users are responsible for
        compliance with U.S. and local country laws. By using this product you
        agree to comply with applicable laws and regulations. If you are unable
        to comply with U.S. and local laws, return this product immediately.
        
        A summary of U.S. laws governing Cisco cryptographic products may be found at:
        http://www.cisco.com/wwl/export/crypto/tool/stqrg.html
        
        If you require further assistance please contact us by sending email to
        export@cisco.com.
        
        cisco WS-C6503-E (R7000) processor (revision 1.4) with 983008K/65536K bytes of memory.
        Processor board ID FXS1821Q2H9
        SR71000 CPU at 600Mhz, Implementation 0x504, Rev 1.2, 512KB L2 Cache
        Last reset from s/w reset
        SuperLAT software (copyright 1990 by Meridian Technology Corp).
        X.25 software, Version 3.0.0.
        Bridging software.
        TN3270 Emulation software.
        1 Virtual Ethernet/IEEE 802.3 interface
        50 Gigabit Ethernet/IEEE 802.3 interfaces
        1917K bytes of non-volatile configuration memory.
        8192K bytes of packet buffer memory.
        
        65536K bytes of Flash internal SIMM (Sector size 512K).
        Configuration register is 0x2102

    '''}
    parsed_output_cat6k = {
        'version': {
            'bootldr_version': 's72033_rp Software (s72033_rp-ADVENTERPRISEK9_WAN-M), Version 12.2(18)SXF7, RELEASE SOFTWARE (fc1)',
            'chassis': 'WS-C6503-E',
            'compiled_by': 'kellythw',
            'compiled_date': 'Thu 23-Nov-06 06:26',
            'cpu': {
                'implementation': '0x504',
                'l2_cache': '512KB',
                'name': 'SR71000',
                'rev': '1.2',
                'speed': '600Mhz',
            },
            'curr_config_register': '0x2102',
            'hostname': 'cat6k_tb1',
            'image': {
                'data_base': '0x42D98000',
                'text_base': '0x40101040',
            },
            'image_id': 's72033_rp-ADVENTERPRISEK9_WAN-M',
            'interfaces': {
                'gigabit_ethernet': 50,
                'virtual_ethernet': 1,
            },
            'last_reset': 's/w',
            'main_mem': '983008',
            'memory': {
                'flash_internal_SIMM': 65536,
                'non_volatile_conf': 1917,
                'packet_buffer': 8192,
            },
            'os': 'IOS',
            'platform': 's72033_rp',
            'processor_board_id': 'FXS1821Q2H9',
            'processor_type': 'R7000',
            'returned_to_rom_by': 'power cycle at 21:57:23 UTC Sat Aug 28 2010 (SP by power on)',
            'rom': 'System Bootstrap, Version 12.2(17r)S4, RELEASE SOFTWARE',
            'rom_version': '(fc1)',
            'softwares': ['SuperLAT software (copyright 1990 by Meridian Technology Corp).', 'X.25 software, Version 3.0.0.', 'Bridging software.', 'TN3270 Emulation software.'],
            'system_image': 'disk0:s72033-adventerprisek9_wan-mz.122-18.SXF7',
            'uptime': '21 weeks, 5 days, 41 minutes',
            'version': '12.2(18)SXF7',
        },
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowVersion(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_show_version_1(self):
        self.device = Mock(**self.output_cat6k)
        obj = ShowVersion(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.parsed_output_cat6k)


class TestDir(unittest.TestCase):
    empty_output = {"execute.return_value": ""}
    golden_output = {'execute.return_value': '''
        cat6k_tb1#dir
        Directory of disk0:/
        
            1  -rw-    82524740  Oct 28 2009 19:07:04 +00:00  s72033-adventerprisek9_wan-mz.122-18.SXF7
            2  -rw-   200200276   Feb 3 2010 22:27:04 +00:00  s72033-adventerprisek9_wan_dbg-vz.CARSON_INTEG_100202
            3  -rw-   201459508   Feb 3 2010 23:18:40 +00:00  s72033-adventerprisek9_wan_dbg-vz.SIERRA_INTEG_100202
            4  -rw-        4485  Jul 21 2015 14:11:10 +00:00  cat6k_tb1-confg
            5  -rw-        4734  Nov 27 2017 21:32:46 +00:00  config_cat6k_tb1_native
        
        512065536 bytes total (27852800 bytes free)
        '''}

    golden_parsed_output = {
        'dir': {
            'dir': 'disk0:/',
            'disk0:/': {
                'bytes_free': '27852800',
                'bytes_total': '512065536',
                'files': {
                    'cat6k_tb1-confg': {
                        'index': '4',
                        'last_modified_date': 'Jul 21 2015 14:11:10 +00:00',
                        'permissions': '-rw-',
                        'size': '4485',
                    },
                    'config_cat6k_tb1_native': {
                        'index': '5',
                        'last_modified_date': 'Nov 27 2017 21:32:46 +00:00',
                        'permissions': '-rw-',
                        'size': '4734',
                    },
                    's72033-adventerprisek9_wan-mz.122-18.SXF7': {
                        'index': '1',
                        'last_modified_date': 'Oct 28 2009 19:07:04 +00:00',
                        'permissions': '-rw-',
                        'size': '82524740',
                    },
                    's72033-adventerprisek9_wan_dbg-vz.CARSON_INTEG_100202': {
                        'index': '2',
                        'last_modified_date': 'Feb 3 2010 22:27:04 +00:00',
                        'permissions': '-rw-',
                        'size': '200200276',
                    },
                    's72033-adventerprisek9_wan_dbg-vz.SIERRA_INTEG_100202': {
                        'index': '3',
                        'last_modified_date': 'Feb 3 2010 23:18:40 +00:00',
                        'permissions': '-rw-',
                        'size': '201459508',
                    },
                },
            },
        },
    }


    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = Dir(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_dir_1(self):
        self.device = Mock(**self.golden_output)
        obj = Dir(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


class TestShowRedundancy(unittest.TestCase):
    empty_output = {"execute.return_value": ""}
    golden_output = {'execute.return_value': '''
        cat6k_tb1#show redundancy
        Redundant System Information :
        ------------------------------
            Available system uptime = 21 weeks, 5 days, 1 hour, 3 minutes
        Switchovers system experienced = 0
                    Standby failures = 0
                Last switchover reason = none
        
                        Hardware Mode = Simplex
            Configured Redundancy Mode = sso
            Operating Redundancy Mode = sso
                    Maintenance Mode = Disabled
                        Communications = Down      Reason: Simplex mode
        
        Current Processor Information :
        -------------------------------
                    Active Location = slot 1
                Current Software state = ACTIVE
            Uptime in current state = 21 weeks, 5 days, 1 hour, 2 minutes
                        Image Version = Cisco Internetwork Operating System Software 
        IOS (tm) s72033_rp Software (s72033_rp-ADVENTERPRISEK9_WAN-M), Version 12.2(18)SXF7, RELEASE SOFTWARE (fc1)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2006 by cisco Systems, Inc.
        Compiled Thu 23-Nov-06 06:26 by kellythw
                                BOOT = 
                        CONFIG_FILE = 
                            BOOTLDR = 
                Configuration register = 0x2102
        
        Peer (slot: unavailable) information is not available because it is in 'DISABLED' state

    '''}
    golden_parsed_output = {
        'red_sys_info': {
            'available_system_uptime': '21 weeks, 5 days, 1 hour, 3 minutes',
            'communications': 'Down',
            'communications_reason': 'Simplex mode',
            'conf_red_mode': 'sso',
            'hw_mode': 'Simplex',
            'last_switchover_reason': 'none',
            'maint_mode': 'Disabled',
            'oper_red_mode': 'sso',
            'standby_failures': '0',
            'switchovers_system_experienced': '0',
        },
        'slot': {
            'slot 1': {
                'compiled_by': 'kellythw',
                'compiled_date': 'Thu 23-Nov-06 06:26',
                'config_register': '0x2102',
                'curr_sw_state': 'ACTIVE',
                'image_id': 's72033_rp-ADVENTERPRISEK9_WAN-M',
                'image_ver': 'Cisco Internetwork Operating System Software',
                'os': 'IOS',
                'platform': 's72033_rp',
                'uptime_in_curr_state': '21 weeks, 5 days, 1 hour, 2 minutes',
                'version': '12.2(18)SXF7',
            },
        },
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowRedundancy(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_show_redundancy_1(self):
        self.device = Mock(**self.golden_output)
        obj = ShowRedundancy(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


class TestShowInventory(unittest.TestCase):
    empty_output = {"execute.return_value": ""}
    golden_output = {'execute.return_value': '''
        cat6k_tb1#show inventory
        NAME: "WS-C6503-E", DESCR: "Cisco Systems Catalyst 6500 3-slot Chassis System"
        PID: WS-C6503-E        , VID: V03, SN: FXS1821Q2H9
        
        NAME: "CLK-7600 1", DESCR: "OSR-7600 Clock FRU 1"
        PID: CLK-7600          , VID:    , SN: FXS181101V4
        
        NAME: "CLK-7600 2", DESCR: "OSR-7600 Clock FRU 2"
        PID: CLK-7600          , VID:    , SN: FXS181101V4
        
        NAME: "1", DESCR: "WS-SUP720-3BXL 2 ports Supervisor Engine 720 Rev. 5.6"
        PID: WS-SUP720-3BXL    , VID: V05, SN: SAL11434P2C
        
        NAME: "msfc sub-module of 1", DESCR: "WS-SUP720 MSFC3 Daughterboard Rev. 3.1"
        PID: WS-SUP720         , VID:    , SN: SAL11434N9G
        
        NAME: "switching engine sub-module of 1", DESCR: "WS-F6K-PFC3BXL Policy Feature Card 3 Rev. 1.8"
        PID: WS-F6K-PFC3BXL    , VID: V01, SN: SAL11434LYG
        
        NAME: "2", DESCR: "WS-X6748-GE-TX CEF720 48 port 10/100/1000mb Ethernet Rev. 2.6"
        PID: WS-X6748-GE-TX    , VID: V02, SN: SAL1128UPQ9
        
        NAME: "switching engine sub-module of 2", DESCR: "WS-F6700-DFC3CXL Distributed Forwarding Card 3 Rev. 1.1"
        PID: WS-F6700-DFC3CXL  , VID: V01, SN: SAL1214LAG5
        
        NAME: "WS-C6503-E-FAN 1", DESCR: "Enhanced 3-slot Fan Tray 1"
        PID: WS-C6503-E-FAN    , VID: V02, SN: DCH183500KW
        
        NAME: "PS 1 PWR-1400-AC", DESCR: "AC power supply, 1400 watt 1"
        PID: PWR-1400-AC       , VID: V01, SN: ABC0830J127
    '''}
    golden_parsed_output = {
        'index': {
            1: {
                'descr': 'Cisco Systems Catalyst 6500 3-slot Chassis System',
                'name': 'WS-C6503-E',
                'pid': 'WS-C6503-E',
                'sn': 'FXS1821Q2H9',
                'vid': 'V03',
            },
            2: {
                'descr': 'OSR-7600 Clock FRU 1',
                'name': 'CLK-7600 1',
                'pid': 'CLK-7600',
                'sn': 'FXS181101V4',
            },
            3: {
                'descr': 'OSR-7600 Clock FRU 2',
                'name': 'CLK-7600 2',
                'pid': 'CLK-7600',
                'sn': 'FXS181101V4',
            },
            4: {
                'descr': 'WS-SUP720-3BXL 2 ports Supervisor Engine 720 Rev. 5.6',
                'name': '1',
                'pid': 'WS-SUP720-3BXL',
                'sn': 'SAL11434P2C',
                'vid': 'V05',
            },
            5: {
                'descr': 'WS-SUP720 MSFC3 Daughterboard Rev. 3.1',
                'name': 'msfc sub-module of 1',
                'pid': 'WS-SUP720',
                'sn': 'SAL11434N9G',
            },
            6: {
                'descr': 'WS-F6K-PFC3BXL Policy Feature Card 3 Rev. 1.8',
                'name': 'switching engine sub-module of 1',
                'pid': 'WS-F6K-PFC3BXL',
                'sn': 'SAL11434LYG',
                'vid': 'V01',
            },
            7: {
                'descr': 'WS-X6748-GE-TX CEF720 48 port 10/100/1000mb Ethernet Rev. 2.6',
                'name': '2',
                'pid': 'WS-X6748-GE-TX',
                'sn': 'SAL1128UPQ9',
                'vid': 'V02',
            },
            8: {
                'descr': 'WS-F6700-DFC3CXL Distributed Forwarding Card 3 Rev. 1.1',
                'name': 'switching engine sub-module of 2',
                'pid': 'WS-F6700-DFC3CXL',
                'sn': 'SAL1214LAG5',
                'vid': 'V01',
            },
            9: {
                'descr': 'Enhanced 3-slot Fan Tray 1',
                'name': 'WS-C6503-E-FAN 1',
                'pid': 'WS-C6503-E-FAN',
                'sn': 'DCH183500KW',
                'vid': 'V02',
            },
            10: {
                'descr': 'AC power supply, 1400 watt 1',
                'name': 'PS 1 PWR-1400-AC',
                'pid': 'PWR-1400-AC',
                'sn': 'ABC0830J127',
                'vid': 'V01',
            },
        },
    }

    golden_output_2 = {'execute.return_value': '''
        NAME: "WS-C6506-E", DESCR: "Cisco Systems, Inc. Catalyst 6500 6-slot Chassis System"
        PID: WS-C6506-E        ,                     VID: V05, SN: SAL123456ET

        NAME: "WS-C6K-VTT-E 1", DESCR: "VTT-E FRU 1"
        PID: WS-C6K-VTT-E      ,                     VID:    , SN: SMT6789A123

        NAME: "WS-C6K-VTT-E 2", DESCR: "VTT-E FRU 2"
        PID: WS-C6K-VTT-E      ,                     VID:    , SN: SMT6789A876

        NAME: "WS-C6K-VTT-E 3", DESCR: "VTT-E FRU 3"
        PID: WS-C6K-VTT-E      ,                     VID:    , SN: SMT6789A456

        NAME: "CLK-7600 1", DESCR: "OSR-7600 Clock FRU 1"
        PID: CLK-7600          ,                     VID:    , SN: SMT8760A198

        NAME: "CLK-7600 2", DESCR: "OSR-7600 Clock FRU 2"
        PID: CLK-7600          ,                     VID:    , SN: SMT8760A198

        NAME: "1", DESCR: "C6800-16P10G-XL DCEF2T 4 port 40GE / 16 port 10GE Rev. 2.1"
        PID: C6800-16P10G-XL   ,                     VID: V03, SN: JAE88776PMK

        NAME: "C6800-DFC-XL Distributed Forwarding Card 4 EARL 1 sub-module of 1", DESCR: "C6800-DFC-XL Distributed Forwarding Card 4 Rev. 2.1"
        PID: C6800-DFC-XL      ,                     VID:    , SN: JAE88776PMK

        NAME: "Transceiver Te1/1", DESCR: "SFP+ Transceiver 10Gbase-SR Te1/1L
        PID: SFP-10G-SR         ,                     VID: V03 , SN: AVD656567YT     

        NAME: "Transceiver Te1/3", DESCR: "SFP+ Transceiver 10Gbase-SR Te1/3"
        PID: SFP-10G-SR         ,                     VID: V03 , SN: AVD989078Z2     

        NAME: "Transceiver Te1/5", DESCR: "SFP+ Transceiver 10Gbase-SR Te1/5"
        PID: SFP-10G-SR         ,                     VID: V03 , SN: AVD012345MB     

        NAME: "Transceiver Te1/7", DESCR: "SFP+ Transceiver 10Gbase-SR Te1/7"
        PID: SFP-10G-SR         ,                     VID: V03 , SN: AVD012345LL     

        NAME: "Transceiver Te1/9", DESCR: "SFP+ Transceiver 10Gbase-SR Te1/9"
        PID: SFP-10G-SR         ,                     VID: V03 , SN: AVD012345LF     

        NAME: "Transceiver Te1/11", DESCR: "SFP+ Transceiver 10Gbase-SR Te1/11"
        PID: SFP-10G-SR         ,                     VID: V03 , SN: AVD012345L4     

        NAME: "Transceiver Te1/13", DESCR: "SFP+ Transceiver 10Gbase-SR Te1/13"
        PID: SFP-10G-SR         ,                     VID: V03 , SN: AVD012345MN     

        NAME: "Transceiver Te1/15", DESCR: "SFP+ Transceiver 10Gbase-SR Te1/15"
        PID: SFP-10G-SR         ,                     VID: V03 , SN: AVD012345LE     

        NAME: "2", DESCR: "C6800-16P10G-XL DCEF2T 4 port 40GE / 16 port 10GE Rev. 2.1"
        PID: C6800-16P10G-XL   ,                     VID: V03, SN: JAE65432PMG

        NAME: "C6800-DFC-XL Distributed Forwarding Card 4 EARL 1 sub-module of 2", DESCR: "C6800-DFC-XL Distributed Forwarding Card 4 Rev. 2.1"
        PID: C6800-DFC-XL      ,                     VID:    , SN: JAE65432PM

        NAME: "Transceiver Te2/1", DESCR: "SFP+ Transceiver 10Gbase-SR Te2/1"
        PID: SFP-10G-SR         ,                     VID: V03 , SN: AVD012345RB     

        NAME: "Transceiver Te2/3", DESCR: "SFP+ Transceiver 10Gbase-SR Te2/3"
        PID: SFP-10G-SR         ,                     VID: V03 , SN: AVD012345RF     

        NAME: "Transceiver Te2/5", DESCR: "SFP+ Transceiver 10Gbase-SR Te2/5"
        PID: SFP-10G-SR         ,                     VID: V03 , SN: AVD0908070T     

        NAME: "Transceiver Te2/7", DESCR: "SFP+ Transceiver 10Gbase-SR Te2/7"
        PID: SFP-10G-SR         ,                     VID: V03 , SN: AVD097896CU     

        NAME: "3", DESCR: "C6800-48P-TX-XL 48 ports DCEF-XL 48P 10/100/1000MB Ethernet Rev. 1.0"
        PID: C6800-48P-TX-XL   ,                     VID: V01, SN: JAE264857DC

        NAME: "WS-F6K-DFC4-AXL Distributed Forwarding Card 4 EARL 1 sub-module of 3", DESCR: "WS-F6K-DFC4-AXL Distributed Forwarding Card 4 Rev. 1.0"
        PID: WS-F6K-DFC4-AXL   ,                     VID:    , SN: JAE264857DO

        NAME: "5", DESCR: "VS-SUP2T-10G 5 ports Supervisor Engine 2T 10GE w/ CTS Rev. 2.1"
        PID: VS-SUP2T-10G      ,                     VID: V06, SN: JAE264233CQ

        NAME: "msfc sub-module of 5", DESCR: "VS-F6K-MSFC5 CPU Daughterboard Rev. 3.1"
        PID: VS-F6K-MSFC5      ,                     VID:    , SN: JAE66880PAV

        NAME: "VS-F6K-PFC4 Policy Feature Card 4 EARL 1 sub-module of 5", DESCR: "VS-F6K-PFC4 Policy Feature Card 4 Rev. 3.0"
        PID: VS-F6K-PFC4       ,                     VID: V04, SN: JAE66880GWE

        NAME: "Transceiver Te5/4", DESCR: "X2 Transceiver 10Gbase-SR Te5/4"
        PID: X2-10GB-SR        ,                     VID: V06 , SN: FNS00002Q8Q

        NAME: "6", DESCR: "VS-SUP2T-10G 5 ports Supervisor Engine 2T 10GE w/ CTS Rev. 2.1"
        PID: VS-SUP2T-10G      ,                     VID: V06, SN: JAE77720W0N

        NAME: "msfc sub-module of 6", DESCR: "VS-F6K-MSFC5 CPU Daughterboard Rev. 3.1"
        PID: VS-F6K-MSFC5      ,                     VID:    , SN: JAE66880PAO

        NAME: "VS-F6K-PFC4 Policy Feature Card 4 EARL 1 sub-module of 6", DESCR: "VS-F6K-PFC4 Policy Feature Card 4 Rev. 3.0"
        PID: VS-F6K-PFC4       ,                     VID: V04, SN: JAE66880GWE

        NAME: "Transceiver Te6/4", DESCR: "X2 Transceiver 10Gbase-SR Te6/4"
        PID: X2-10GB-SR        ,                     VID: V06 , SN: FNS00002Q9B

        NAME: "WS-C6506-E-FAN 1", DESCR: "Enhanced 6-slot Fan Tray 1"
        PID: WS-C6506-E-FAN    ,                     VID: V03, SN: DCH200022UZ

        NAME: "PS 1 WS-CAC-6000W", DESCR: "AC power supply, 6000 watt 1"
        PID: WS-CAC-6000W      ,                     VID: V06, SN: ART1999F5B5

        NAME: "PS 2 WS-CAC-6000W", DESCR: "AC power supply, 6000 watt 2"
        PID: WS-CAC-6000W      ,                     VID: V06, SN: ART1999F5B8


        '''}

    golden_parsed_output_2 = {
    'index': {
        1: {
            'descr': 'Cisco Systems, Inc. Catalyst 6500 6-slot Chassis System',
            'name': 'WS-C6506-E',
            'pid': 'WS-C6506-E',
            'sn': 'SAL123456ET',
            'vid': 'V05',
        },
        2: {
            'descr': 'VTT-E FRU 1',
            'name': 'WS-C6K-VTT-E 1',
            'pid': 'WS-C6K-VTT-E',
            'sn': 'SMT6789A123',
        },
        3: {
            'descr': 'VTT-E FRU 2',
            'name': 'WS-C6K-VTT-E 2',
            'pid': 'WS-C6K-VTT-E',
            'sn': 'SMT6789A876',
        },
        4: {
            'descr': 'VTT-E FRU 3',
            'name': 'WS-C6K-VTT-E 3',
            'pid': 'WS-C6K-VTT-E',
            'sn': 'SMT6789A456',
        },
        5: {
            'descr': 'OSR-7600 Clock FRU 1',
            'name': 'CLK-7600 1',
            'pid': 'CLK-7600',
            'sn': 'SMT8760A198',
        },
        6: {
            'descr': 'OSR-7600 Clock FRU 2',
            'name': 'CLK-7600 2',
            'pid': 'CLK-7600',
            'sn': 'SMT8760A198',
        },
        7: {
            'descr': 'C6800-16P10G-XL DCEF2T 4 port 40GE / 16 port 10GE Rev. 2.1',
            'name': '1',
            'pid': 'C6800-16P10G-XL',
            'sn': 'JAE88776PMK',
            'vid': 'V03',
        },
        8: {
            'descr': 'C6800-DFC-XL Distributed Forwarding Card 4 Rev. 2.1',
            'name': 'C6800-DFC-XL Distributed Forwarding Card 4 EARL 1 sub-module of 1',
            'pid': 'SFP-10G-SR',
            'sn': 'AVD656567YT',
            'vid': 'V03',
        },
        9: {
            'descr': 'SFP+ Transceiver 10Gbase-SR Te1/3',
            'name': 'Transceiver Te1/3',
            'pid': 'SFP-10G-SR',
            'sn': 'AVD989078Z2',
            'vid': 'V03',
        },
        10: {
            'descr': 'SFP+ Transceiver 10Gbase-SR Te1/5',
            'name': 'Transceiver Te1/5',
            'pid': 'SFP-10G-SR',
            'sn': 'AVD012345MB',
            'vid': 'V03',
        },
        11: {
            'descr': 'SFP+ Transceiver 10Gbase-SR Te1/7',
            'name': 'Transceiver Te1/7',
            'pid': 'SFP-10G-SR',
            'sn': 'AVD012345LL',
            'vid': 'V03',
        },
        12: {
            'descr': 'SFP+ Transceiver 10Gbase-SR Te1/9',
            'name': 'Transceiver Te1/9',
            'pid': 'SFP-10G-SR',
            'sn': 'AVD012345LF',
            'vid': 'V03',
        },
        13: {
            'descr': 'SFP+ Transceiver 10Gbase-SR Te1/11',
            'name': 'Transceiver Te1/11',
            'pid': 'SFP-10G-SR',
            'sn': 'AVD012345L4',
            'vid': 'V03',
        },
        14: {
            'descr': 'SFP+ Transceiver 10Gbase-SR Te1/13',
            'name': 'Transceiver Te1/13',
            'pid': 'SFP-10G-SR',
            'sn': 'AVD012345MN',
            'vid': 'V03',
        },
        15: {
            'descr': 'SFP+ Transceiver 10Gbase-SR Te1/15',
            'name': 'Transceiver Te1/15',
            'pid': 'SFP-10G-SR',
            'sn': 'AVD012345LE',
            'vid': 'V03',
        },
        16: {
            'descr': 'C6800-16P10G-XL DCEF2T 4 port 40GE / 16 port 10GE Rev. 2.1',
            'name': '2',
            'pid': 'C6800-16P10G-XL',
            'sn': 'JAE65432PMG',
            'vid': 'V03',
        },
        17: {
            'descr': 'C6800-DFC-XL Distributed Forwarding Card 4 Rev. 2.1',
            'name': 'C6800-DFC-XL Distributed Forwarding Card 4 EARL 1 sub-module of 2',
            'pid': 'C6800-DFC-XL',
            'sn': 'JAE65432PM',
        },
        18: {
            'descr': 'SFP+ Transceiver 10Gbase-SR Te2/1',
            'name': 'Transceiver Te2/1',
            'pid': 'SFP-10G-SR',
            'sn': 'AVD012345RB',
            'vid': 'V03',
        },
        19: {
            'descr': 'SFP+ Transceiver 10Gbase-SR Te2/3',
            'name': 'Transceiver Te2/3',
            'pid': 'SFP-10G-SR',
            'sn': 'AVD012345RF',
            'vid': 'V03',
        },
        20: {
            'descr': 'SFP+ Transceiver 10Gbase-SR Te2/5',
            'name': 'Transceiver Te2/5',
            'pid': 'SFP-10G-SR',
            'sn': 'AVD0908070T',
            'vid': 'V03',
        },
        21: {
            'descr': 'SFP+ Transceiver 10Gbase-SR Te2/7',
            'name': 'Transceiver Te2/7',
            'pid': 'SFP-10G-SR',
            'sn': 'AVD097896CU',
            'vid': 'V03',
        },
        22: {
            'descr': 'C6800-48P-TX-XL 48 ports DCEF-XL 48P 10/100/1000MB Ethernet Rev. 1.0',
            'name': '3',
            'pid': 'C6800-48P-TX-XL',
            'sn': 'JAE264857DC',
            'vid': 'V01',
        },
        23: {
            'descr': 'WS-F6K-DFC4-AXL Distributed Forwarding Card 4 Rev. 1.0',
            'name': 'WS-F6K-DFC4-AXL Distributed Forwarding Card 4 EARL 1 sub-module of 3',
            'pid': 'WS-F6K-DFC4-AXL',
            'sn': 'JAE264857DO',
        },
        24: {
            'descr': 'VS-SUP2T-10G 5 ports Supervisor Engine 2T 10GE w/ CTS Rev. 2.1',
            'name': '5',
            'pid': 'VS-SUP2T-10G',
            'sn': 'JAE264233CQ',
            'vid': 'V06',
        },
        25: {
            'descr': 'VS-F6K-MSFC5 CPU Daughterboard Rev. 3.1',
            'name': 'msfc sub-module of 5',
            'pid': 'VS-F6K-MSFC5',
            'sn': 'JAE66880PAV',
        },
        26: {
            'descr': 'VS-F6K-PFC4 Policy Feature Card 4 Rev. 3.0',
            'name': 'VS-F6K-PFC4 Policy Feature Card 4 EARL 1 sub-module of 5',
            'pid': 'VS-F6K-PFC4',
            'sn': 'JAE66880GWE',
            'vid': 'V04',
        },
        27: {
            'descr': 'X2 Transceiver 10Gbase-SR Te5/4',
            'name': 'Transceiver Te5/4',
            'pid': 'X2-10GB-SR',
            'sn': 'FNS00002Q8Q',
            'vid': 'V06',
        },
        28: {
            'descr': 'VS-SUP2T-10G 5 ports Supervisor Engine 2T 10GE w/ CTS Rev. 2.1',
            'name': '6',
            'pid': 'VS-SUP2T-10G',
            'sn': 'JAE77720W0N',
            'vid': 'V06',
        },
        29: {
            'descr': 'VS-F6K-MSFC5 CPU Daughterboard Rev. 3.1',
            'name': 'msfc sub-module of 6',
            'pid': 'VS-F6K-MSFC5',
            'sn': 'JAE66880PAO',
        },
        30: {
            'descr': 'VS-F6K-PFC4 Policy Feature Card 4 Rev. 3.0',
            'name': 'VS-F6K-PFC4 Policy Feature Card 4 EARL 1 sub-module of 6',
            'pid': 'VS-F6K-PFC4',
            'sn': 'JAE66880GWE',
            'vid': 'V04',
        },
        31: {
            'descr': 'X2 Transceiver 10Gbase-SR Te6/4',
            'name': 'Transceiver Te6/4',
            'pid': 'X2-10GB-SR',
            'sn': 'FNS00002Q9B',
            'vid': 'V06',
        },
        32: {
            'descr': 'Enhanced 6-slot Fan Tray 1',
            'name': 'WS-C6506-E-FAN 1',
            'pid': 'WS-C6506-E-FAN',
            'sn': 'DCH200022UZ',
            'vid': 'V03',
        },
        33: {
            'descr': 'AC power supply, 6000 watt 1',
            'name': 'PS 1 WS-CAC-6000W',
            'pid': 'WS-CAC-6000W',
            'sn': 'ART1999F5B5',
            'vid': 'V06',
        },
        34: {
            'descr': 'AC power supply, 6000 watt 2',
            'name': 'PS 2 WS-CAC-6000W',
            'pid': 'WS-CAC-6000W',
            'sn': 'ART1999F5B8',
            'vid': 'V06',
        },
    },
}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowInventory(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_show_inventory_1(self):
        self.device = Mock(**self.golden_output)
        obj = ShowInventory(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)

    def test_show_inventory_2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_2)
        obj = ShowInventory(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_2)

class TestShowModule(unittest.TestCase):
    device = Device(name="aDevice")

    empty_output = {"execute.return_value": ""}

    golden_parsed_output_1 = {
        "slot": {
            "1": {
                "rp": {
                    "card_type": "Catalyst 6000 supervisor 2 (Active)",
                    "fw_ver": "6.1(3)",
                    "hw_ver": "3.9",
                    "mac_address_from": "0001.64ff.1958",
                    "mac_address_to": "0001.64ff.1959",
                    "model": "WS-X6K-S2U-MSFC2",
                    "ports": 2,
                    "serial_number": "SAD0628035C",
                    "status": "Ok",
                    "subslot": {
                        "WS-F6K-MSFC2": {
                            "hw_ver": "2.5",
                            "model": "WS-F6K-MSFC2",
                            "serial_number": "SAD062803TX",
                            "status": "Ok",
                        },
                        "WS-F6K-PFC2": {
                            "hw_ver": "3.2",
                            "model": "WS-F6K-PFC2",
                            "serial_number": "SAD062802AV",
                            "status": "Ok",
                        },
                    },
                    "sw_ver": "7.5(0.6)HUB9",
                }
            },
            "2": {
                "rp": {
                    "card_type": "Supervisor-Other",
                    "fw_ver": "Unknown",
                    "hw_ver": "0.0",
                    "mac_address_from": "0000.0000.0000",
                    "mac_address_to": "0000.0000.0000",
                    "model": "unknown",
                    "ports": 0,
                    "serial_number": "unknown",
                    "status": "Unknown",
                    "sw_ver": "Unknown",
                }
            },
            "3": {
                "lc": {
                    "card_type": "Pure SFM-mode 16 port 1000mb GBIC",
                    "fw_ver": "12.1(5r)E1",
                    "hw_ver": "1.3",
                    "mac_address_from": "0005.74ff.1b9d",
                    "mac_address_to": "0005.74ff.1bac",
                    "model": "WS-X6816-GBIC",
                    "ports": 16,
                    "serial_number": "SAL061218K3",
                    "status": "Ok",
                    "subslot": {
                        "WS-F6K-DFC": {
                            "hw_ver": "2.1",
                            "model": "WS-F6K-DFC",
                            "serial_number": "SAL06121A19",
                            "status": "Ok",
                        }
                    },
                    "sw_ver": "12.1(13)E3",
                }
            },
            "4": {
                "lc": {
                    "card_type": "Pure SFM-mode 16 port 1000mb GBIC",
                    "fw_ver": "12.1(5r)E1",
                    "hw_ver": "1.3",
                    "mac_address_from": "0005.74ff.1bcd",
                    "mac_address_to": "0005.74ff.1bdc",
                    "model": "WS-X6816-GBIC",
                    "ports": 16,
                    "serial_number": "SAL061218K8",
                    "status": "Ok",
                    "subslot": {
                        "WS-F6K-DFC": {
                            "hw_ver": "2.1",
                            "model": "WS-F6K-DFC",
                            "serial_number": "SAL06121A46",
                            "status": "Ok",
                        }
                    },
                    "sw_ver": "12.1(13)E3",
                }
            },
            "5": {
                "other": {
                    "card_type": "Switching Fabric Module-136 (Active)",
                    "fw_ver": "6.1(3)",
                    "hw_ver": "1.2",
                    "mac_address_from": "0001.00ff.0205",
                    "mac_address_to": "0001.00ff.0205",
                    "model": "WS-X6500-SFM2",
                    "ports": 0,
                    "serial_number": "SAD061701YC",
                    "status": "Ok",
                    "sw_ver": "7.5(0.6)HUB9",
                }
            },
            "6": {
                "lc": {
                    "card_type": "1 port 10-Gigabit Ethernet Module",
                    "fw_ver": "6.3(1)",
                    "hw_ver": "1.0",
                    "mac_address_from": "0002.7eff.58b5",
                    "mac_address_to": "0002.7eff.58b5",
                    "model": "WS-X6502-10GE",
                    "ports": 1,
                    "serial_number": "SAD062003CM",
                    "status": "Ok",
                    "subslot": {
                        "WS-F6K-DFC": {
                            "hw_ver": "2.3",
                            "model": "WS-F6K-DFC",
                            "serial_number": "SAL06261R0A",
                            "status": "Ok",
                        },
                        "WS-G6488": {
                            "hw_ver": "1.1",
                            "model": "WS-G6488",
                            "serial_number": "SAD062201BN",
                            "status": "Ok",
                        },
                    },
                    "sw_ver": "7.5(0.6)HUB9",
                }
            },
        }
    }

    golden_output_1 = {
        "execute.return_value": """
        Mod Ports Card Type                              Model              Serial No.
        --- ----- -------------------------------------- ------------------ -----------
          1    2  Catalyst 6000 supervisor 2 (Active)    WS-X6K-S2U-MSFC2   SAD0628035C
          2    0  Supervisor-Other                       unknown            unknown
          3   16  Pure SFM-mode 16 port 1000mb GBIC      WS-X6816-GBIC      SAL061218K3
          4   16  Pure SFM-mode 16 port 1000mb GBIC      WS-X6816-GBIC      SAL061218K8
          5    0  Switching Fabric Module-136 (Active)   WS-X6500-SFM2      SAD061701YC
          6    1  1 port 10-Gigabit Ethernet Module      WS-X6502-10GE      SAD062003CM

        Mod MAC addresses                       Hw    Fw           Sw           Status
        --- ---------------------------------- ------ ------------ ------------ -------
          1  0001.64ff.1958 to 0001.64ff.1959   3.9   6.1(3)       7.5(0.6)HUB9 Ok      
          2  0000.0000.0000 to 0000.0000.0000   0.0   Unknown      Unknown      Unknown 
          3  0005.74ff.1b9d to 0005.74ff.1bac   1.3   12.1(5r)E1   12.1(13)E3,  Ok      
          4  0005.74ff.1bcd to 0005.74ff.1bdc   1.3   12.1(5r)E1   12.1(13)E3,  Ok      
          5  0001.00ff.0205 to 0001.00ff.0205   1.2   6.1(3)       7.5(0.6)HUB9 Ok      
          6  0002.7eff.58b5 to 0002.7eff.58b5   1.0   6.3(1)       7.5(0.6)HUB9 Ok      

        Mod Sub-Module                  Model           Serial           Hw     Status 
        --- --------------------------- --------------- --------------- ------- -------
          1 Policy Feature Card 2       WS-F6K-PFC2     SAD062802AV      3.2    Ok     
          1 Cat6k MSFC 2 daughterboard  WS-F6K-MSFC2    SAD062803TX      2.5    Ok     
          3 Distributed Forwarding Card WS-F6K-DFC      SAL06121A19      2.1    Ok     
          4 Distributed Forwarding Card WS-F6K-DFC      SAL06121A46      2.1    Ok     
          6 Distributed Forwarding Card WS-F6K-DFC      SAL06261R0A      2.3    Ok     
          6 10GBASE-LR Serial 1310nm lo WS-G6488        SAD062201BN      1.1    Ok
    """
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowModule(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_show_module_1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_1)
        obj = ShowModule(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_1)

if __name__ == "__main__":
    unittest.main()
