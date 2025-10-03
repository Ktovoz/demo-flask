# Flask 用户管理系统

一套基于 Flask 3 的演示级用户管理平台，包含账户认证、权限分组、可视化后台与自动化部署示例。项目已经模块化拆分，适合作为中小型管理后台或团队内部工具的脚手架。

## ✨ 功能亮点
- 登录 / 注册 / 退出与记住我能力，基于 Flask-Login 管理会话
- 演示账号 (demo/demo1234) 与初始化种子脚本，便于快速体验
- 角色分组（超级管理员 / 管理员 / 普通用户）与简单权限判定
- 后台仪表盘：用户 CRUD、重置密码、管理成员归属
- Loguru 驱动的结构化日志输出，附加轮转与标准 logging 接入
- Docker 与 GitHub Actions 示例，方便扩展部署

## 🧱 技术栈
| 组件 | 说明 |
|------|------|
| Python 3.10+ | 运行环境 |
| Flask 3.0 | Web 框架 & 蓝图体系 |
| SQLAlchemy 2.x / Flask-Migrate | ORM 与数据库迁移 |
| Flask-Login / Flask-WTF | 认证与表单校验 |
| Loguru | 结构化日志与轮转输出 |
| Bootstrap 5 | 响应式前端 UI |

## 🚀 快速开始
`ash
# 克隆项目
git clone https://github.com/your-repo/demo-flask.git
cd demo-flask

# 创建并激活虚拟环境
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库并写入种子账号
flask --app run.py init-db

# 启动开发服务器
flask --app run.py --debug run
`
访问 http://127.0.0.1:5000，使用 demo / demo1234 体验后台。

## 🗂️ 项目结构
`
app/
├── __init__.py            # 应用工厂，注册扩展/蓝图/命令
├── extensions.py          # db、login_manager、migrate 等集中声明
├── commands.py            # Flask CLI：数据库初始化
├── controllers/           # 蓝图 (auth / user / group / main)
├── services/              # 业务服务层 (auth_service, user_service)
├── forms/                 # WTForms 定义
├── models/                # SQLAlchemy 模型
├── templates/
│   ├── layouts/           # 基础与后台布局 (base, auth_base, app_base)
│   ├── partials/          # 侧边栏、数据表、模态框、脚本等片段
│   └── errors/            # 403 / 404 / 500 页面
├── utils/                 # 日志配置、数据种子等工具
└── ...
`

## 🧩 架构要点
- **扩展分离**：pp/extensions.py 集中实例化并在工厂中初始化，避免循环依赖。
- **服务层**：pp/services/ 处理登录、用户 CRUD、密码与分组变更，控制器仅负责请求解析与响应。
- **日志统一**：pp/utils/logging.py 通过 Loguru 将 stdout 与文件日志接管，并桥接标准库 logging。
- **模板拆分**：布局 (layouts/) + 片段 (partials/) 组合成后台页面，便于后续扩展页面或替换 UI。
- **数据引导**：ensure_seed_data 会在 CLI 与应用启动时运行，确保基础用户组与 demo 账号存在。

## 🧪 开发与测试
`ash
# 运行单元 / 集成测试（示例）
pytest

# 数据库迁移
flask --app run.py db migrate -m "message"
flask --app run.py db upgrade
`
> 建议为新增功能补充 Pytest 用例（默认使用内存 SQLite 与禁用 CSRF 的 TestingConfig）。

## 📝 日志
- 默认输出到标准输出与 instance/logs/app.log
- 可通过环境变量自定义:
  - LOG_LEVEL（默认 INFO）
  - LOG_ROTATION / LOG_RETENTION
  - LOG_PATH 或 LOG_DIR
  - LOG_BACKTRACE / LOG_DIAGNOSE

## 🤝 贡献指南
1. Fork & 新建分支，遵循 Conventional Commits（如 eat(user): ...）
2. 保持 lack / lake8 风格（PEP 8 / 4 空格缩进）
3. 增补测试、更新文档或截图，并在 PR 中描述验证步骤
4. 避免提交本地数据库、__pycache__、IDE 配置等构建产物

## 📄 许可
本项目基于 MIT License 发布。
