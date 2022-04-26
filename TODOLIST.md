>更新日志
>20190823

test

----
# <为了学习>后端结构方案
抓包软件 stream

# bug
抢座函数：当学校/自习室不存在时，就提示不存在并提示添加指令；（现在是 不存在则马上自动去爬取一遍自习室信息）
>
    * ok 自习室开放一个不开放一个，导致的爬取座位表解析异常
    * ok school_abbr 大小写未转换统一
    * ok #sessionid srverid位置不同导致的失效误判问题
    * ok #sessionid serverid 位置交换，漏写重新复制给content的语句

* 自习室开放时间段才能 添加学校
* 返回"指令格式不正确"  qz；hbucm；20127；69；20127；69；sessionid; serverid 

    
* ok #抢座候选座位只有一个的时候 【候选座位只有一个引发的指令解析异常】
* ok  #1, sduwh，当前状态为订座成功，有'退订按钮'，此时添加学校导致解析异常
在 已经预约的状态下 无法添加学校
* ok  #2  指令前缀 中文的#号导致解析异常
* ok  #3, 抢座任务座位号前导 0 导致的问题
* ok  wechatSESS_ID在最末尾，且没有分号空格时导致的解析异常
> ```...wechatSESS_ID=0e9504ef6929d52c9676d0c3c11fdf434d978dc6ec66d869'''```

* 

