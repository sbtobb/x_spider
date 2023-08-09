## 任务一
### 请爬取一下网页的内容并获取 指定内容
#### 需求 
* 获取 前10条推文信息 内容需要包括
用户名, 用户id, 用户screen name (@elonmusk) ,时间, 内容
并且生成格式

```
{"username":"Elon Musk", screen_name":"elonmusk","time":"1691382236", "full_text":"Diablo IV is a great game. Nice work by the  @Blizzard_Ent team!"}
```
* 把刚刚的数据保存到数据库中 (使用mysql)
* 使用fast api 写一个接口 把刚刚爬取的数据展示出来

##  任务二

请完成一个简单的 web 后端服务
需要包括 
* 请使用FastAPI建立一个简单的RESTful API，该API应该能够创建、读取、更新和删除数据库中的记录(MySQL)
* 请在上述API中添加用户认证。用户应该能够注册、登录，并获取一个JWT令牌。这个令牌应该在之后的所有请求中使用。只有拥有有效令牌的用户才能访问API。
* 数据验证：请利用FastAPI的Pydantic模型进行数据验证。在用户提交的数据不符合要求时，API应该返回一个清晰的错误消息。
* 完成一个接口,这个接口需要包括用户权限验证(可以尝试使用depends 验证)
* 在处理中请包含应有的错误处理
