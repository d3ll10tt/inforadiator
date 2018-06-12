import re
import os
import json
from pprint import pprint


class AnsibleFacts:

    '''Class to hold ansible facts about all platform servers'''

    _rawfacts = {}                # {hostname : {fact : values}}
    _facts = {}                   # {environment : {hostname : {fact: value}}}
    _installed_packages = set ()  # set of installed savvi rpms

    def __init__(self, facts_cache_dir):

        self.load_raw_facts(facts_cache_dir)
        self.create_hostmap(self._rawfacts)

        for host, host_facts in self._rawfacts.items():
            for pkg in host_facts['savvi_versions'].keys():
                self._installed_packages.add(pkg)

        return

    # Methods
    def dump_raw_facts(self):

        return self._rawfacts

    def load_raw_facts(self, dir):

        for file in os.listdir(dir):
            filename = os.fsdecode(file)
            if filename.endswith(".local"):
                with open(os.path.join(dir, filename), encoding='utf-8') as data_file:
                    data = json.loads(data_file.read())
                    self._rawfacts[filename] = data




    def create_hostmap(self, dict_of_facts):

        '''Given a dictionary of hostnames -> [host facts] return a dictionary of dicts environment : {hostname : facts}'''


        pattern = re.compile(r'\'([a-zA-Z0-9]+)-env\'')

        for host, host_facts in dict_of_facts.items():
            env = re.search(pattern, host_facts['roles']).group(1)
            if env not in self._facts:
                self._facts[env]={}
            self._facts[env].update({str(host_facts['ansible_hostname']).upper():host_facts})








    def get_environment_facts(self, environment):

        ret_value = None

        if environment in self._facts:
            ret_value = self._facts[environment]
        else:
            raise AnsibleException('Could not get facts for env ' + environment)

    def get_environment_names(self):

        return sorted(self._facts.keys())




        return ret_value

    def get_all_packages(self):

        return sorted(list(self._installed_packages))

    def return_table_data(self, environment):

        table = []
        header_row = [''] + sorted(list(self._installed_packages))
        table.append(header_row)

        for host in sorted(self._facts[environment].keys()):
            host_packages = self._facts[environment][host]['savvi_versions'].keys()
            host_row = [host]
            for pkg in sorted(list(self._installed_packages)):

                if pkg in host_packages:
                    host_row.append(self._facts[environment][host]['savvi_versions'][pkg])
                else:
                    host_row.append('-')

            table.append(host_row)

        return table





class AnsibleHost:
    '''Class to hold ansible facts about a host'''

    def __init__(self, hostfacts):

        extract_env_pattern = re.compile(r'\'([a-zA-Z0-9]+)-env\'')

        self.facts = hostfacts
        self.hostname = hostfacts['ansible_hostname']
        self.environment = re.search(extract_env_pattern, hostfacts['roles']).group(1)
        self.roles = hostfacts['roles']
        self.platform_packages = hostfacts['savvi_versions']

        return


class AnsibleException(Exception):

    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(AnsibleException, self).__init__(message)

        #self.errors = errors