重大bug
20190822 task_id=11875 
> #抢座;  ecut;    1141;   7;  1141;   8;  wechatSESS_ID=ce17f323a3c0dc54f976bb0d26a8ecd47930c0ba729c3680; Hm_lpvt_7ecd21a13263a714793f376c18038a87=1566481408; SERVERID=d3936289adfff6c3874a2579058ac651|1566481444|1566481377
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20190823164938939.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1JlbmppYUx1OTUyNw==,size_16,color_FFFFFF,t_70)
这样的任务也能添加成功
# todolist
- [ ] 0，抢座任务，时间自己输入 
- [ ] 1，添加特定关键字反馈
- [ ] 2，添加任务执行完毕的状态信息-数据库
- [ ] 3，测试极速版执行 
> 使用首页的hexcodeurl- failed, 
> 明日预约的任务，使用 今日预约的开放的自习室的 hexcodeurl - failed
> ```![在这里插入图片描述](https://img-blog.csdnimg.cn/20190824201133332.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1JlbmppYUx1OTUyNw==,size_16,color_FFFFFF,t_70)
- [x] 4，解决【刚刚把抓的包发给了我去图书馆，有点慌。】
- [ ] 5，两个座位被抢，则抢一个随机的空座位 
- [ ] 6，座位冲突的问题
- [ ] 7，连续多天失败的奖励机制
- [ ] 8，随机头headers
- [ ] 9，尝试 pyv8执行js
- [ ] 10，添加指令 查询指令 关键字回复
- [ ] 11，抢座结果增加昨天前天的字样
- [ ] 12，使用 emoji 增强文本表达
- [ ] 13，开抢前5-30分钟 提交任务才有效哦 的提示加到 抢座函数的反馈信息里
- [ ] 14，保证 数据库中的 sessionid serverid 分别含有 **wechatSESS_ID=** 和 **SERVERID=**
- [ ] 15，**协程**
- [ ] 16，统一 sessionid 的名称为 wechat_sess_id
- [ ] 17，隐藏抢座人数，不能直接从taskid上看出来
- [ ] 18，进入座位表页面失败-可能的原因
- [x] 19，捡漏指令的读入7
- [x] 20，抢座指令支持 0 和负数                                 



----
# 尝试
failed 首页的script url 已经被取消     

1，使用图书馆首页的  hexcodejs得到的hexcode能否完成抢座

2，准时开抢任务失败后，转为 捡漏任务，要区分pre 和 today

ok 尝试失败， 3，带cookies 请求hexcodeurl，然后抢座
在实际上线运行中会出现"【该座位不存在!清尝试刷新页面】"的提示，就是人与程序的操作冲突，人的操作刷新了 hexcodejs，
而程序却还保留着过期的 hexcodejs，导致得到的 hexcode 不正确；

4，使用协程替换线程，提高抢座函数的资源占用
5，或者使用c++重写抢座函数
6，尝试开抢时间提前几秒

> 实时捡漏  要区分pre 和 today

自习室关闭了怎么办

# 捡漏、抢座指令设计
>
>#抢座|#捡漏；
>libid1，seatnum1，libid2，seatnum2，libid3，seatnum3；
> sessionid；serverid；
> starttime；pre_or_today; _保留字段_

## 考虑
~~可以设置 预约-捡漏，也可以明日预约-捡漏，捡漏指令可以指定pre_or_today
默认 19:00 之前，捡漏指令 为 today，19:01之后，捡漏指令为pre~~

只考虑当日实时预定的捡漏，不支持明日预约的捡漏；

抢座、捡漏指令：用户可指定一个开抢时间；

捡漏任务，每次尝试，只更新  memcache；没有update操作
只有在满足结束条件后，才向 任务结果表 插入 一条数据，并同时删除 今日任务表中的这条记录；



## 基础规则
~~0，正常的抢座任务失败后，休眠一段时间转为 **捡漏任务**~~
0，只有白天能使用捡漏指令，只接受当日即时预订的实时捡漏预定，06：00-21：00 有效



1，与 mainloop 同属于一个线程

2，白天05：00 - 23：00 循环读取数据库中的捡漏任务；

3，休眠间隔 [60, 80, 100, 120, 140, 160, 180] 单位秒 ，每次启动顺序执行；

4，不开启线程，使用协程，顺序执行捡漏任务，执行完则休眠2-4分钟；

5，启动前，需判断接下来1分钟是否有正常的任务，有则休眠，跳过开抢时间；
每条捡漏任务 只能保持 1 小时的时间有效期，30次的尝试

6，捡漏任务提交成功后不会立即执行，只能等待 捡漏线程 按预定规则读取；这样避免出现频繁访问的问题，也简化了捡漏函数代码

7，捡漏任务执行完成了如何标记完成，保证下次获取数据库中的今日任务，不会包含已经执行完毕的 捡漏任务
>解决方案：
>1，每执行完一条捡漏任务，就删除一条
>2，使用update，增加任务状态 字段 task_status表示任务是否有效，执行完一条捡漏任务就去更新 今日任务表中的数据

## 执行流程
1，开始；

2，接下来的 前后 ttt= 60 s 没有任务，若之前 ttt 时间内有正常的抢座任务，休眠 ttt 启动；若之后的 ttt 时间内有任务，则休眠  ttt + ttt 时间再启动

则读取数据库**今日任务表**中的捡漏任务，无，则休眠，

3，有捡漏任务，读取，读取时按每个用户分组，取最新提交的任务；

4，将捡漏任务列表按**学校**分组，获取这些学校的座位表

5，随机取一个学校，任务不分组  ~~按自习室随机和不随机分为三组：全随机，候选二随机，全指定~~
            ~~先定义 空闲座位表dct~~ 由于存在延时，所以不使用 全局的空闲座位表；更大的原因是因为，抢座需要 hexcode，必须通过进入座位表获得

6，改为每个任务都进入自习室座位表

7，遍历这个学校的捡漏任务，使用协程，构造执行任务列表 

8，限定了**自习室id**的则直接填入，没有指定的则随机先填充自习室id；
> 对于每一条捡漏任务，先获取 有哪些学校，去查询对应学校有哪些自习室，得到(id, name)
> 然后，对 设置了随机自习室的任务进行 **自习室随机不重复**  填充，
> 填充到不多于三个自习室（后续可能会增加候选自习室数量，注意代码的可扩展性），
> 填充时，去掉指令中标明的不需要的自习室
> 座位号先不管
> 然后
> 一个任务最多三个自习室
> 

9，**座位号**不管指定不指定，都得先进座位表页面获取空位，再判断空位是否是限定的那个**座位号**，若不是则记录这条任务本次执行的情况；若存在空位，且没有限定**座位号**，则随机选一个提交

10，实现 **寻找空位函数**，指定图书馆id，返回一个空位坐标，若没有空位返回 ```NOT_FOUND```
```
def search_empty_position(libid, serverid, sessionid):
	'''
	'''
	return seat_coordinate
	
