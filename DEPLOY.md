# 宝塔 Linux 部署指南（腾讯云服务器）

## 一、服务器准备

1. 购买腾讯云轻量应用服务器（推荐 **2核4G** 及以上配置）
2. 系统选择 **Ubuntu 22.04** 或 **CentOS 8**
3. 在安全组中开放端口：**22**、**80**、**443**、**8888**（宝塔面板）、**5000**（如需直接访问）

## 二、安装宝塔面板

SSH 连接服务器后执行：

```bash
# Ubuntu/Debian
wget -O install.sh https://download.bt.cn/install/install-ubuntu_6.0.sh && sudo bash install.sh ed8484bec

# CentOS
wget -O install.sh https://download.bt.cn/install/install_6.0.sh && sudo bash install.sh ed8484bec
```

安装完成后，会显示宝塔面板的访问地址、用户名和密码，请保存好。

## 三、宝塔面板基础配置

1. 浏览器访问 `http://服务器IP:8888`
2. 首次进入会提示绑定宝塔账号，按提示操作
3. 在弹出的推荐安装窗口中，选择安装：
   - **Nginx 1.24**（必须）
   - **MySQL 8.0**（可选，如想用 MySQL 代替 SQLite）

## 四、安装 Python 项目管理器

1. 宝塔左侧菜单 → **软件商店**
2. 搜索 **Python 项目管理器**
3. 点击 **安装**（选择最新版）

## 五、部署项目

### 5.1 拉取代码

在宝塔面板中打开 **终端**，执行：

```bash
cd /www/wwwroot
git clone https://github.com/teenybod/-.git filter_mgmt
cd filter_mgmt
```

### 5.2 创建 Python 项目

1. 宝塔左侧菜单 → **Python 项目管理器**
2. 点击 **添加项目**
3. 填写配置：

| 配置项 | 值 |
|--------|-----|
| 项目名称 | `filter_mgmt` |
| 路径 | `/www/wwwroot/filter_mgmt` |
| Python 版本 | `3.10` 或 `3.11`（推荐） |
| 框架 | `flask` |
| 启动方式 | `gunicorn` |
| 启动文件/文件夹 | `wsgi.py` |
| 端口 | `8000` |
| 是否安装模块依赖 | ✅ 勾选 |
| requirements.txt 路径 | `/www/wwwroot/filter_mgmt/requirements.txt` |

4. 点击 **确定**

宝塔会自动：
- 创建 Python 虚拟环境
- 安装 `requirements.txt` 中的依赖
- 启动 Gunicorn 服务

### 5.3 配置 Nginx 反向代理

1. 宝塔左侧菜单 → **网站**
2. 点击 **添加站点**
3. 填写：
   - 域名：你的域名（如 `filter.yourdomain.com`），如果没有域名可以填服务器 IP
   - 根目录：`/www/wwwroot/filter_mgmt`
   - PHP 版本：**纯静态**
4. 点击 **提交**
5. 在网站列表中找到刚创建的站点，点击 **设置**
6. 选择 **反向代理** 标签
7. 点击 **添加反向代理**
8. 填写：
   - 代理名称：`filter_mgmt`
   - 目标 URL：`http://127.0.0.1:8000`
   - 发送域名：`$host`
9. 点击 **提交**

### 5.4 配置 SSL（强烈建议）

1. 在站点设置中，选择 **SSL** 标签
2. 点击 **Let's Encrypt**，选择你的域名
3. 勾选 **强制 HTTPS**
4. 点击 **保存**

## 六、访问系统

- 浏览器访问你的域名或服务器 IP
- 首次访问会自动创建数据库和默认数据
- 默认管理员账号：**`admin`** / **`1234`**

## 七、后台定时任务说明

部署到宝塔后，以下功能将**正常工作**：

- ✅ 飞书 webhook 预警推送（每天 8:00 和 20:00 自动推送）
- ✅ 飞书多维表格自动同步（按配置间隔自动同步）
- ✅ 所有数据持久保存在服务器本地

## 八、常用维护命令

在宝塔终端中执行：

```bash
# 进入项目目录
cd /www/wwwroot/filter_mgmt

# 查看 Gunicorn 进程
ps aux | grep gunicorn

# 手动重启项目（在 Python 项目管理器中点重启更方便）
kill -HUP <gunicorn_pid>

# 查看日志
cd /www/wwwroot/filter_mgmt
tail -f error.log
```

## 九、常见问题

### Q1: 页面打开后没有文字显示？
A: 宝塔 + Linux 部署不会出现编码问题。如果出现，请检查 Nginx 配置中是否添加了 `charset utf-8;`

### Q2: 如何修改数据库为 MySQL？
A: 在宝塔中创建 MySQL 数据库，然后在 Python 项目管理器 → 项目中添加环境变量：
- `DATABASE_URL` = `mysql+pymysql://用户名:密码@localhost:3306/数据库名`
然后重新安装依赖（添加 `pymysql`）并重启项目。

### Q3: 如何修改访问密码 /  secret_key？
A: 在 Python 项目管理器 → 项目中添加环境变量：
- `SECRET_KEY` = 你自己设置的随机字符串（建议 32 位以上）

### Q4: 数据库文件在哪里？
A: 默认使用 SQLite，数据库文件位于 `/www/wwwroot/filter_mgmt/filter_mgmt.db`。备份时直接复制这个文件即可。
