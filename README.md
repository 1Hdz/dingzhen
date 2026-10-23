# Django 员工管理系统（EMS）

基于 Django + MySQL + Bootstrap 3 开发的员工管理后台，包含部门管理、用户管理、靓号管理三大模块。

## 技术栈

- **后端框架**：Django
- **数据库**：MySQL 8.0
- **前端**：Bootstrap 3 + jQuery + bootstrap-datepicker
- **ORM**：Django ORM + ModelForm

## 功能模块

### 1. 部门管理
- 部门列表展示
- 添加 / 编辑 / 删除部门

### 2. 用户管理
- 用户列表展示
- 原生表单新增用户（支持日期选择器）
- ModelForm 方式新增用户
- 编辑 / 删除用户
- 关联部门、性别下拉选择

### 3. 靓号管理
- 靓号列表（按级别排序）
- 号码模糊搜索
- 分页（首页 / 上一页 / 页码 / 下一页，保留搜索条件）
- 新增 / 编辑 / 删除靓号
- 手机号格式正则校验 + 重复校验
- 级别：领导 / 队长 / 部长

## 快速启动

```bash
# 1. 安装依赖
pip install django pymysql

# 2. 配置数据库（ems/settings.py 中 DATABASES）
# 需要先在 MySQL 中创建名为 ems 的数据库

# 3. 执行数据库迁移
python manage.py makemigrations
python manage.py migrate

# 4. 启动开发服务器
python manage.py runserver
```

访问 http://127.0.0.1:8000/

## 项目结构

```
ems/
├── manage.py
├── ems/                # 项目配置
│   ├── settings.py     # 数据库、静态文件配置
│   └── urls.py         # 路由入口
└── app01/              # 业务应用
    ├── models.py       # 数据模型（Department/UserInfo/PrettyNum）
    ├── views.py        # 视图函数
    ├── forms.py        # ModelForm 表单
    ├── urls.py         # 子路由
    ├── utils/
    │   └── pagination.py  # 分页组件
    ├── templates/      # HTML 模板
    └── static/         # 静态资源（Bootstrap/jQuery/datepicker）
```
