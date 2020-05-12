# Global Imports
import json
from collections import defaultdict

# Metaparser
from genie.metaparser import MetaParser

# =============================================
# Collection for '/mgmt/tm/sys/turboflex/profile/all' resources
# =============================================


class SysTurboflexAllSchema(MetaParser):

    schema = {}


class SysTurboflexAll(SysTurboflexAllSchema):
    """ To F5 resource for /mgmt/tm/sys/turboflex/profile/all
    """

    cli_command = "/mgmt/tm/sys/turboflex/profile/all"

    def rest(self):

        response = self.device.get(self.cli_command)

        response_json = response.json()

        if not response_json:
            return {}

        return response_json
