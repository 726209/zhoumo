# ZhouMo Cello — 部署说明

这是无需安装前端依赖的静态网站。`index.html` 是入口；图片和视频放在 `assets/`。网站使用相对路径，可用于 GitHub Pages 项目子目录或 Cloudflare Pages 根域名。

## 当前状态

当前按要求先交付本地网站，未公开发布。本文件为日后部署提供配置；实际公开地址以 GitHub / Cloudflare 显示的成功部署结果为准。无需把密码、Token 或密钥写进网站文件。

## 发布前编辑

- 网站使用英文名 ZhouMo，乐器为 Cello，不设置个人简介。
- 后续如添加曲目、演出地点、时间或联系方式，仅填写已核实的内容。
- 如使用 Google Drive 视频，确认分享权限允许“知道链接的任何人”查看，并用无痕窗口测试。

## 本地预览与打包

在本项目目录执行：

```sh
python3 scripts/build.py
python3 -m http.server 8000 --directory site-dist
```

在浏览器打开 `http://localhost:8000`。`site-dist/` 只包含网站公开文件，不会上传本说明、部署脚本、工作流或本地配置。它也会检查素材是否超过 Cloudflare 单文件限制。

## 方案 A：GitHub Pages

1. 创建一个新的 GitHub 仓库，例如 `music-portfolio`。免费个人账号使用公开仓库即可启用 Pages；公开仓库内的源文件和素材也将公开。
2. 将本项目目录内容放到仓库根目录，包括 `.github/workflows/pages.yml`，默认分支设为 `main`。大视频建议通过 Git 推送，而非网页逐个上传。
3. 在仓库 **Settings → Pages → Build and deployment → Source** 中选择 **GitHub Actions**。
4. 推送 `main` 分支，或在 **Actions → Publish portfolio to GitHub Pages → Run workflow** 手动运行。
5. 等待工作流成功，在 **Deploy to GitHub Pages** 的部署结果或仓库 **Settings → Pages** 获取真实网站地址。

已提供的工作流会先生成 `site-dist/`，再发布静态内容。以后推送 `main` 会自动更新。若使用其他默认分支，请修改工作流里的 `branches: [main]`。

仓库首次连接时也可以在项目目录执行以下命令；将最后一行的仓库地址替换为 GitHub 创建后显示的实际地址：

```sh
git init -b main
git add .
git commit -m "Create music portfolio"
git remote add origin <实际仓库 Git 地址>
git push -u origin main
```

## 方案 B：Cloudflare Pages 连接 GitHub（持续更新）

在 Cloudflare 控制台创建 **Pages** 项目，连接上述 GitHub 仓库，然后使用：

| 设置 | 值 |
| --- | --- |
| Production branch | `main` |
| Framework preset | `None` |
| Build command | `python3 scripts/build.py` |
| Build output directory | `site-dist` |
| Root directory | 仓库根目录（留空） |

部署完成后，Cloudflare 会提供实际的 `pages.dev` 地址。以后推送 GitHub 会触发更新。`_headers` 会随打包进入输出目录，在 Cloudflare 上启用安全响应头；GitHub Pages 会忽略该配置。

## 方案 C：Cloudflare Pages 直接上传（最快）

1. 执行 `python3 scripts/build.py`。
2. 在 Cloudflare **Workers & Pages** 中创建 **Pages → Direct Upload** 项目。
3. 上传整个 `site-dist/` 文件夹，或上传其中内容组成的 ZIP；确保 `index.html` 位于上传内容的顶层。
4. 点击部署并等待成功，再复制控制台返回的公开地址。

注意：Cloudflare 的 Direct Upload 项目之后不能直接改为 Git 集成；如果希望每次更新自动发布，优先选择方案 B。

也可在自己登录 Cloudflare 后使用命令行：

```sh
npx wrangler@4 login
npx wrangler@4 pages project create music-portfolio --production-branch main
python3 scripts/build.py
npx wrangler@4 pages deploy site-dist --project-name music-portfolio --branch main
```

项目名可按账号实际情况修改；已有项目应复用，不要重复创建。命令行首次使用需要联网并安装 Wrangler。

## 视频与兼容性

Cloudflare Pages 单个文件最大为 25 MiB。本网站本地提供 75 秒有声演出选段和 8 秒静音预览，所有素材均低于此限制；10 分 31 秒的完整演出通过 Google Drive 播放，无需将原始大视频放进仓库。

如果当前网络或浏览器无法播放本地视频，访客可以改为打开提供的 [Google Drive 原视频](https://drive.google.com/file/d/1SNV6oNJskdxrOYUmpqKmk10OKzdtOEuN/view?usp=drivesdk)。Drive 预览可能受文件权限、Google 的处理状态、地区网络或第三方 Cookie 设置影响，应始终保留新窗口打开链接。

## 官方资料

- [GitHub Pages 自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Cloudflare Pages 直接上传](https://developers.cloudflare.com/pages/get-started/direct-upload/)
- [Cloudflare Pages 文件大小限制](https://developers.cloudflare.com/pages/platform/limits/)

以上部署方式与限制于 2026 年 11 月 19 日按官方文档核对。
