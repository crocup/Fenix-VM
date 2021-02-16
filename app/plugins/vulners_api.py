# use api vulners.com
import vulners


class Vulnerability:

    def __init__(self, api_key):
        """

        :param api_key:
        """
        self.api_key = vulners.Vulners(api_key=api_key)

    def softwareVulnerabilities(self, name, version):
        """

        :param name:
        :param version:
        :return:
        """
        results = self.api_key.softwareVulnerabilities(name, version)
        vulnerabilities_list = [results.find_data_all(key) for key in results if key not in ['info', 'blog', 'bugbounty']]
        return vulnerabilities_list

    def publicExploits(self, name, version):
        """

        :param name:
        :param version:
        :return:
        """
        soft = "{0} {1}".format(name, version)
        return self.api_key.searchExploit(soft)
