# 🚀 Flask 用户管理系统 ✨

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/flask-3.0-blue.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/ktovoz/demo-flask/docker-image.yml)](https://github.com/ktovoz/demo-flask/actions)


✨ 这是一个基于Flask的用户管理系统，提供完整的用户认证和权限管理解决方案。

## 📌 目录
- [✨ 功能特性](#-功能特性)
- [🛠️ 技术栈](#️-技术栈)
- [⚡ 快速开始](#-快速开始)
- [📚 API文档](#-api文档)
- [🏗️ 项目结构](#️-项目结构)
- [🤝 贡献指南](#-贡献指南)
- [📜 许可证](#-许可证)

## ✨ 功能特性

<details>
<summary><strong>🔐 用户认证</strong></summary>

- ✅ 📧 用户注册：支持邮箱验证和安全密码存储
- ✅ 🔑 登录/注销：基于Flask-Login的会话管理
</details>

<details>
<summary><strong>👥 用户管理</strong></summary>

- ✅ 🛠️ CRUD操作：创建、读取、更新和删除用户
- ✅ 👨‍💻 用户分组：超级管理员、管理员和普通用户三级权限
</details>

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| 🐍 Python 3.x | 后端语言 |
| 🏗️ Flask 3.0 | Web框架 |
| 🗃️ SQLAlchemy 2.0 | ORM |
| 🔑 Flask-Login | 用户会话管理 |
| 📝 Flask-WTF | 表单处理 |

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/your-repo/demo-flask.git
cd demo-flask

# 创建虚拟环境
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境
cp .env.example .env

# 初始化数据库
flask db init
flask db migrate
flask db upgrade

# 启动应用
flask run

# 使用Gunicorn生产环境部署
gunicorn -w 4 -b 0.0.0.0:5000 "run:app"
```

## API文档

访问 `/api/docs` 查看Swagger API文档

### API端点

#### 用户认证
| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/auth/register` | 用户注册 |
| POST | `/api/auth/login` | 用户登录 |
| POST | `/api/auth/logout` | 用户注销 |
| POST | `/api/auth/reset-password` | 密码重置 |

#### 用户管理
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/users` | 获取用户列表 |
| POST | `/api/users` | 创建新用户 |
| GET | `/api/users/{id}` | 获取单个用户信息 |
| PUT | `/api/users/{id}` | 更新用户信息 |
| DELETE | `/api/users/{id}` | 删除用户 |

#### 用户组管理
| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/groups` | 获取用户组列表 |
| POST | `/api/groups` | 创建新用户组 |
| PUT | `/api/groups/{id}` | 更新用户组信息 |
| DELETE | `/api/groups/{id}` | 删除用户组 |

## 项目结构

```
.
├── .github/
│   └── workflows/
│       └── docker-image.yml
├── app/
│   ├── __init__.py
│   ├── commands.py
│   ├── controllers/
│   │   ├── auth.py
│   │   ├── group.py
│   │   ├── main.py
│   │   └── user.py
│   ├── forms/
│   │   └── auth.py
│   ├── models/
│   │   ├── group.py
│   │   └── user.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── errors/
│   │   ├── index.html
│   │   ├── login.html
│   │   └── register.html
│   └── utils/
│       └── decorators.py
├── config.py
├── Dockerfile
├── instance/
│   └── app.db
├── migrations/
│   └── env.py
├── requirements.txt
├── run.py
└── README.md
```

## 贡献指南

欢迎提交Pull Request。请确保：
1. 代码符合PEP8规范
2. 添加适当的测试
3. 更新相关文档

## 许可证

MIT License