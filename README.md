# ems（员工管理系统）

基于 **Django 5.2** 的个人学习项目，从零搭建，用于系统练习 Django 后端开发的完整业务流程：ModelForm 表单、ORM 增删改查、外键关联、搜索过滤、分页组件封装、Bootstrap 静态资源本地化。

> 本项目按照 Django 教程逐步搭建，涵盖部门管理、用户管理、靓号管理三大模块的完整 CRUD，是练习 MTV 架构与 Web 开发基本功的综合案例。

---

## 一、技术栈

| 分类 | 技术 | 用途 |
| --- | --- | --- |
| 后端框架 | Django 5.2.17 | Web 应用框架 |
| 数据库 | MySQL 8.0 | 业务数据存储，库名 `ems` |
| 数据库驱动 | PyMySQL | 通过 `install_as_MySQLdb()` 连接 MySQL |
| 前端框架 | Bootstrap 3.4.1 | 页面样式（本地静态资源） |
| 前端脚本 | jQuery 3.6.0 | JS 库（本地静态资源） |
| 日期插件 | bootstrap-datepicker | 入职时间日历选择器（中文） |

---

## 二、功能模块

### 1. 部门管理
- **部门列表 `/depart/list/`**：展示所有部门
- **添加部门 `/depart/add/`**：POST 提交部门名称后入库
- **编辑部门 `/depart/<id>/edit/`**：按 ID 回填并更新部门名称
- **删除部门 `/depart/<id>/delete/`**：按 ID 删除后重定向回列表

### 2. 用户管理
- **用户列表 `/user/list/`**：展示用户姓名、年龄、余额、入职时间、性别、所属部门（外键关联显示部门名称）
- **原生表单新增 `/user/add/`**：手写 HTML 表单，性别/部门下拉框，入职时间接 bootstrap-datepicker 日历选择
- **ModelForm 新增 `/user/model/form/add/`**：用 ModelForm 自动生成输入框并自动加 Bootstrap 样式
- **编辑用户 `/user/<id>/edit/`**：ModelForm 回填旧数据，提交后更新
- **删除用户 `/user/<id>/delete/`**：按 ID 删除

### 3. 靓号管理（核心案例）
- **靓号列表 `/pretty/list/`**：按级别倒序展示号码、价格、级别（领导/队长/部长）、状态
- **号码搜索**：右上角搜索框，按手机号模糊匹配（`mobile__contains`），翻页时保留搜索条件
- **分页组件**：每页 10 条，首页 / 上一页 / 数字页码 / 下一页，封装在 `utils/pagination.py` 可复用
- **新增靓号 `/pretty/add/`**：ModelForm 自动渲染，带手机号正则校验（`1[3-9]` 开头 11 位）和手机号重复校验
- **编辑靓号 `/pretty/<id>/edit/`**：编辑时重复校验排除自身
- **删除靓号 `/pretty/<id>/delete/`**：按 ID 删除

---

## 三、路由一览

| 路由 | 方法 | 功能 | 对应视图 |
| --- | --- | --- | --- |
| `/depart/list/` | GET | 部门列表 | `views.depart_list` |
| `/depart/add/` | GET/POST | 添加部门 | `views.depart_add` |
| `/depart/<id>/edit/` | GET/POST | 编辑部门 | `views.depart_edit` |
| `/depart/<id>/delete/` | GET | 删除部门 | `views.depart_delete` |
| `/user/list/` | GET | 用户列表 | `views.user_list` |
| `/user/add/` | GET/POST | 原生表单新增用户 | `views.user_add` |
| `/user/model/form/add/` | GET/POST | ModelForm 新增用户 | `views.user_model_form_add` |
| `/user/<id>/edit/` | GET/POST | 编辑用户 | `views.user_edit` |
| `/user/<id>/delete/` | GET | 删除用户 | `views.user_delete` |
| `/pretty/list/` | GET | 靓号列表（搜索+分页） | `views.pretty_list` |
| `/pretty/add/` | GET/POST | 新增靓号 | `views.pretty_add` |
| `/pretty/<id>/edit/` | GET/POST | 编辑靓号 | `views.pretty_edit` |
| `/pretty/<id>/delete/` | GET | 删除靓号 | `views.pretty_delete` |

---

## 四、数据模型

当前模型定义于 `app01/models.py`：

```python
class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='部门名称', max_length=16)


class UserInfo(models.Model):
    """用户表"""
    name = models.CharField(verbose_name='姓名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='余额', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name='入职时间')
    gender_choices = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    depart = models.ForeignKey(verbose_name='部门', to='Department',
                               to_field='id', on_delete=models.SET_NULL, null=True, blank=True)


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    price = models.IntegerField(verbose_name='价格', default=0)
    level_choices = ((1, '领导'), (2, '队长'), (3, '部长'))
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)
    status_choices = ((1, '已占用'), (2, '未使用'))
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=2)
```

