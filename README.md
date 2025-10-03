# Flask 用户管理系统

基于 Flask 3 打造的演示级用户管理平台，内置账号体系、权限分组、可视化后台与日志监控示例，适合作为中小型管理后台或团队内部工具的脚手架。

## ✨ 功能亮点
- 登录 / 注册 / 退出与记住我能力，可一键填充演示账号（login 页按钮自动填写 `demo / demo1234`）
- 默认管理员账号（`admin / admin123`）与演示账号自动注入，`init-db` 或项目启动即可使用
- 角色分组：超级管理员 / 管理员 / 普通用户，对应增删改查、分组调整、重置密码等权限
- 后台仪表盘采用模块化模板 + 动态 JS，支持用户创建、修改、删除、调组、重置密码等操作后即时刷新
- Loguru 集成结构化日志，桥接标准 logging 并支持轮转、保留策略与多终端输出
- Dockerfile 与 GitHub Actions 示例，开箱即用的容器与 CI 流程

## 🧱 技术栈
| 组件 | 说明 |
|------|------|
| Python 3.10+ | 运行环境 |
| Flask 3.0 | Web 框架、Blueprint 体系 |
| SQLAlchemy 2.x / Flask-Migrate | ORM 与数据库迁移 |
| Flask-Login / Flask-WTF | 会话认证与表单校验 |
| Loguru | 日志管理与轮转 |
| Bootstrap 5 | 响应式前端 UI |

## 🚀 快速开始
```bash
# 克隆项目
git clone https://github.com/your-repo/demo-flask.git
cd demo-flask

# 创建并激活虚拟环境
python -m venv .venv
# Windows
.venv\Scriptsctivate
# macOS / Linux
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库并写入默认账号
flask --app run.py init-db

# 启动开发服务器
flask --app run.py --debug run
```
访问 `http://127.0.0.1:5000`，使用 `admin / admin123` 登录后台；登录页的“试用演示账号”按钮可一键填入 `demo / demo1234`。

## 🗂️ 项目结构（节选）
```
app/
├── __init__.py            # 应用工厂：注册扩展/蓝图/命令
├── extensions.py          # db、login_manager、migrate 等集中声明
├── commands.py            # Flask CLI：数据库初始化
├── controllers/           # 蓝图 (auth / user / group / main)
├── services/              # 业务服务层 (auth_service, user_service)
├── models/                # SQLAlchemy 模型
├── templates/
│   ├── layouts/           # 基础与后台布局 (base, auth_base, app_base)
│   ├── partials/          # 侧边栏、数据表、模态框、Dashboard 脚本等片段
│   └── errors/            # 403 / 404 / 500 页面
├── utils/                 # 日志配置、种子数据、请求日志辅助
└── ...
```

## 🧩 架构要点
- **扩展集中**：`app/extensions.py` 统一实例化并在工厂中初始化，避免循环依赖
- **服务分层**：`app/services/` 处理认证、用户 CRUD、密码与分组逻辑，控制器仅负责请求解析与响应
- **日志统一**：`app/utils/logging.py` 通过 Loguru 接管 stdout/文件，并桥接标准库 logging
- **模板拆分 + JS 状态管理**：布局 (`layouts/`) + 片段 (`partials/`) 组合后台页面；`Dashboard` 脚本负责渲染、权限控制、空态提示与消息反馈
- **数据播种**：`ensure_seed_data` 会在 CLI 与应用启动时运行，确保默认角色与管理员 / 演示账号存在
- **行为日志**：`app/utils/request_logger.py` 提供请求与用户操作日志辅助，便于审计与排障

## 🧪 开发与测试
```bash
# 运行测试（示例）
pytest

# 数据库迁移
flask --app run.py db migrate -m "message"
flask --app run.py db upgrade
```
> 建议为新增功能补充 Pytest 用例（TestingConfig 默认使用内存 SQLite 与禁用 CSRF）。

## 📝 日志配置
- 默认输出到标准输出与 `instance/logs/app.log`
- 可通过环境变量自定义：`LOG_LEVEL`、`LOG_ROTATION`、`LOG_RETENTION`、`LOG_PATH / LOG_DIR`、`LOG_BACKTRACE`、`LOG_DIAGNOSE`

## 🤝 贡献指南
1. Fork & 新建分支，遵循 Conventional Commits（如 `feat(user): ...`）
2. 保持 PEP 8 风格（4 空格缩进），推荐 `black`/`flake8`
3. 为功能附测试、更新文档或截图，并在 PR 中写明验证步骤
4. 避免提交本地数据库、`__pycache__`、IDE 配置等临时文件

## 📄 许可
本项目基于 MIT License 发布。
