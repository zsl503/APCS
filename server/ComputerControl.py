from typing import Optional
from alibabacloud_iot20180120.client import Client as Iot20180120Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_iot20180120 import models as iot_20180120_models


def create_client(
        access_key_id: str,
        access_key_secret: str,
) -> Iot20180120Client:
    """
    使用AK&SK初始化账号Client
    @param access_key_id:
    @param access_key_secret:
    @return: Client
    @throws Exception
    """
    config = open_api_models.Config(
        # 您的AccessKey ID,
        access_key_id=access_key_id,
        # 您的AccessKey Secret,
        access_key_secret=access_key_secret
    )
    # 访问的域名
    config.endpoint = 'iot.cn-shanghai.aliyuncs.com'
    return Iot20180120Client(config)


class ComputerControl:
    def __init__(self,
                 access_key_id: str,
                 access_key_secret: str,
                 iot_instance_id: str,
                 product_key: str,
                 device_name: str
                 ):
        self.client = create_client(access_key_id, access_key_secret)
        self.iot_instance_id = iot_instance_id
        self.product_key = product_key
        self.device_name = device_name

    def set_switch(self, switch: int) -> Optional[bool]:
        set_device_property_request = iot_20180120_models.SetDevicePropertyRequest(
            iot_instance_id=self.iot_instance_id,
            product_key=self.product_key,
            device_name=self.device_name,
            items='{"switch":' + str(switch) + '}'
        )
        # 复制代码运行请自行打印 API 的返回值
        return self.client.set_device_property(set_device_property_request).body.success

    def online(self) -> bool:
        try:
            get_device_status_request = iot_20180120_models.GetDeviceStatusRequest(
                iot_instance_id=self.iot_instance_id,
                product_key=self.product_key,
                device_name=self.device_name,
            )
            # 复制代码运行请自行打印 API 的返回值
            res = self.client.get_device_status(get_device_status_request).body.data.to_map()["Status"]
            return res == "ONLINE"
        except:
            return False
        

    def status(self) -> Optional[bool]:
        if self.online() is False:
            return None
        
        # 复制代码运行请自行打印 API 的返回值
        try:
            query_device_property_status_request = iot_20180120_models.QueryDevicePropertyStatusRequest(
                iot_instance_id=self.iot_instance_id,
                product_key=self.product_key,
                device_name=self.device_name,
            )
            res = self.client.query_device_property_status(query_device_property_status_request).body.data.list.to_map()[
                'PropertyStatusInfo']
            for i in res:
                if i['Identifier'] == 'status':
                    return i['Value'] == '1'
            return None
        except Exception as e:
            print(e)
            return None

    def reset(self):
        return self.set_switch(2)

    def open(self):
        return self.set_switch(1)

    def close(self):
        return self.set_switch(0)


if __name__ == '__main__':
    com = ComputerControl(access_key_id='xxxxx',
                          access_key_secret='xxxxx',
                          iot_instance_id='xxxxx',
                          product_key='xxxxx',
                          device_name='xxxxx', )
    print(com.online())
    print(com.status())