import json
import csv

from datetime import datetime
from prettytable import PrettyTable
from sredaily import prefetch
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import AuthorizeSecurityGroupRequest
from aliyunsdkecs.request.v20140526 import DescribeElasticityAssurancesRequest
from aliyunsdkecs.request.v20140526 import RevokeSecurityGroupRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import RunInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesFullStatusRequest
from aliyunsdkecs.request.v20140526 import DescribeAvailableResourceRequest
from aliyunsdkecs.request.v20140526 import DescribeImagesRequest
from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupsRequest
from aliyunsdkecs.request.v20140526 import DescribeVpcsRequest
from aliyunsdkecs.request.v20140526 import DescribeVSwitchesRequest
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import AllocatePublicIpAddressRequest
from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupAttributeRequest

class secretinfo:
    @property
    def convert_ak(self):
        sercetfile = 'AccessKey.csv'
        csv_file = open(sercetfile)
        csv_res = csv.reader(csv_file)
        rows = [row for row in csv_res]
        aliyunak = rows[1][0]
        return aliyunak
    
    @property
    def convert_sk(self):
        sercetfile = 'AccessKey.csv'
        csv_file = open(sercetfile)
        csv_res = csv.reader(csv_file)
        rows = [row for row in csv_res]
        aliyunsk = rows[1][1]
        return aliyunsk

