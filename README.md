
# igotolibrary-抢座助手
![language](https://img.shields.io/badge/language-python3.x-green.svg) 
![license](https://img.shields.io/badge/LICENSE-MIT-brightgreen.svg)

------

## 声明
**我去图书馆** 对爬虫的防护较弱且更新不及时, 网络上已经开始流传**收费**的抢座助手; 这些对正常抢座的普通同学不公平; 
1. ``` igotolibrary ```  无意侵犯任务组织或个人的权益, 仅作学习交流; 
2. ``` igotolibrary ```  已经三次向 **我去图书馆** 反馈了抢座漏洞的问题, 但没有得到积极的反馈和有效的响应, [反馈截图](https://github.com/qmppz/igotolibrary/blob/master/fankui_screenshot.jpeg);
3. ``` igotolibrary ``` 开源, 供大家公平使用; 欢迎有兴趣的同学一起维护更新, 直到修复漏洞为止;
4. 希望大家不要二次开发后用来提供收费服务.

------

## 简介
一个简单的 *Python* 爬虫，通过 *Charles* 抓包分析公众号《**我去图书馆**》、《**来选座**》的服务通信协议，获取自习室和座位表信息，使用```Python```+```requests```库模拟预定座位的流程，实现定时预订/实时捡漏自动抢座。

------

## 抓包过程分析
* [[igtl-again]我去图书馆-抢座主逻辑详解](https://blog.csdn.net/RenjiaLu9527/article/details/96843605)
* [[igtl-again]我去图书馆-抢座主逻辑详解](https://zhuanlan.zhihu.com/p/74706139)

------

## 项目结构
分为两个部分 
* mainloop 抢座任务执行部分
* mhandle_content 指令解析验证储存部分

如图:

> ![igtl_again](https://github.com/qmppz/igotolibrary/blob/master/igtl-again.png)

> * 有疑问可提交 **Issues**
> * 有修改可提交到 **dev** 分支后 **Pull requests** 

------

## 接下来可改进的地方 TODOLIST
1. 一些细节: [TODOLIST.md](https://github.com/qmppz/igotolibrary/blob/master/TODOLIST.md);
2. ```reserve.py``` 模块弃用线程, 改用协程, 节约资源, 增大并发任务量;
3. 尝试换成 ```pyv8```库执行js; 加快 ```hex_code``` 字段的计算;
4. 开发一个极速版 ```personal_reserve```, 去掉冗余的参数信息只保留核心的步骤, 最大可能的加速抢座;
5. ...(待补充)

------

## 部署demo
我已将工程部署到了微信 《**为了学习**》公众号，欢迎测试，服务启动中...

> ![weilexuexi_gzh](https://github.com/RenjiaLu9527/igotolibrary/blob/master/qrcode.png)

------

## 致谢
* [IPProxyPool](https://github.com/qiyeboy/IPProxyPool)
* [memcached](https://github.com/memcached/memcached)

> # 有问题可留言 或 联系公众号管理员

## AppreciationCode
> ![AppreciationCode.png](https://github.com/RenjiaLu9527/igotolibrary/blob/master/AppreciationCode.png)


