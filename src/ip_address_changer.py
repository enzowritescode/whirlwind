import boto3

class IpAddressChanger:
    def __init__(self, instance_id, hosted_zone_id, sns_topic):
        # args
        self.instance_id = instance_id
        self.hosted_zone_id = hosted_zone_id
        self.sns_topic = sns_topic

        # AWS SDK setup
        self.route53 = boto3.client('route53')
        self.ec2 = boto3.client('ec2')
        self.sns = boto3.client('sns')

        return

    def _fetch_current_ip_allocation_id(self):
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(self.instance_id)
        public_ip = instance.public_ip_address

        desc = self.ec2.describe_addresses(PublicIps=[public_ip])
        return desc['Addresses'][0]

    def _find_dns_record(self, old_ip_address):
        record_sets = self.route53.list_resource_record_sets(HostedZoneId=self.hosted_zone_id)

        resource_record_sets = record_sets['ResourceRecordSets']

        for resource_record_set in resource_record_sets:
            record_type = resource_record_set['Type']

            # skip over non 'A' records
            if record_type != 'A':
                continue

            resource_records = resource_record_set['ResourceRecords']

            for resource_record in resource_records:
                if resource_record['Value'] == old_ip_address:
                    return resource_record_set

        return None
                        
    def _change_dns_record(self, resource_record_set, old_ip_address, new_ip_address):
        resource_records = resource_record_set['ResourceRecords']

        for resource_record in resource_records:
            if resource_record['Value'] == old_ip_address:
                resource_record['Value'] = new_ip_address
                
                self.route53.change_resource_record_sets(
                    HostedZoneId=self.hosted_zone_id,
                    ChangeBatch={
                        'Changes': [
                            {
                                'Action': 'UPSERT',
                                'ResourceRecordSet': resource_record_set
                            }
                        ]
                    }
                )

                return True

        return False

    def execute(self):
        # get current IP address and find matching DNS record
        old_ip_adrr_info = self._fetch_current_ip_allocation_id()
        old_ip_address = old_ip_adrr_info['PublicIp']
        resource_record_set = self._find_dns_record(old_ip_address)

        # uh oh...
        if resource_record_set is None:
            print('Failed to find DNS record')
            self.sns.publish(
                TopicArn=self.sns_topic, 
                Message='Failed to find DNS record', 
                Subject='VPN IP Address Rotate Failed')

            return

        # allocate new IP address
        new_ip_addr_info = self.ec2.allocate_address(Domain='vpc')

        # associate/dissociate
        new_ip_allocation_id = new_ip_addr_info['AllocationId']
        old_ip_allocation_id = old_ip_adrr_info['AllocationId']

        self.ec2.associate_address(
            AllocationId=new_ip_allocation_id,
            InstanceId=self.instance_id)

        self.ec2.release_address(AllocationId=old_ip_allocation_id)

        # update dns record
        new_ip_address = new_ip_addr_info['PublicIp']

        if not self._change_dns_record(resource_record_set, old_ip_address, new_ip_address):
            print('Failed to updated DNS record')
            self.sns.publish(
                TopicArn=self.sns_topic, 
                Message='Failed to update DNS record', 
                Subject='VPN IP Address Rotate Failed')

            return