```

11，当**自习室id**未指定时，为了避免产生验证码，每任务只有 3 个libid_coordinate，即调用三次 **寻找空位函数**





启动前检查，
1，避开 其他学校的开抢时间；
2，随机时间间隔 50s - 120s 执行；
3，
捡漏指令：#捡漏，学校英文简称，自习室1，座位号1，自习室2，座位号2，serverid，sessionid
其中，自习室id为空或-1，则为随机选择自习室进行抢座；不为空则优先选择；全部不为空，则限定了这两个位置

支持不想要的座位：使用负数表示

### 指令格式
==***实时预定 | 捡漏 | jl | #jl***   ；   ***学校英文简称***；***自习室id1***；***座位号***；***自习室id2***，***座位号***；
***serverid***；***sessionid***==

#### 解释：
自习室id 和 座位号 如果为 **0**，则表示 可以任意选择一个；

自习室id 和 座位号 如果为 **某个正确的自习室id或座位号**，则表示 限定了某个自习室或者座位号；

自习室id 和 座位号 如果为 **某个正确的自习室id或座位号**的**相反数**(前面加个负号)，则表示不能选这个自习室或者这个座位号；

#### 举例:
 * 捡漏，pku，1230，80，1231，81，serverid，sessionid
> **注意：自习室座位号明确了的话，那么任务执行只会尝试预订这两个位置**
>  表示 学校 pku 的捡漏任务，限定了只在1230和1231这两个自习室里面选，
>  而且对于这两个自习室，只会去尝试预定 1230的80号 或者 1231的81号座位；
>  执行实施预定任务时，如果这两个位置都不是空闲状态的话，则不尝试抢其他位置。

* #jl，pku，1230，80，1231，0，serverid，sessionid 
> **注意：0表示随机选择**
> 表示 学校 pku 的捡漏任务，限定了只在1230和1231这两个自习室里面选；
> 其中1230自习室还限定了 座位号：1230的80号座位；1231自习室没有限定座位号，则会随机选择1230中的一个空位
> 执行实施预定任务时，如果1230自习室80号座位没有成功，则会进入1231自习室，随机预定一个空闲的座位

* 实时预定，pku，1230，80， 0， 0，serverid，sessionid  
> 注意： **0 表示随机选择**
> 表示 学校 pku 的捡漏任务，限定优先在1230 自习室里面选，若不成功则去其他任意一个自习室找一个空位进行预定；
> 其中1230自习室还限定了 座位号：1230的80号座位，优先进行1230的80号座位的预定，不成功则随即进入其他自习室寻找空位，再次进行预定

* 实时预定，pku，-1230，0， 1231， -81，serverid，sessionid
> **注意：负数表示不选择这个自习室，或者这个座位号**
> 表示 学校 pku 的捡漏任务，限定**不能**在1230 自习室里面选空位，只能在1231自习室选空位，且，在1231自习室里面不能选 81号。

* jl，pku，0，0， 0， 0，serverid，sessionid 
>
> 表示没有任何限定，可以选择任意自习室的任意座位进行预定

....可以有很多组合

总而言之，自习室id为 0 ，则随机选择空位，座位号为0则，随机选择座位号；为负数，则排除对应的自习室或者座位号；
按顺序先尝试候选1然后再尝试候选2





4，捡漏线程的结束标志：

5，捡漏线程可能遇到的情况
    1，成功，抢座成功，更新memcache，结束；
    2，成功，你已经预定了其他座位，结束
    3，失败，sessionid失效，更新memcache，结束；
    4，失败，进入自习室连接超时，不结束，待会继续重试
    5，失败，与人的操作冲突导致的座位表不存在，不结束，待会继续重试
    6，失败，需要验证码
    7，失败，自习室不开放


6，一个捡漏任务一个线程，一旦启动无法停止，有效时间，半小时-两小时不等


7，太过频繁容易引发验证码

每执行一次记录一次结果保存memcache



#  抢座失败

* 【该座位不存在】：解析执行hexcode 得到了unicode字符 Zm67ÆYF | xdrbtN8M¥eJpm |

hexch_js_url= https://static.wechat.v2.traceint.com/template/theme2/cache/layout/28jhHRbfHQBjsecd.js
thread_name=ecut_11871 http_hexch_seatinfo= https://wechat.v2.traceint.com/index.php/prereserve/save/libid=1144&xdrbtN8M¥eJpm=19,15&yzm=
xdrbtN8M¥eJpm

* 【选座中,请稍后】:

* 【参数不正确】：可能是由于 和手抢冲突，导致脚本这边的 hex失效
thread_name=ycit_11900 hexch_js_url= https://static.wechat.v2.traceint.com/template/theme2/cache/layout/PY3cN4imk5EQThnF.js
thread_name=ycit_11900 http_hexch_seatinfo= https://wechat.v2.traceint.com/index.php/reserve/get/libid=1234&XSCF37jDYdz=21,8&yzm=

* 【参数不正确】：使用今日预约的 hexcodeurl 获取hexcode 进行明日预约任务，返回参数不正确

* 【该座位不存在】:参数肉眼检查正常，
school:bjtu
taskid:11990
任务提交:2019.08.24_19:53:40.414
候选一:[第一自习室A区 (5楼)]的[78]号座位:
执行:2019.08.24_20:10:00.086
结果:FAILED-【该座位不存在】

* 【黑名单用户无法预定座位】
----#2019.08.25_22:00:06.095|[run]ecut_12086 delaytime= 13
----#2019.08.25_22:00:06.096|[run]ecut_12123 😱 😱很抱歉，抢座失败😱 😱 thread_name= ecut_12123 status= False task_result=
 😱 😱很抱歉，抢座失败😱 😱
school:ecut
taskid:12123
任务提交:2019.08.25_21:54:33.548

候选一:[环境科学阅览室（C0805） (8楼)]的[46]号座位:
执行:2019.08.25_22:00:00.056
结果:FAILED-【黑名单用户无法预定座位】

候选二:[环境科学阅览室（C0805） (8楼)]的[47]号座位:
执行:2019.08.25_22:00:04.511
结果:FAILED-【黑名单用户无法预定座位】

----

# 架构
## memcache的设计
**正常用户可用**
正常的抢座结果，key=userid_reserve， value=
实时抢座|捡漏的结果，key=userid_realtime，value={} json 需要精简，内容不宜过多
> 实时抢座|捡漏的结果 value: {'try_cnt': 10, 'cant_entry_seatpage_cnt':1,'try_record': '10:00:00 []的[]座位[]'}
用户的积分 ？ 
**管理员可用：**
每天的任务统计信息，key=admin_stats，value=今日任务数量，提交了任务的用户userid，当前正在执行的捡漏任务

## mainloop
0，
> 捡漏任务必须保证在30s内执行完成，极限情况参考 action_duration=silence_window + 1s的情况，
> > silence_window = 100 * 1000 ，这是最后留出的空闲时间，
> > 	action_duration=silence_window+1s  > silence_window，则启动一次捡漏线程，此时如果有正常的抢座任务，
> > 那么应该在 50s处开抢，所以为了不影响正常抢座任务， 捡漏线程必须得在30s内执行完成
> 
> 
> 捡漏任务是一个独立的线程，有任务时启动，使用顺序执行完毕后注销
> 正常抢座任务 前10s后90s   共100s 内为禁区，如果剩余操作时间  action_duration  小于  
> silence_window，则放弃捡漏任务的执行，进入下一次大的循环
> 
> 
```python
        # real_time task, time unit is millisecond
        now_time = now_time = int(time.time()*1000)
        # a time window , no task running, wait for next loop sleep
        silence_window = 100 * 1000
        action_duration = next_awaken - now_time - silence_window
        while action_duration > 0:
            # start real_time thread
            
            delay_time = random.choice(range(60,min(action_duration//1000, 120),10))
            if action_duration - delay_time*1000 > 0:
                action_duration -= delay_time * 1000
                time.sleep(delay_time)
            else:
                # no action_duration time
                break
```

1，使用滑动窗口，窗口长度为5分钟 300s
2，每次awake，先判断接下来的 一个时间窗口 内，是否有正常的抢座任务，若有，
> 若有正常的抢座任务， 先启动正常的抢座任务，在判断是否执行 捡漏函数
> 
> 如果有多个学校在这个时间窗口的话，获取抢座任务的最早和最晚 开抢时间，
> 得到 [最早开抢时间-60s, 最晚开抢时间+60s] 区间，如果当前时间 在区间之外，则启动一次捡漏任务执行函数；如果当前时间在区间之内，则不执行捡漏函数；
> 

则先处理正常的抢座任务，将其一个一个启动线程，然后进入下一步； 若没有则直接进入下一步
3，对于此次awake，判断完正常的抢座任务后，开始处理 捡漏任务，
4，先获取刚才启动的正常抢座任务的开抢时间，得到 跳过区间 [open_time-60s, open_time+60s]
捡漏任务的执行必须保证在下一次 awake时间之前 60 s；

## 表：今日任务表、历史命令表、自习室信息表、任务结果表、~~历史任务结果表~~

其中 
>~~* 0，今日任务表分为 抢座任务表 和 捡漏任务表~~
> 其中，抢座任务表   userid 为 unique， 捡漏任务表 wechat_sess_id为 unique
> 两个表都设置了 备份到历史任务表的 触发器
> 


* 0，共四个表，今日任务  任务结果    历史命令  自习室信息表
> 今日任务表，储存抢座任务与捡漏任务，创建联合索引 ( task_kind, userid)
> 每个用户每种任务只能保留一条，即使用replace关键字进行任务插入
>  任务执行的结果立即 保存到**任务结果表**，只保存有结果的任务

* 1，**今日任务表** 储存**抢座和捡漏指令**，并使用触发器自动备份每一条命令到  **历史指令表**
* 2，**今日任务表** 和  **历史指令表** 增加字段 

>  int : pre_or_today (抢今天的还是明天的)
>  text: open_time 开抢时间
>  int : task_kind 任务类型(捡漏或抢座);      
>   int:  succ_failed 任务结果；    
>   detail_info 详细的每次尝试 的 服务器返回信息
>  1个 str 型 保留字段 others_info


* 3，**任务结果表** tb_task_result  储存  抢座和捡漏的任务执行结果
 >id,  int
> userid, text
> task_kind  int 任务类型 
> wechat_sess_id,  text   id验证信息
> submit_time  int 提交时间20190822215000
> succ_failed, int 成功失败
> detail_info, text 详细的服务器返回信息
> 1个 str 型 保留字段 others_result_info
>


> ~~4，**任务结果表** 每天凌晨的停机时间，自动去和  **今日任务表**~~
> join，全连接操作（理论上应该以今日任务表为主，右连接）；join的key 为
> > userid
> > task_kind 任务类型
> > wechat_sess_id
> > 
> > 注意：
> > 一个用户 的 抢座任务可能随时会更新覆盖，taskid 和数据库中的id会增加，抢座任务只有一条；
> > 一个用户 的 捡漏任务肯能被覆盖，也可能一天提交多次；捡漏任务可以存在多条；其中，覆盖的标准是按照  sessionid 和 serverid 是否相同；不同则不覆盖
> >

5，任务结果表 join 今日任务表后，储存到历史指令表或者一个新表

6，抢座任务或捡漏任务完成后，立即构造一条记录，储存到 **任务结果表**中，等待凌晨的join的操作，同时将结果暂存 memcache，方便用户查询；

7，**历史任务结果表**保存 今日任务表 与 任务结果表 join的结果



----

## 可能出现的场景
1，某用户的抢座任务，22：00执行完成，已经将结果写入 任务结果表，但此时如果用户再次提交抢座任务，将会update 已经执行完成的任务；如果wechat_sess_id不一样，那么就会导致凌晨 join的操作可能出现对不上号的情况。
（这种情况不处理，制作说明提醒用户 不要在 当日开抢完成后，再次添加抢座任务，这会使其积分失效）

2，ecut 22：00开抢，
一名ecut的同学，白天想实时抢座，使用**捡漏指令**，添加了任务，任务按照预先设计的逻辑执行，每尝试一次，都更新一次memcache


----

# 下一次更新的内容
1，查询指令，添加指令。。。的关键字回复
2，向客服反馈的聊天截图
3，sessionid 是需要你们自己获取的，不是示例的 也不是这个单词
4，抓包会有 风险提示
5，请在开抢前5-30
6，解释各种失败的情况
7，结果指令需要一点时间延迟
8，抢座时间不对、自习室缺少、抢座返回【参数错误】请联系以下管理员添加信息
9，修改 各个指令 详情的标题为【查询指令 添加指令 最后添加任务等
10，问我不收费，这么做的原因，个人爱好




## database
```python
creat_tb_cmd = '''
        CREATE TABLE IF NOT EXISTS schl_lib_stmp(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                schl_abbr TEXT NOT NULL ,
                schl_nm TEXT  NOT NULL ,
                open_time TEXT,
                libid INTEGER NOT NULL UNIQUE ,
                clssrm_nm TEXT NOT NULL ,
                seatmap_json TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS task_history(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            userid TEXT NOT NULL      UNIQUE, 
            task_kind INTEGER    NOT NULL,
            wechat_sess_id TEXT ,
            
            succ_failed INTEGER ,
            return_info TEXT,
            others_result_info TEXT,
            
            taskid INTEGER NOT NULL, 
            user_name TEXT, 
            school_name TEXT,
            schl_abbr TEXT,
            classroom_name1 TEXT, 
            libid1 INTEGER, 
            seat_num1 INTEGER,
            coordinate1 TEXT,
            classroom_name2 TEXT, 
            libid2 INTEGER, 
            seat_num2 INTEGER, 
            coordinate2 TEXT,
            serverid TEXT, 
            comment_info TEXT,
            timestamp INTEGER,
            pre_or_today INTEGER,
            others_info TEXT
        );
        
        CREATE TABLE IF NOT EXISTS task_result(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                userid TEXT NOT NULL      UNIQUE, 
                task_kind INTEGER    NOT NULL,
                succ_failed INTEGER ,
                wechat_sess_id TEXT ,
                return_info TEXT,
                others_result_info TEXT
        );
        
        CREATE TABLE IF NOT EXISTS today_task(
                 id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                 task_kind INTEGER  NOT NULL,
                 taskid INTEGER NOT NULL     UNIQUE, 
                 userid TEXT NOT NULL      UNIQUE, 
                 user_name TEXT, 
                 school_name TEXT,
                 schl_abbr TEXT,
                 classroom_name1 TEXT, 
                 libid1 INTEGER, 
                 seat_num1 INTEGER,
                 coordinate1 TEXT,
                 classroom_name2 TEXT, 
                 libid2 INTEGER, 
                 seat_num2 INTEGER, 
                 coordinate2 TEXT,
                 serverid TEXT, 
                 sessionid TEXT, 
                 comment_info TEXT,
                 timestamp INTEGER,
                 succ_failed INTEGER,
                 pre_or_today INTEGER,
                 others_info TEXT
        );
          
        CREATE TABLE IF NOT EXISTS origin_cmd_log(
                 id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                 task_kind INTEGER  NOT NULL,
                 taskid INTEGER NOT NULL   , 
                 userid TEXT NOT NULL    , 
                 user_name TEXT, 
                 school_name TEXT,
                 schl_abbr TEXT,
                 classroom_name1 TEXT, 
                 libid1 INTEGER, 
                 seat_num1 INTEGER,
                 coordinate1 TEXT,
                 classroom_name2 TEXT, 
                 libid2 INTEGER, 
                 seat_num2 INTEGER, 
                 coordinate2 TEXT,
                 serverid TEXT, 
                 sessionid TEXT, 
                 comment_info TEXT,
                 timestamp INTEGER,
                 succ_failed INTEGER,
                 pre_or_today INTEGER,
                 others_info TEXT
        );
        
        CREATE TRIGGER cmd_backup AFTER INSERT ON today_task 
        FOR EACH ROW 
        BEGIN 
            INSERT INTO origin_cmd_log (task_kind, taskid, userid, user_name, school_name, schl_abbr, classroom_name1, libid1, seat_num1, coordinate1, classroom_name2, libid2, seat_num2, coordinate2, serverid, sessionid, comment_info, timestamp, succ_failed, pre_or_today, others_info) 
            VALUES(new.task_kind, new.taskid, new.userid, new.user_name, new.school_name, new.schl_abbr, new.classroom_name1, new.libid1, new.seat_num1, new.coordinate1, new.classroom_name2, new.libid2, new.seat_num2, new.coordinate2, new.serverid, new.sessionid, new.comment_info, new.timestamp, new.succ_failed, new.pre_or_today, new.others_info);
        END;
        '''
```


