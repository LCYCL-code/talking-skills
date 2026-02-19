# 如何将代码上传到 GitHub 🐙

这是一份专门为你准备的傻瓜式指南，跟着做就行！

## 第一步：准备 GitHub 仓库

1. 登录 [GitHub](https://github.com/)。
2. 点击右上角的 **+** 号，选择 **New repository**。
3. 填写仓库信息：
   - **Repository name**: `talking-skills` (或者你喜欢的名字，比如 `dont-argue`)
   - **Description**: (可选) `基于金字塔原理的智能表达训练平台`
   - **Public/Private**: 选择 Public (公开) 或 Private (私有)。
   - **Initialize this repository with**: **全部不要勾选** (不要勾选 Add a README, .gitignore, license)。因为我们本地已经准备好了。
4. 点击 **Create repository** 按钮。
5. 创建成功后，你会看到一个页面，复制那行地址，类似：
   `https://github.com/你的用户名/talking-skills.git`

## 第二步：在本地初始化并上传

在你现在的 VS Code 终端里（确保路径是 `d:\talking_skills_google`），依次执行以下命令：

### 1. 初始化 git
```powershell
git init
```

### 2. 添加所有文件
```powershell
git add .
```
*(这一步会把所有代码放入暂存区，`.gitignore` 里的文件会自动被忽略，不用担心)*

### 3. 提交第一次修改
```powershell
git commit -m "feat: first commit 🚀"
```

### 4. 关联远程仓库
将下面的 URL 换成你刚才在 GitHub 复制的那个地址：
```powershell
git remote add origin https://github.com/你的用户名/talking-skills.git
```
*(如果提示 origin 已存在，可以先运行 `git remote remove origin` 再运行上面这句)*

### 5. 推送到 GitHub
```powershell
git branch -M main
git push -u origin main
```

## 常见问题

**Q: 只有 `git push` 的时候报错说没有权限？**
A: 如果是第一次用 git，可能会弹出一个窗口让你登录 GitHub，输入你的账号密码（或者 Token）即可。

**Q: 上传后发现少了一些文件？**
A: 检查一下 `.gitignore` 文件，有些自动生成的文件（如 `node_modules`）是不应该上传的，这是正常的。

**Q: 这里写错了想重来？**
A: 删除项目根目录下的隐藏文件夹 `.git`，然后从第一步 `git init` 重新开始即可。
