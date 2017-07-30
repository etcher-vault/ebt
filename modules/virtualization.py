__author__ = 'larrabee'
import sys
import os
import libvirt
from xml.etree import ElementTree as ET

class Libvirt():
    def __init__(self, uri='qemu:///system'):
        self.conn = libvirt.open(uri)
        self.include = list()
        self.exclude = list()

    def list_domains(self):
        return self.conn.listAllDomains()

    def get_domain_disks(self, domain):
        assert isinstance(domain, libvirt.virDomain), '{1}.{2}: variable "{0}" has wrong type.'\
            .format('domain', __name__, sys._getframe().f_code.co_name)
        domain_xml = domain.XMLDesc(0)
        root = ET.fromstring(domain_xml)
        disks = root.findall('./devices/disk')
        disks_list = list()
        for disk in disks:
            disk_info = {}
            if disk.attrib['device'] in ('disk',):
                if (disk.find('source') is not None) and (disk.find('source').get('dev') is not None):
                    disk_info['path'] = disk.find('source').get('dev')
                    disk_info['target'] = disk.find('target').get('dev')
                    disk_info['source_type'] = 'dev'
                    disk_info['snapshot_path'] = None
                    disks_list.append(disk_info)
                elif (disk.find('source') is not None) and (disk.find('source').get('file') is not None):
                    disk_info['path'] = disk.find('source').get('file')
                    disk_info['target'] = disk.find('target').get('dev')
                    disk_info['source_type'] = 'file'
                    disk_info['snapshot_path'] = None
                    disks_list.append(disk_info)
        return disks_list

    def filter_domain_list(self, domains):
        assert isinstance(self.include, list), '{1}.{2}: variable "{0}" has wrong type.' \
            .format('include', __name__, sys._getframe().f_code.co_name)
        assert isinstance(self.exclude, list), '{1}.{2}: variable "{0}" has wrong type.' \
            .format('exclude', __name__, sys._getframe().f_code.co_name)
        assert isinstance(domains, list) and isinstance(domains[0], libvirt.virDomain), '{1}.{2}: variable "{0}" has wrong type.' \
            .format('domains', __name__, sys._getframe().f_code.co_name)
        filtered_list = list()
        for domain in domains:
            if (domain.name() in self.include) or (('all' not in self.exclude) and (domain.name() not in self.exclude)):
                filtered_list.append(domain)
        return filtered_list

    def export_xml(self, domain, path):
        domain_xml = domain.XMLDesc(0)
        xml_file = open(path, mode='w')
        xml_file.write(domain_xml)
        xml_file.close()


    def restore(self, path):
        self.conn.restore(path)
    
    def create_snaapshot_xml(self, disks, memory_dump=None):
        snap_xmp =ET.
        
    def create_snaapshot_xml(self, disks, memory_dump=None):
        snap_xml = ET.Element('domainsnapshot')
        disks_xml = ET.SubElement(snap_xml, 'disks')
        if memory_dump is None:
            ET.SubElement(snap_xml, 'memory', {'snapshot': 'no'})
        else:
            ET.SubElement(snap_xml, 'memory', {'snapshot': 'external', 'file': memory_dump})
        for disk in disks:
            if disk['snapshot_path'] is None:
                ET.SubElement(disks_xml, 'disk', {'name': disk['target'], 'snapshot': 'no'})
            else:
                disk_xml = ET.SubElement(disks_xml, 'disk', {'name': disk['target']})
                ET.SubElement(disk_xml, 'source', {'file': disk['snapshot_path']})
        return snap_xml
