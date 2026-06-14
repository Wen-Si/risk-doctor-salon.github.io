# 风控博士沙龙 - 微信公众号文章链接RPA提取方案

## 方案概述

本方案使用**影刀RPA**（推荐）或**Python + mitmproxy**实现自动化获取"风控博士沙龙"微信公众号所有文章的永久链接。

## 方案一：影刀RPA（推荐，零代码）

### 前置条件

1. Windows电脑
2. 安装影刀RPA（官网：https://www.yingdao.com）
3. 安装Chrome浏览器
4. 已登录微信公众号后台（mp.weixin.qq.com）

### 方法一：通过公众号后台"超链接"功能获取（推荐）

#### 操作步骤

1. **登录公众号后台**
   - 打开浏览器，访问 https://mp.weixin.qq.com
   - 扫码登录公众号后台

2. **进入文章编辑页面**
   - 点击左侧菜单"新的创作" → "文章"
   - 进入图文编辑页面

3. **打开超链接弹窗**
   - 点击编辑器顶部工具栏的"超链接"按钮
   - 在弹窗中点击"选择其他账号"

4. **搜索目标公众号**
   - 在搜索框输入：风控博士沙龙
   - 选择搜索结果中的公众号

5. **影刀RPA自动化采集**

创建影刀应用，使用以下指令流程：

```
【启动参数】
- 公众号名称：风控博士沙龙
- 采集数量：全部（或指定数量）

【流程步骤】
1. 打开网页
   - 网址：mp.weixin.qq.com（已登录状态）

2. 点击元素(网页)
   - 目标："新的创作"菜单

3. 点击元素(网页)
   - 目标："文章"选项

4. 等待网页加载
   - 等待时间：3秒

5. 点击元素(网页)
   - 目标：编辑器"超链接"按钮

6. 等待网页加载
   - 等待时间：2秒

7. 点击元素(网页)
   - 目标："选择其他账号"按钮

8. 等待网页加载
   - 等待时间：2秒

9. 填写输入框(网页)
   - 目标：搜索框
   - 内容：风控博士沙龙

10. 键盘输入
    - 发送回车键

11. 等待网页加载
    - 等待时间：3秒

12. 点击元素(网页)
    - 目标：搜索结果中的公众号

13. 等待网页加载
    - 等待时间：3秒

14. 【循环】翻页采集
    
    14.1 批量数据抓取(网页)
        - 抓取目标：文章列表中的标题、链接、发布时间
        - 保存至数据表格
    
    14.2 判断元素是否存在(网页)
        - 目标："下一页"按钮
        - 如果存在：点击"下一页"，等待3秒，继续循环
        - 如果不存在：结束循环

15. 导出数据表格
    - 格式：Excel
    - 文件名：风控博士沙龙_文章列表.xlsx
    - 包含字段：序号、文章标题、发布时间、文章链接
```

### 方法二：通过PC微信客户端获取

#### 操作步骤

1. **打开PC微信**
   - 确保已登录微信

2. **搜索公众号**
   - 点击搜索框
   - 输入：风控博士沙龙
   - 选择公众号

3. **进入文章列表**
   - 点击"文章"标签

4. **影刀RPA自动化采集**

```
【流程步骤】
1. 获取窗口对象
   - 窗口标题：微信

2. 点击元素(win)
   - 目标：搜索框

3. 键盘输入
   - 内容：风控博士沙龙

4. 等待
   - 时间：2秒

5. 键盘输入
   - 发送回车键

6. 等待
   - 时间：3秒

7. 点击元素(win)
   - 目标：公众号结果

8. 等待
   - 时间：3秒

9. 点击元素(win)
   - 目标："文章"标签

10. 等待
    - 时间：3秒

11. 【无限循环】滚动加载所有文章
    
    11.1 获取相似元素列表(win)
        - 目标：文章标题元素
        - 保存到：article_list
    
    11.2 设置变量
        - 变量名：last_count
        - 值：article_list的长度
    
    11.3 滚动鼠标滚轮
        - 方向：向下
        - 次数：10
    
    11.4 等待
        - 时间：2秒
    
    11.5 获取相似元素列表(win)
        - 目标：文章标题元素
        - 保存到：new_article_list
    
    11.6 IF条件
        - 如果 new_article_list长度 == last_count
        - 则：退出循环

12. 回到顶部
    - 键盘输入：{HOME}

13. 【ForEach循环】遍历所有文章
    
    13.1 设置变量
        - 当前文章元素 = loop_item
    
    13.2 【无限循环】确保元素可见
        
        13.2.1 Try
            - 点击元素(win)：当前文章元素
            - 如果成功：退出循环
        
        13.2.2 Catch
            - 滚动鼠标滚轮：向下3次
            - 等待：1秒
    
    13.3 等待
        - 时间：3秒
    
    13.4 获取元素信息(win)
        - 目标：文章标题
        - 保存到：title
    
    13.5 获取元素信息(win)
        - 目标：发布时间
        - 保存到：publish_time
    
    13.6 点击元素(win)
        - 目标：右上角"..."按钮
    
    13.7 等待
        - 时间：1秒
    
    13.8 点击元素(win)
        - 目标："复制链接"选项
    
    13.9 获取剪贴板内容
        - 保存到：article_url
    
    13.10 写入内容至Excel工作表
        - 行数据：[序号, title, publish_time, article_url]
    
    13.11 键盘输入
        - 发送ESC键（关闭弹窗）
    
    13.12 键盘输入
        - 发送ALT+LEFT（返回上一页）
    
    13.13 等待
        - 时间：2秒

14. 保存Excel文件
    - 文件名：风控博士沙龙_文章链接.xlsx
```

