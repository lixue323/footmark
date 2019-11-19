from footmark.dns.dnsobject import TaggedDNSObject


class Dns(TaggedDNSObject):
    def __init__(self, connection=None):
        super(Dns, self).__init__(connection)

    def __repr__(self):
        return 'Dns:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.id
        if name == 'name':
            return self.domain_name
        if name == 'domain_remark':
            if hasattr(self, 'remark'):
                return self.remark
            return ''
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'domain_id':
            self.id = value
        if name == 'domain_name':
            self.name = value
        super(TaggedDNSObject, self).__setattr__(name, value)

    def get(self):
        return self.connection.describe_domain_info(domain_name=self.name)

    def read(self):
        dns = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region"]:
                continue

            if name == 'domain_id':
                dns['id'] = value
            dns[name] = value
        return dns

    def delete(self):
        return self.connection.delete_domain(domain_name=self.name)

    def modify_remark(self, remark=None):
        if remark and self.domain_remark != remark:
            return self.connection.update_domain_remark(domain_name=self.name, remark=remark)
        return False