# 该脚本制作固定变更
class aliyunecs(secretinfo,prefetch,PrettyTable):
    def __init__(self):
        self.ak = super().convert_ak
        self.sk = super().convert_sk
        self.beauty_value_dictionary = {}
        self.securitygrouplist = []
        self.descriptions = []
        self.beauty_value_dictionary = {}

    def main(self):
        region_name = self.DescribeRegions
        print('您当前的公网ip为:',prefetch().get_external_ip)
        for key,value in region_name.items():
            print('所在区域:',key,'区域id:',value)
        self.DescribeSecurityGroups(region_value=value)
        self.DescribeSecurityGroupAttribute(region_value=value)
        self.authorizeSecurityGroupRequest(region_value=value,SecurityGroupId=self.securitygrouplist)

    @property
    def DescribeRegions(self):
        regionsclt = client.AcsClient(self.ak , self.sk)
        regionsreq = DescribeRegionsRequest.DescribeRegionsRequest()
        regionsreq.set_accept_format('json')
        regionsre = json.loads(regionsclt.do_action_with_exception(regionsreq))
        regions = {}
        city_name = 'cn-shenzhen'
        for i in regionsre['Regions']['Region']:
            if city_name == i['RegionId']:
                regions[i['LocalName']] = i['RegionId']
            else:
                pass
        return regions

    def DescribeSecurityGroups(self,region_value):
        sgidclt = client.AcsClient(self.ak , self.sk,region_id=region_value)
        sgidreq = DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
        sgidreq.set_accept_format('json')
        sgidreq.set_PageSize(50)
        sgidsre = json.loads(sgidclt.do_action_with_exception(sgidreq))
        beauty_value = PrettyTable()
        beauty_value.title = '当前实例所在区域安全组信息'
        beauty_value.field_names = ['序号','安全组名称','Vpc编号','安全组编号','创建时间']
        convert_res = sgidsre['SecurityGroups']['SecurityGroup']
        x = 0
        y = 1
        while x < len(convert_res):
            parsed_time = datetime.strptime(convert_res[x]['CreationTime'], "%Y-%m-%dT%H:%M:%SZ")
            formatted_time = parsed_time.strftime("%Y/%m/%d %H:%M:%S")
            self.beauty_value_dictionary['序号'] = str(x+y)
            self.beauty_value_dictionary['安全组名称'] = convert_res[x]['SecurityGroupName']
            self.beauty_value_dictionary['安全组编号'] = convert_res[x]['SecurityGroupId']
            self.beauty_value_dictionary['Vpc编号'] = convert_res[x]['VpcId']
            self.beauty_value_dictionary['创建时间'] =formatted_time
            self.securitygrouplist.append(convert_res[x]['SecurityGroupId'])
            beauty_value.add_row([self.beauty_value_dictionary['序号'],self.beauty_value_dictionary['安全组名称'],self.beauty_value_dictionary['Vpc编号'],self.beauty_value_dictionary['安全组编号'],self.beauty_value_dictionary['创建时间']])
            x += 1
        print(beauty_value)

    def DescribeSecurityGroupAttribute(self,region_value):
        sgattrclt = client.AcsClient(self.ak , self.sk,region_id=region_value)
        sgattrreq = DescribeSecurityGroupAttributeRequest.DescribeSecurityGroupAttributeRequest()
        sgattrreq.set_accept_format('json')
        z = 1
        beauty_value = PrettyTable()
        # beauty_value.title = '安全组白名单策略信息'
        # beauty_value.field_names = ['序号','权重','源ip地址','端口范围','创建时间']
        for x in self.securitygrouplist:
            # self.beauty_value_dictionary = {}
            sgattrreq.set_SecurityGroupId(x)
            sgatrrsre = json.loads(sgattrclt.do_action_with_exception(sgattrreq))
            vpcid = sgatrrsre['VpcId']
            sgname = sgatrrsre['SecurityGroupName']
            convert_policy_rule = sgatrrsre['Permissions']['Permission']
            print('vpc:',vpcid,'安全组名称',sgname)

            for y in range(len(convert_policy_rule)):
                # self.beauty_value_dictionary = {}
                beauty_value.title = '安全组白名单策略信息'
                beauty_value.field_names = ['权重','源ip地址','端口范围','创建时间']
                parsed_time = datetime.strptime(convert_policy_rule[y]['CreateTime'], "%Y-%m-%dT%H:%M:%SZ")
                formatted_time = parsed_time.strftime("%Y/%m/%d %H:%M:%S")
                # self.beauty_value_dictionary['序号'] = str(z+y)
                self.beauty_value_dictionary['权重'] = convert_policy_rule[y]['Priority']
                self.beauty_value_dictionary['源ip地址'] = convert_policy_rule[y]['SourceCidrIp']
                self.beauty_value_dictionary['端口范围'] = convert_policy_rule[y]['PortRange']
                self.beauty_value_dictionary['创建时间'] = formatted_time
                beauty_value.add_row([self.beauty_value_dictionary['权重'],self.beauty_value_dictionary['源ip地址'],self.beauty_value_dictionary['端口范围'],self.beauty_value_dictionary['创建时间']])
                # beauty_value.add_row([self.beauty_value_dictionary['序号'],self.beauty_value_dictionary['权重'],self.beauty_value_dictionary['源ip地址'],self.beauty_value_dictionary['端口范围'],self.beauty_value_dictionary['创建时间']])
                print('编号:',str(z+y),'权重:',convert_policy_rule[y]['Priority'],'源ip:',convert_policy_rule[y]['SourceCidrIp'],'端口范围:',convert_policy_rule[y]['PortRange'])
            print('*'*108)
        # print(beauty_value)

    def authorizeSecurityGroupRequest(self,region_value,SecurityGroupId):
        print('当前获取到您的公网Ip:',prefetch().get_external_ip)
        whiteip = ('白名单ip为',prefetch().get_external_ip)
        try:
            convert_ip = whiteip[-1]
        except Exception as e:
            print(f"{e}{'原获取ip网站发生错误'}")
        print(f"{'检测到您要添加的安全组编号为为:'}{[x for x in SecurityGroupId]}")
        whiteport = f"{'32000'}" # 这个值怎么变成一个变量可以传参数 不论如何总有一个环节是要手动执行的
        descriptions = f"{'hyf-want-jenkins-dashboard-connections'}"
        iplist = []
        portlist = []
        iplist.append(convert_ip)
        portlist.append(whiteport)
        SecurityGroupIds = SecurityGroupId[0]
        print('sg-id:',SecurityGroupIds)
        sgauthorclt = client.AcsClient(self.ak , self.sk,region_id=region_value)
        sgauthorreq = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
        for SecurityGroupIds in SecurityGroupId:
            sgauthorreq.set_accept_format('json')
            sgauthorreq.set_SecurityGroupId(SecurityGroupIds)
            sgauthorreq.set_IpProtocol('TCP')
            sgauthorreq.set_PortRange(str(portlist[0]) + '/' + str(portlist[0]))
            sgauthorreq.set_SourceCidrIp(str(iplist[0]) + '/32')
            sgauthorreq.set_Priority('10')
            sgauthorreq.set_Description(descriptions)
            sgauthorreq.set_Policy('accept')
            sgauthorreq.set_action_name('authorizeSecurityGroup')
            sgauthorsre = json.loads(sgauthorclt.do_action_with_exception(sgauthorreq))
            print(f'{sgauthorsre}{type(sgauthorsre)}')

if __name__ == '__main__':
    run_aliyun_instance = aliyunecs().main()
    # run_aliyun_instance = aliyunecs().DescribeSecurityGroups