try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class CDAUtils:
    @staticmethod
    def validate_c0001(data):
        root = ET.parse(data)
        cda_id = root.find('.{urn:hl7-org:v3}id[@root="2.16.156.10011.1.1"]').get('extension')
        gmt_cda = root.find('.{urn:hl7-org:v3}effectiveTime').get('value')
        print(gmt_cda)
