# 联通用户管理系统（EMS）

基于 **Django 5.0** 的用户与业务管理系统示例，包含 **部门管理、用户管理、靓号管理、任务管理、订单管理、数据统计、文件上传、城市列表** 八个模块，覆盖增删改查、ModelForm 表单、搜索与分页、Ajax JSON 接口、Excel 批量导入、文件上传（三种方式）、ECharts / Highcharts 图表等常见 Web 开发功能。

## 目录

- [一、功能特性](#一功能特性)
  - [部门管理](#部门管理) · [用户管理](#用户管理) · [靓号管理](#靓号管理) · [任务管理](#任务管理) · [订单管理](#订单管理) · [数据统计](#数据统计)
  - [文件上传](#文件上传) · [城市列表（文件）](#城市列表文件) · [通用能力](#通用能力)
- [二、技术栈](#二技术栈)
- [三、项目结构](#三项目结构)
- [四、数据模型](#四数据模型)
- [五、路由说明](#五路由说明)
- [六、快速开始](#六快速开始)
  - [1. 环境要求](#1-环境要求) · [2. 安装依赖](#2-安装依赖) · [3. 创建数据库](#3-创建数据库)
  - [4. 配置数据库](#4-配置数据库) · [5. 执行迁移](#5-执行迁移) · [6. 启动开发服务器](#6-启动开发服务器) · [7. 登录](#7-登录)
- [七、核心实现说明](#七核心实现说明)
- [八、注意事项与待完善](#八注意事项与待完善)

---

## 一、功能特性

### 部门管理
- 部门列表（带分页）
- 新建部门
- 编辑部门
- 删除部门
- **Excel 批量导入**（`openpyxl` 逐行读取，重复名称自动跳过）

### 用户管理
- 用户列表（带分页，展示部门、性别等字段）
- 基于 **ModelForm** 新建用户，自动完成字段校验
- 编辑用户（`instance` 回显 + 更新）
- 删除用户

### 靓号管理
- 靓号列表（按级别排序 + 分页）
- 按手机号模糊搜索（保留分页参数）
- 新建 / 编辑 / 删除靓号
- 业务校验：**当状态为“已占用”时，手机号在全表内不可重复**（编辑时自动排除自身）

### 任务管理
- 任务列表（ID、标题、级别、负责人，按 ID 倒序 + 分页）
- 表单 + Ajax 新建任务，校验错误回显在对应输入框下方
- 新建成功后 `location.reload()` 自动刷新，新任务出现在第一行
- 行内「编辑」进入独立编辑页（GET 回显、POST 校验保存），「删除」二次确认后回到列表

### 订单管理
- 订单列表（订单号、名称、价格、状态、管理员，分页）
- 新建 / 编辑共用 Bootstrap 弹窗，全部通过 Ajax 读写
- 订单号由后端按“时间戳 + 4 位随机数”生成，管理员取当前登录用户
- 删除前弹出确认框，价格非法值错误提示定位到对应字段

### 数据统计
- 折线图 / 柱状图 / 饼图三张图表（ECharts）
- 后端只返回 `{"status": ..., "data": ...}` 的 JSON，前端负责 `setOption` 渲染
- `/chart/highcharts/` 演示 Highcharts，CDN 不可用时自动回退到本地 `echarts.js`

### 文件上传
- **原始方式**（`/upload/list/`）：从 `request.FILES` 取文件，`chunks()` 分块写盘，适合大文件
- **普通 Form 上传**（`/upload/form/`）：文件由视图自己写盘到 `media/boss/`，数据库只存相对路径（`Boss` 表）
- **ModelForm 上传**（`/upload/modal/form/`）：`FileField` 自动按 `upload_to` 保存，路径写入数据库（`City` 表）
- **头像预览**（`/tt/`）：`FileReader` 在浏览器本地预览选中的图片，上传后存到 `media/avatar/`（`XX` 表）
- 头像页下方会列出已上传的记录（缩略图 + 名称），支持删除（同时删掉 `media/avatar/` 里的文件）
- 媒体文件通过 `/media/` 前缀访问（开发环境由 `re_path` + `django.views.static.serve` 提供）

### 城市列表（文件）
- 城市列表展示 Logo（`<img src="/media/{{ obj.img }}">`）、名称、人口
- 新建城市复用 ModelForm，`FileField` 自动存到 `media/city/`，保存后重定向回列表
- 用于验证 `MEDIA_ROOT`、`MEDIA_URL`、`/media/` 路由整条链路是否打通

### 通用能力
- `BootstrapForm` / `BootstrapModelForm`：统一为表单字段添加 `form-control` 样式与 `placeholder`
- `bootstrap_exclude_fields`：文件框等字段可排除在外，保持原生样式
- `Pagination`：可复用的分页组件，支持首页 / 上一页 / 页码 / 下一页 / 尾页 / 页码跳转，并在跳转时保留搜索等查询参数
- `AuthMiddleware`：统一登录校验，未登录访问业务页会跳转到 `/login/`
- 基于 Bootstrap 3.4.1 + jQuery 的页面布局（`layout.html` 母版）

---

## 二、技术栈

| 类别 | 技术 |
| --- | --- |
| 语言 | Python 3.10+（本项目在 3.12 下验证） |
| Web 框架 | Django 5.0.14 |
| 数据库 | MySQL 5.7+ / 8.0（驱动 `mysqlclient`，也可换 `pymysql`） |
| 表格处理 | openpyxl 3.1.x |
| 前端 | Bootstrap 3.4.1、jQuery 3.6.0、bootstrap-datepicker |
| 图表 | ECharts（本地 `static/js/echarts.js`）、Highcharts（CDN，可降级到 ECharts） |
| 模板引擎 | Django Template |
| 图片处理 | Pillow（登录图片验证码、头像占位图） |

---

## 三、项目结构

```text
ems/
├─ manage.py                    # Django 管理脚本
├─ README.md
├─ requirements.txt             # 依赖清单（pip install -r requirements.txt）
├─ ems/                         # 项目配置
│  ├─ settings.py               # 数据库、MEDIA_ROOT/MEDIA_URL、静态文件、中间件
│  ├─ urls.py                   # 根路由
│  ├─ wsgi.py
│  └─ asgi.py
├─ media/                       # 用户上传文件（MEDIA_ROOT，默认被 .gitignore 排除）
│  ├─ boss/                     # Form 上传的头像
│  ├─ city/                     # 城市 Logo
│  └─ avatar/                   # 头像预览
└─ app01/                       # 业务应用
   ├─ models.py                 # Department / UserInfo / PrettyNum / Admin / Task / Order / Boss / City / XX
   ├─ apps.py
   ├─ admin.py
   ├─ tests.py                  # 暂无自动化测试
   ├─ middleware/
   │  └─ auth.py                # 登录校验中间件
   ├─ migrations/               # 数据库迁移（0001 ~ 0009）
   ├─ views/                    # 视图（按业务拆分）
   │  ├─ __init__.py            # 统一导出视图函数
   │  ├─ account.py             # 登录 / 注销 / 图片验证码
   │  ├─ admin.py               # 管理员账户管理
   │  ├─ depart.py              # 部门管理（含 Excel 批量导入）
   │  ├─ user.py                # 用户管理
   │  ├─ pretty.py              # 靓号管理
   │  ├─ task.py                # 任务管理
   │  ├─ order.py               # 订单管理
   │  ├─ chart.py               # 数据统计（ECharts / Highcharts）
   │  ├─ upload.py              # 文件上传（原始 / Form / ModelForm / 头像预览）
   │  └─ city.py                # 城市列表（FileField + MEDIA）
   ├─ utils/                    # 公共组件
   │  ├─ bootstrap.py           # BootstrapForm / BootstrapModelForm 基类
   │  ├─ form.py                # 业务表单（UserModelForm / PrettyModelForm / AdminModelForm 等）
   │  ├─ pagination.py          # 分页组件
   │  ├─ code.py                # 图片验证码生成
   │  └─ encrypt.py             # MD5 加密
   ├─ templates/                # 页面模板
   │  ├─ layout.html            # 公共母版（导航 + 内容区 + css/js 区块）
   │  ├─ login.html
   │  ├─ admin_list.html / change.html
   │  ├─ depart_*.html          # 注意：实际使用的是 depart_*2.html
   │  ├─ user_list.html / user_model_form_add.html / user_edit.html
   │  ├─ pretty_list.html / pretty_add.html / pretty_edit.html
   │  ├─ task_list.html / task_edit.html
   │  ├─ order_list.html
   │  ├─ chart_list.html / highcharts.html
   │  ├─ upload_list.html       # 原始方式上传
   │  ├─ upload_form.html       # Form / ModelForm / 新建城市共用
   │  ├─ tt.html                # 头像预览 + 已上传列表
   │  └─ city_list.html         # 城市列表（展示 Logo）
   └─ static/                   # 静态资源
      ├─ plugins/              # Bootstrap 3.4.1、bootstrap-datepicker
      ├─ js/                   # jQuery、datepicker、echarts.js
      ├─ css/
      └─ img/                  # 1.png、default.png（头像占位图）
```

> 用户上传的文件存放在项目根目录的 `media/` 下（`MEDIA_ROOT`），数据库只保存相对路径。

---

## 四、数据模型

### Department（部门表）
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | BigAutoField | 主键，自动生成 |
| title | CharField(32) | 部门名称 |

### UserInfo（员工表）
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | BigAutoField | 主键，自动生成 |
| name | CharField(16) | 姓名 |
| password | CharField(64) | 密码（示例项目为明文存储，仅用于练习） |
| age | IntegerField | 年龄 |
| account | DecimalField(10,2) | 账户余额，默认 0 |
| create_time | DateTimeField | 入职时间 |
| gender | SmallIntegerField | 性别：1-男，2-女 |
| depart | ForeignKey(Department) | 所属部门，级联删除 |

### PrettyNum（靓号表）
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | BigAutoField | 主键，自动生成 |
| mobile | CharField(11) | 手机号 |
| price | IntegerField | 价格，默认 0 |
| level | SmallIntegerField | 级别：1~4 级，默认 1 |
| status | SmallIntegerField | 状态：1-已占用，2-未使用，默认 2 |

### Admin（管理员表）
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | BigAutoField | 主键，自动生成 |
| username | CharField(32) | 用户名 |
| password | CharField(64) | 密码（MD5，`utils/encrypt.py`） |

### Task（任务表）
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | BigAutoField | 主键，自动生成 |
| level | SmallIntegerField | 级别：1-紧急，2-重要，3-普通，默认 1 |
| title | CharField(64) | 标题 |
| detail | TextField | 详细信息 |
| leader | ForeignKey(UserInfo) | 负责人，级联删除 |

### Order（订单表）
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | BigAutoField | 主键，自动生成 |
| oid | CharField(64) | 订单号（后端生成：时间戳 + 4 位随机数） |
| title | CharField(32) | 名称 |
| price | IntegerField | 价格 |
| status | SmallIntegerField | 状态：1-待支付，2-已支付，默认 1 |
| admin | ForeignKey(Admin) | 管理员，取当前登录用户，级联删除 |

### Boss（老板表，普通 Form 上传示例）
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | BigAutoField | 主键，自动生成 |
| name | CharField(32) | 姓名 |
| age | IntegerField | 年龄 |
| img | CharField(128) | 头像相对路径（如 `boss/xxx.png`，文件由视图写盘） |

### City（城市表，FileField 示例）
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | BigAutoField | 主键，自动生成 |
| name | CharField(32) | 名称 |
| count | IntegerField | 人口 |
| img | FileField(128, upload_to='city/') | Logo，文件自动保存到 `MEDIA_ROOT/city/` |

### XX（头像预览示例）
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | BigAutoField | 主键，自动生成 |
| title | CharField(32) | 名称 |
| image | FileField(upload_to='avatar/') | 头像，文件自动保存到 `MEDIA_ROOT/avatar/` |

---

## 五、路由说明

| 模块 | URL | 视图 | 功能 |
| --- | --- | --- | --- |
| 认证 | `/login/` | `login` | 登录（用户名 + 密码 + 图片验证码） |
| 认证 | `/image/code/` | `image_code` | 生成图片验证码（存入 session） |
| 认证 | `/logout/` | `logout` | 注销，清空 session |
| 管理员 | `/admin/list/` | `admin_list` | 管理员列表（分页） |
| 管理员 | `/admin/add/` | `admin_add` | 新建管理员（校验两次密码） |
| 管理员 | `/admin/<int:nid>/edit/` | `admin_edit` | 编辑管理员 |
| 管理员 | `/admin/delete/` | `admin_delete` | 删除管理员 |
| 管理员 | `/admin/<int:nid>/reset/` | `admin_reset_password` | 重置密码 |
| 部门 | `/depart/list/` | `depart_list` | 部门列表（分页） |
| 部门 | `/depart/add/` | `depart_add` | 新建部门 |
| 部门 | `/depart/<int:nid>/edit/` | `depart_edit` | 编辑部门 |
| 部门 | `/depart/delete/` | `depart_delete` | 删除部门 |
| 部门 | `/depart/multi/` | `depart_multi` | Excel 批量导入部门 |
| 用户 | `/user/list/` | `user_list` | 用户列表（分页） |
| 用户 | `/user/model/form/add/` | `user_model_form_add` | 新建用户（ModelForm，入职日期用 datepicker） |
| 用户 | `/user/<int:nid>/edit/` | `user_edit` | 编辑用户 |
| 用户 | `/user/delete/` | `user_delete` | 删除用户 |
| 靓号 | `/pretty/list/` | `pretty_list` | 靓号列表（搜索 + 分页） |
| 靓号 | `/pretty/add/` | `pretty_add` | 新建靓号 |
| 靓号 | `/pretty/<int:nid>/edit/` | `pretty_edit` | 编辑靓号 |
| 靓号 | `/pretty/delete/` | `pretty_delete` | 删除靓号 |
| 任务 | `/task/list/` | `task_list` | 任务列表（表单 + 分页表格） |
| 任务 | `/task/add/` | `task_add` | Ajax 新建任务 |
| 任务 | `/task/<int:nid>/edit/` | `task_edit` | 编辑任务 |
| 任务 | `/task/delete/` | `task_delete` | 删除任务 |
| 任务 | `/task/ajax/` | `task_ajax` | Ajax 演示接口（返回 JSON） |
| 订单 | `/order/list/` | `order_list` | 订单列表（分页） |
| 订单 | `/order/add/` | `order_add` | 新建订单（Ajax） |
| 订单 | `/order/detail/` | `order_detail` | 订单详情（Ajax） |
| 订单 | `/order/edit/` | `order_edit` | 编辑订单（Ajax） |
| 订单 | `/order/delete/` | `order_delete` | 删除订单（Ajax） |
| 统计 | `/chart/list/` | `chart_list` | 数据统计页面（三张图） |
| 统计 | `/chart/bar/` | `chart_bar` | 柱状图数据（JSON） |
| 统计 | `/chart/pie/` | `chart_pie` | 饼图数据（JSON） |
| 统计 | `/chart/line/` | `chart_line` | 折线图数据（JSON） |
| 统计 | `/chart/highcharts/` | `highcharts` | Highcharts 演示页面 |
| 上传 | `/upload/list/` | `upload_list` | 原始方式上传 |
| 上传 | `/upload/form/` | `upload_form` | 普通 Form 上传（Boss 表） |
| 上传 | `/upload/modal/form/` | `upload_modal_form` | ModelForm 上传（City 表） |
| 上传 | `/tt/` | `tt` | 头像预览 + 已上传列表（XX 表） |
| 上传 | `/tt/delete/` | `tt_delete` | 删除头像（同时删 media 文件） |
| 城市 | `/city/list/` | `city_list` | 城市列表（展示 Logo） |
| 城市 | `/city/add/` | `city_add` | 新建城市（ModelForm 上传文件） |
| 媒体 | `/media/<path>` | `django.views.static.serve` | 开发环境访问 `MEDIA_ROOT` 下的文件 |
| 后台 | `/admin/` | Django Admin | Django 自带后台，注册在最后避免抢占 `/admin/...` |

> 项目没有根路由 `/`，启动后请直接访问 `/login/` 或任意列表页，例如 <http://127.0.0.1:8000/pretty/list/>。

---

## 六、快速开始

### 1. 环境要求
- Python 3.10+（推荐 3.12）
- MySQL 5.7+ / 8.0
- pip

### 2. 安装依赖

```bash
pip install -r requirements.txt
# 或手动安装：
pip install django==5.0.14 mysqlclient openpyxl Pillow
```

> 仓库根目录已提供 `requirements.txt`（Django / mysqlclient / openpyxl / Pillow 的固定版本）。

> 若 `mysqlclient` 安装失败，可改用 `pymysql`：安装后在 `ems/__init__.py` 中加入
> `import pymysql; pymysql.install_as_MySQLdb()`。
>
> `Pillow` 是登录验证码的必需依赖，漏装会导致 `/image/code/` 报错、无法登录。
>
> 验证码字体在 `app01/utils/code.py` 中写死为 `arial.ttf`；Linux/macOS 上若缺字体，
> 请改成系统里存在的字体文件（如 `DejaVuSans.ttf`）。
>
> 本机装了多个 Python 版本时，请用**装了上述依赖的那个解释器**运行，例如 Windows 下：
> `py -3.12 manage.py runserver`。

### 3. 创建数据库

```sql
CREATE DATABASE ems DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

### 4. 配置数据库

编辑 `ems/settings.py` 中的 `DATABASES`：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ems',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### 5. 执行迁移

```bash
python manage.py migrate
```

> 媒体目录已在 `ems/settings.py` 中配置：
> `MEDIA_ROOT = os.path.join(BASE_DIR, "media")`、`MEDIA_URL = "/media/"`。
> `media/boss/`、`media/city/`、`media/avatar/` 会在首次上传时自动创建，也可以手动预先建好。

### 6. 启动开发服务器

```bash
python manage.py runserver
```

### 7. 登录

浏览器访问 <http://127.0.0.1:8000/login/>，输入用户名、密码和图片验证码。

- 迁移 `0005_seed_admin` 会插入默认管理员 **颜楷 / 123456**（`0006` 再把它转为 MD5）；
- 也可以在 `/admin/list/` 里新建管理员，或直接往 `app01_admin` 表插数据。

---

## 七、核心实现说明

### 1. 表单样式基类
`app01/utils/bootstrap.py` 里的 `BootstrapForm` / `BootstrapModelForm` 在初始化时遍历所有字段，
统一设置 `class="form-control"` 和 `placeholder`；已存在的控件属性（如 `Textarea` 的 `rows`）会被保留。

### 2. 靓号号码唯一校验
`app01/utils/form.py` 的 `PrettyModelForm.clean()`：

```python
if mobile and status == 1:                      # 仅“已占用”时校验
    queryset = models.PrettyNum.objects.filter(mobile=mobile)  # 全表范围
    if self.instance and self.instance.pk:      # 编辑时排除自身
        queryset = queryset.exclude(pk=self.instance.pk)
    if queryset.exists():
        self.add_error("mobile", "该手机号已被占用，号码不能重复")
```

错误信息会挂到 `mobile` 字段，页面通过 `{{ field.errors.0 }}` 直接展示。

### 3. 表单排除字段（文件框）
`BootstrapForm` / `BootstrapModelForm` 支持 `bootstrap_exclude_fields`，列在其中的字段（通常是
`FileField`）不会套上 `form-control`，文件框保持原生样式：

```python
class UpForm(BootstrapForm):
    bootstrap_exclude_fields = ["img"]
```

### 4. 分页组件
`app01/utils/pagination.py` 的 `Pagination` 接收 `request` 与 `queryset`，提供：

- `page_queryset`：当前页数据
- `html()`：生成分页按钮 HTML（首页 / 上一页 / 页码 / 下一页 / 尾页 / 跳转框）
- 通过深拷贝 `request.GET` 并更新 `page` 参数，保证搜索条件在翻页时不会丢失

### 5. 登录态与订单归属
`AuthMiddleware`（`app01/middleware/auth.py`）对 `/login/`、`/image/code/`、`/static/` 之外的所有请求校验
`request.session["info"]`，未登录一律跳转登录页。登录成功时写入：

```python
request.session["info"] = {"id": admin.id, "name": admin.username}
```

订单的「管理员」正是取 `session["info"]["id"]`，所以**改过 session 结构后需要退出重新登录一次**。

---

## 八、注意事项与待完善

- `ems/settings.py` 中的 `SECRET_KEY` 与数据库密码目前是明文，**公开仓库或部署上线前请改为环境变量**，并关闭 `DEBUG`。
- 上传 GitHub 时注意 `.gitignore`：`media/`、`__pycache__/`、`.idea/`、`*.log`、`.env` 都不应提交。
- `depart_*1.html` 为旧版页面，当前视图使用的是 `depart_*2.html`。
- 暂无自动化测试（`app01/tests.py` 仍是默认空壳）。
- 批量导入依赖 `openpyxl`；Excel 第一行为表头，从第二行开始读取第一列的部门名称，重名自动跳过。
- `chart_list.html` 引用的是 `static/js/echarts.js`（与 `static/js/js/echarts.js` 是同一份，后者可删除）；Highcharts 页面优先走 CDN，离线时回退到 `echarts.js`。
- 文件上传三要素：`method="post"`、`enctype="multipart/form-data"`、控件带 `name`；漏掉 `enctype` 时 `request.FILES` 取不到文件。
- `/media/` 的开发环境路由（`re_path` + `django.views.static.serve`）只用于调试，生产环境应交给 Nginx 等静态文件服务。
- 上传落盘位置：`/upload/list/` 按原名写到项目根目录；`/upload/form/` → `media/boss/`；`/upload/modal/form/` → `media/city/`；`/tt/` → `media/avatar/`。
- 头像预览的默认占位图是 `app01/static/img/default.png`（本项目已生成），缺失时会显示裂图。
- 待完善：城市列表没有编辑 / 删除；任务列表没有按级别筛选；`/chart/*` 的数据仍是写死的示例，可改为 `values(...).annotate(...)` 的真实聚合。
