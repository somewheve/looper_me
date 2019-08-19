# looper_me
ctpbee 使用的数据服务器

> 获取准确数据的解决方案


## 目标

1, 载入符合ctpbee标准数据格式的历史数据
2, 符合同时能够接收ctpbee推送的tick数据,并在端口提供转发 

> 感谢[yutiansut](https://github.com/yutiansut) 的idea ~~

设计架构 

![structure](https://github.com/somewheve/looper_me/blob/master/architecture.png)             


## 开始之前 

-  serve_config.ini 文件记录了服务器启动的端口, 当发现端口被占用的时候请更换 
值得注意的是http端口需要和admin/src/main.js 下面的
`const URL = 'http://127.0.0.1:8888'  `端口保持一致

- 安装依赖
  ```
  pip install -r requirement.txt
  如jwt报错 请手动:pip install PyJWT
  ```
## 启动服务端
`python serve.py `

#### 启动前端 
```
cd admin
npm install
npm run dev
```

#### 启动客户端 --> tick行情推送端
`python client.py `


#### 一些注意事项 
请记住每个ip下面只能运行一个tick发送器 , 这样是为了确保在不同的ip下采样的效果会达到最佳取样

如果你要实现单台机子上面实现多个发送的源, 请自行修改代码. 代码不多 , 随便看下就好了 ..