当前库中实际表：`app01_department`、`app01_userinfo`、`app01_prettynum`。

---

## 五、项目结构

```
ems/
├── manage.py                  # Django 管理入口
├── ems/                       # 项目配置目录
│   ├── settings.py            # 全局配置（MySQL、模板、静态文件、中文时区）
│   ├── urls.py                # 全局路由（include app01.urls）
│   ├── __init__.py            # 引入 PyMySQL 并安装为 MySQLdb
│   ├── asgi.py                # ASGI 入口
│   └── wsgi.py                # WSGI 入口
└── app01/                     # 业务应用
    ├── models.py              # 三个数据模型
    ├── views.py               # 全部视图函数
    ├── forms.py               # ModelForm 表单（UserModelForm/PrettyModelForm/PrettyEditModelForm）
    ├── urls.py                # 子路由
    ├── utils/
    │   └── pagination.py      # 通用分页组件（首页/上一页/页码/下一页，保留搜索参数）
    ├── templates/             # HTML 模板
    │   ├── layout.html        # 母版（导航栏 + 内容块）
    │   ├── depart_*.html       # 部门增删改查
    │   ├── user_*.html        # 用户增删改查（原生表单 + ModelForm 两种新增页）
    │   └── pretty_*.html       # 靓号增删改查（列表带搜索+分页）
    └── static/                # 静态资源（全部本地化，无需 CDN）
        ├── js/jquery-3.6.0.min.js
        └── plugins/
            ├── bootstrap-3.4.1/      # Bootstrap 全套
            └── bootstrap-datepicker/  # 日期选择器（含中文语言包）
```

---

## 六、环境准备

### 1. 环境要求
- Python 3.10+
- 本地 MySQL 服务（8.0）

### 2. 安装依赖
```bash
pip install django==5.2.17 pymysql
```

### 3. 配置数据库
项目默认连接 MySQL，配置位于 `ems/settings.py`：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ems',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

先登录 MySQL 创建数据库：
```sql
CREATE DATABASE ems DEFAULT CHARACTER SET utf8mb4;
```

### 4. 执行迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 启动服务
```bash
python manage.py runserver
```

浏览器访问 <http://127.0.0.1:8000/depart/list/>。

---

## 七、功能体验指引

| 页面 | 访问地址 | 操作说明 |
| --- | --- | --- |
| 部门管理 | <http://127.0.0.1:8000/depart/list/> | 部门的增删改查 |
| 用户管理 | <http://127.0.0.1:8000/user/list/> | 用户列表，可新增（两种表单）、编辑、删除 |
| 新增用户（原生） | <http://127.0.0.1:8000/user/add/> | 手写表单，入职时间有日历选择 |
| 新增用户（ModelForm） | <http://127.0.0.1:8000/user/model/form/add/> | 自动生成带样式的表单 |
| 靓号管理 | <http://127.0.0.1:8000/pretty/list/> | 搜索号码 + 翻页 + 增删改查 |
| 新增靓号 | <http://127.0.0.1:8000/pretty/add/> | 手机号格式校验 + 重复校验 |

---

## 八、常见问题排查

| 现象 | 原因与解决 |
| --- | --- |
| `ModuleNotFoundError: No module named 'pymysql'` | 未安装依赖，执行 `pip install pymysql` |
| `django.db.utils.OperationalError: (1045...)` | MySQL 账号密码错误，检查 `settings.py` 中 `USER` / `PASSWORD` |
| `(2003...) Can't connect to MySQL server` | MySQL 服务未启动，先启动 MySQL 服务 |
| `(1049...) Unknown database 'ems'` | 数据库未创建，先执行 `CREATE DATABASE ems ...` |
| 页面样式丢失 | 静态资源未本地化或 `STATICFILES_DIRS` 配置错误，确认 `app01/static/` 目录结构 |
| `That port is already in use` | 8000 端口被占用，换端口：`python manage.py runserver 8001` |
| 日期选择器不弹 | 确认 `user_add.html` 底部引入了 bootstrap-datepicker 的 css/js/zh-CN 三个文件 |

---

## 九、备注

- 静态资源已全部本地化（Bootstrap 3.4.1、jQuery 3.6.0、bootstrap-datepicker），页面样式无需联网。
- 导航栏写死为「联想用户管理系统」，右上角显示「登录 / 黄道旭」，仅作展示，未接入真实登录逻辑。
- 靓号级别为「领导 / 队长 / 部长」三档，数据库存 1/2/3，页面通过 `get_level_display` 翻译显示。
- 分页组件 `app01/utils/pagination.py` 为通用封装，用户管理等其他列表页可直接复用。
- `SECRET_KEY` 为开发环境默认值，**部署生产环境前必须更换**，并设置 `DEBUG = False`。