---

## 方案二：Python + mitmproxy（技术方案）

### 环境准备

```bash
pip install mitmproxy requests
```

### 步骤1：配置mitmproxy抓包

创建 `mitm_script.py`：

```python
from mitmproxy import http
import json
import re

class WeChatArticleExtractor:
    def __init__(self):
        self.articles = []
    
    def response(self, flow: http.HTTPFlow):
        # 拦截公众号文章列表请求
        if "mp.weixin.qq.com/mp/profile_ext" in flow.request.url:
            try:
                text = flow.response.text
                # 提取msgList数据
                msg_list_match = re.findall(r"var msgList = '(.*?)';", text)
                if msg_list_match:
                    msg_list_str = msg_list_match[0]
                    msg_list_str = msg_list_str.replace('&quot;', '"')
                    msg_list_str = msg_list_str.replace('&nbsp;', ' ')
                    msg_list_str = msg_list_str.replace('&amp;', '&')
                    msg_list_str = msg_list_str.replace('\\/', '/')
                    
                    data = json.loads(msg_list_str)
                    
                    for item in data.get('list', []):
                        app_msg = item.get('app_msg_ext_info', {})
                        comm_msg = item.get('comm_msg_info', {})
                        
                        article = {
                            'title': app_msg.get('title', ''),
                            'url': app_msg.get('content_url', ''),
                            'publish_time': comm_msg.get('datetime', ''),
                            'author': app_msg.get('author', ''),
                            'digest': app_msg.get('digest', '')
                        }
                        
                        if article['url']:
                            self.articles.append(article)
                            print(f"获取文章: {article['title']}")
                    
                    # 保存到文件
                    with open('articles.json', 'w', encoding='utf-8') as f:
                        json.dump(self.articles, f, ensure_ascii=False, indent=2)
                        
            except Exception as e:
                print(f"解析错误: {e}")

addons = [WeChatArticleExtractor()]
```

### 步骤2：启动mitmproxy

```bash
mitmweb -s mitm_script.py --listen-port 8080
```

### 步骤3：配置系统代理

1. 打开系统设置 → 网络 → 代理
2. 设置HTTP代理：127.0.0.1:8080
3. 安装mitmproxy证书（访问 http://mitm.it 下载安装）

### 步骤4：使用影刀自动打开公众号

```python
# 影刀Python代码块
import subprocess
import time

# 打开PC微信并搜索公众号
subprocess.Popen(["C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"])
time.sleep(5)

# 后续使用影刀的win元素操作
# 搜索"风控博士沙龙"并进入文章列表
```

### 步骤5：获取文章列表URL

公众号文章列表页URL格式：
```
https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={BIZ值}&scene=124#wechat_redirect
```

**获取BIZ值的方法：**
1. 打开任意一篇公众号文章
2. 复制文章链接
3. 从链接中提取 `__biz=` 后面的值

---

## 数据导出格式

采集完成后，数据应导出为以下格式：

| 序号 | 文章标题 | 发布时间 | 文章链接 | 作者 | 分类 |
|------|---------|---------|---------|------|------|
| 1 | 金融危机下金融从业人员心理健康... | 2024-03-28 | https://mp.weixin.qq.com/s/... | 张天源 | 心理健康 |
| 2 | 风险经理是干什么的？ | 2024-01-15 | https://mp.weixin.qq.com/s/... | Aaron Brown | 职业解读 |

---

## 注意事项

1. **频率控制**
   - 每次操作间隔至少2-3秒
   - 避免触发微信反爬机制
   - 建议分批次采集，每批不超过50篇

2. **登录状态**
   - 确保公众号后台或微信客户端保持登录
   - Cookie过期需要重新登录

3. **链接有效性**
   - 获取的链接为永久链接
   - 如果文章被删除，链接会失效

4. **法律合规**
   - 仅采集自己运营的公众号内容
   - 遵守微信公众平台使用规范

---

## 更新网站链接

获取到真实链接后，更新 `index.html` 中的 `articles` 数组：

```javascript
const articles = [
    {
        tag: "心理健康",
        title: "金融危机下金融从业人员心理健康、相关影响和应对措施",
        summary: "基于风险视角下的思考...",
        author: "张天源",
        date: "2024-03-28",
        source: "《上财风险管理论坛》2024年第1期",
        url: "https://mp.weixin.qq.com/s/XXXXXXXXXXXX"  // 替换为真实链接
    },
    // ... 其他文章
];
```

---

## 推荐工具下载

- **影刀RPA**：https://www.yingdao.com
- **mitmproxy**：https://mitmproxy.org
- **Chrome浏览器**：https://www.google.com/chrome

---

## 技术支持

如遇问题，可参考：
- 影刀官方文档：https://www.yingdao.com/yddoc
- 影刀开发者社区：https://www.yingdao.com/community
