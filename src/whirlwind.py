#            _     _      _          _           _ 
#           | |   (_)    | |        (_)         | |
#  __      __ |__  _ _ __| |_      ___ _ __   __| |
#  \ \ /\ / / '_ \| | '__| \ \ /\ / / | '_ \ / _` |
#   \ V  V /| | | | | |  | |\ V  V /| | | | | (_| |
#    \_/\_/ |_| |_|_|_|  |_| \_/\_/ |_|_| |_|\__,_|

import os
from ip_address_changer import IpAddressChanger

def lambda_handler(event, context):
    print("lambda_handler called")
    
    instance_id = os.getenv('INSTANCE_ID')
    hosted_zone_id = os.getenv('HOSTED_ZONE_ID')
    sns_topic = os.getenv('SNS_TOPIC')

    ip_address_changer = IpAddressChanger(instance_id, hosted_zone_id, sns_topic)
    ip_address_changer.execute()
    
    print("lambda_handler executed")
    return
