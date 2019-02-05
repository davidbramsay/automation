from scapy.all import arping

#ARP tool to look up smart outlet IPs -- saves us from
#hand finding them when IPs are reassigned with DHCP

class NetworkLookup:
    mac_to_ip = {}
    addresses = ''

    def __init__(self, addresses="192.168.1.*"):

        self.addresses = addresses
        ans, unans = arping(addresses)

        for r in ans:
            mac = r[1].hwsrc
            ip = r[1].psrc
            self.mac_to_ip[mac] = ip

    def get_full_lookup_table(self):
        return self.mac_to_ip

    def lookup_mac(self, mac):
        if mac in self.mac_to_ip:
            return self.mac_to_ip[mac]
        else:
            print 'not found'
            return None


arp = NetworkLookup()

print 'looking up'
print arp.lookup_mac('84:0d:8e:49:f4:87')

print 'looking up'
print arp.lookup_mac('60:01:94:a4:7b:9e')

print 'full table'
print arp.get_full_lookup_table()


