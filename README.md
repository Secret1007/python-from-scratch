# Python FastAPI Project

一个基于 FastAPI 构建的完整后端 API 项目，包含用户认证、帖子管理、评论和标签系统。

## 功能特性

- 🔐 **用户认证系统**：JWT Token 认证，密码加密存储
- 📝 **帖子管理**：创建、编辑、删除和查询帖子
- 💬 **评论系统**：支持对帖子进行评论
- 🏷️ **标签管理**：为帖子添加标签，支持标签搜索
- 👤 **用户管理**：用户注册、登录、个人信息管理
- 🔒 **权限控制**：基于角色的访问控制

## 技术栈

- **FastAPI** - 现代、高性能的 Python Web 框架
- **SQLAlchemy** - Python SQL 工具包和 ORM
- **Alembic** - 数据库迁移工具
- **Pydantic** - 数据验证和设置管理
- **JWT** - JSON Web Token 认证
- **Uvicorn** - ASGI 服务器

## 安装步骤

### 1. 克隆项目

```bash
git clone git@github.com:Secret1007/python-from-scratch.git
cd python-from-scratch
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
```

### 3. 激活虚拟环境

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置环境变量

创建 `.env` 文件并配置必要的环境变量：

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./my_database.db
```

### 6. 运行数据库迁移

```bash
alembic upgrade head
```

## 运行项目

启动开发服务器：

```bash
uvicorn main:app --reload
```

服务器将在 `http://127.0.0.1:8000` 启动

## API 文档

启动服务器后，访问以下地址查看自动生成的 API 文档：

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 项目结构

```
py-txt/
├── api/                # API 路由
│   ├── auth.py        # 认证相关接口
│   ├── users.py       # 用户管理接口
│   ├── posts.py       # 帖子管理接口
│   ├── comment.py     # 评论接口
│   └── tags.py        # 标签接口
├── crud/              # 数据库操作
├── models/            # 数据库模型
├── schemas/           # Pydantic 模型
├── core/              # 核心功能（权限等）
├── alembic/           # 数据库迁移文件
├── main.py            # 应用入口
└── database.py        # 数据库配置
```

## 主要功能模块

### 用户认证
- 用户注册
- 用户登录
- JWT Token 验证

### 帖子管理
- 创建帖子
- 查询帖子列表
- 获取帖子详情
- 更新帖子
- 删除帖子

### 评论系统
- 添加评论
- 查看评论
- 删除评论

### 标签管理
- 创建标签
- 为帖子添加标签
- 按标签筛选帖子

## 开发

### 创建新的数据库迁移

```bash
alembic revision --autogenerate -m "描述更改内容"
```

### 应用迁移

```bash
alembic upgrade head
```

### 回滚迁移

```bash
alembic downgrade -1
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

