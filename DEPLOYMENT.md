# 🚀 全栈部署指南 (Full Stack Deployment)

你的项目是一个**前后端分离**的全栈应用 (Vue + FastAPI)，因此不能只部署到 Netlify（它主要支持前端）。

**最佳部署路径：**
1. **GitHub** (代码托管) ✅ *已完成准备*
2. **Render / Railway / Fly.io** (部署后端 API)
3. **Netlify / Vercel** (部署前端页面)

---

## 📦 第一步：上传到 GitHub (必须)

请按照根目录下的 `GITHUB_UPLOAD.md` 操作，先把代码推送到 GitHub。这是后续所有部署的基础。

---

## 🖥️ 第二步：部署后端 (Backend)

推荐使用 **Render** (有免费层) 或 **Railway**。

### 以 Render 为例：
1. 注册并登录 [render.com](https://render.com/)。
2. 点击 **New +** -> **Web Service**。
3. 连接你的 GitHub 仓库 (`talking-skills`)。
4. 配置参数：
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. **添加环境变量 (Environment Variables)**:
   - `AI_API_KEY`: (你的 Key)
   - `AI_BASE_URL`: (你的 Base URL)
   - `AI_MODEL_NAME`: (你的模型名)
6. 点击 **Create Web Service**。
7. 等待部署完成，你会获得一个后端地址，例如：`https://talking-skills-api.onrender.com`。**复制这个地址！**

---

## 🌐 第三步：部署前端 (Frontend) -> Netlify

1. 注册并登录 [netlify.com](https://www.netlify.com/)。
2. 点击 **Add new site** -> **Import from existing project**。
3. 选择 **GitHub** -> 授权并选择你的仓库。
4. **关键配置** (Netlify 会自动识别 `netlify.toml`，但请检查)：
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
5. **设置环境变量 (Environment variables)**:
   - 点击 "Show advanced" 或部署后的 "Site configuration" -> "Environment variables"。
   - Key: `VITE_API_BASE_URL`
   - Value: (你在第二步获得的后端地址，例如 `https://talking-skills-api.onrender.com`)
6. 点击 **Deploy site**。

---

## 🎉 完成！

现在访问 Netlify 给你分配的域名，你的全栈应用就上线了！
