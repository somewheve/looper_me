# looper_me
ctpbee 使用的数据服务器

> 获取准确数据的解决方案



## 目标

1, 载入符合ctpbee标准数据格式的历史数据
2, 符合同时能够接收ctpbee推送的tick数据,并在端口提供转发 

> 推送数据应该与ctpbee的looper接口TransferProtocol协议保持一致

设计架构 

![structure](https://github.com/somewheve/looper_me/blob/master/architecture.png)             


## 开始之前 
serve_config.ini 文件记录了服务器启动的端口, 当发现端口被占用的时候请更换 
值得注意的是http端口需要和admin/src/main.js 下面的
`const URL = 'http://127.0.0.1:8888'  `端口保持一致



#### 启动服务端
`python serve.py `

#### 启动前端 
```
cd admin
npm install
npm run dev
```

#### 启动客户端 --> tick行情推送端
`python client.py `