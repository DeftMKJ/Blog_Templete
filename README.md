## How To Start 

1. `git clone xxxx` 到本地

2. `cd`到项目根目录，`virtualenv -p /usr/local/bin/python3 venv`创建Python3的虚拟环境

3. `. venv/bin/activate`激活虚拟环境 `deactivate` 退出

4. `pip install -r requirements.txt` 从requirement文件导入依赖  `pip freeze > requirements.txt` 导出到指定路径文本文件

5. `cd mkjwebsite/`进去网站项目 `python manage.py runserver` 启动本地服务即可




## admin 密码

账号：mikejing 
密码：mikejing

## Pycharm设置
> 不是用Pycharm的项目如何手动设置Python参数?

1.`.gitignore`该文件已经忽略了`venv`等资源文件，我们一般暴露一个`requirement.txt`就好

2.`Templates`文件设置，右击----Make Directory as-----Template Folder 文件夹变成紫色，同时需要在Settings.py中设置查找路径

3.`venv`文件设置，右击----Make Directory as-----Exclusion 变成橙色

4.根目录设置，右击----Make Directory as-----SourcesRoot 变成蓝色

5.模板文件提示，Pythcharm----Preference-----Language&Framework-----Python Template Languages设置成Django，这样模板文件就有了模板提示

6.代码提示，资源跳转  Pythcharm----Preference-----Language&Framework-----Django------设置参数

![](pycharm_setting.png)

## 已完成功能
- [x] 博客框架设计，虚拟环境，Pycharm配置
- [x] 博客列表和详情，博客分页，日期分类，类型分类
- [x] Bootstrap的应用
- [ ] 阅读统计，热门博客
- [ ] 富文本编辑器 md编辑
- [ ] 评论功能
- [ ] 用户登陆，第三方登陆功能
- [ ] 缓存设计
- [ ] 点赞功能
- [ ] Django Form表单的应用
- [ ] 订阅，邮箱推送
- [ ] 部署清单 Nginx + uWSGI  或者  Apache + mod_wsgi
- [ ] 静态资源搜集
- [ ] 站内消息通知
- [ ] 简单搜索
- [ ] 数据库迁移，部署Mysql
- [ ] 汉化（特别是时间，最好用timezone模块取值，通过settings进行时区校准）


## 阶段性总结
- [ ] Django整体结构和配置文件分析
- [ ] CSRF，CSS 原理分析
- [ ] Django中间件原理分析
- [ ] Django请求整个过程流转


## 免费API搜集
![](https://github.com/fangzesheng/free-api)


## ContentType
目前理解为一个中间关系Model，可以关联挂载数据到任何模型，比如Blog和统计ReamNum，ReadNum基于ContentType后再就可以关联到Blog上面

