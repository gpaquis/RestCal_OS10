from pprint import pprint as pp
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = '192.168.100.129'
creds = ('admin', 'admin')

resource = '/restconf/data/ietf-interfaces:interfaces'

def disable_switchport(interface):
    """ Disables switchport for  specific interface
    Arguement:
    interface -- text form of interface (exemple: "ethernet 1/1/10")
    """
    interface_name = interface
    payload = {"ietf-interfaces:interfaces":{"interface":[{"name": interface_name, "de
ll-interface:mode":"MODE_L2DISABLED"}]}}
    _run_patch(resource, payload)


def set_ipaddress(interface, ipaddress):
    """Sets ip address of switch interface

    Arguments:
    interface -- text form of interface (example: "ethernet1/1/10")
    ipaddress -- text form of ipaddress (example: "10.0.0.1/24")
    """
    interface_name = interface
    ip2set = ipaddress
    payload = {"ietf-interfaces:interfaces":{"interface":[{"name": interface_name,"del
l-ip:ipv4":{"address":{"primary-addr": ip2set }}}]}}

    _run_patch(resource, payload)

def get_configuration(interface):
    """Shows the configuration of a switch interface

    Arguments:
    interface -- text form of interface (example: "ethernet1/1/10")
    """
    int_id = interface.replace('/', "%2F")

    interface_name = "/interface=" + int_id + "?content=config"
    url = "https://{}{}{}".format(host, resource, interface_name)

    r = requests.get(url, auth=creds, verify=False) 
    
    r.status_code == 200
    config = r.json() 
    return config


def enable_interface(interface):
    """Enable the interface on the switch

    Arguments:
    interface -- text form of interface (example: "ethernet1/1/10")
    """

    interface_name = interface
    payload = {"ietf-interfaces:interfaces":{"interface":[{"name": interface_name, "en
abled":"true"}]}}
    _run_patch(resource, payload)


def _run_patch(resource, payload):
    """Runs a HTTP PATCH call using provided resource and payload 

    Arguments:
    resource -- REST resource (example: '/restconf/data/ietf-interfaces:interfaces')
    payload -- Python Dict (example: {"ietf-interfaces:interfaces":{"interface":[{"nam
e":"ethernet1/1/10","dell-interface:mode":"MODE_L2DISABLED"}]}} )
    """

    resourcedata = resource
    payload_to_run = payload

    url = "https://{}{}".format(host, resourcedata)

    r = requests.patch(url, json=payload_to_run, auth=creds, verify=False)
    r.raise_for_status()
    return r


interface_input = "ethernet1/1/10"
ipinterface = "10.0.0.1/24"


print('==================== CONFIGURATION BEFORE MODOFICATION ==================')
myconf = get_configuration (interface_input) 
pp (myconf)
print('')

disable_switchport(interface_input)
set_ipaddress(interface_input, ipinterface)
enable_interface(interface_input)

print('==================== CONFIGURATION AFTER MODOFICATION ==================')
myconf = get_configuration (interface_input) 
pp (myconf)

