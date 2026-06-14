"""
影刀RPA - 微信公众号文章链接批量提取脚本
适用于：风控博士沙龙公众号
作者：AI助手
日期：2026-06-14

使用方法：
1. 在影刀RPA中创建新应用
2. 添加"执行Python代码"指令
3. 将本代码粘贴进去
4. 根据实际情况调整元素选择器
"""

import json
import time
from datetime import datetime

def extract_wechat_articles():
    """
    影刀RPA微信公众号文章提取主函数
    需要在影刀中以"执行Python代码"方式运行
    """
    
    articles_data = []
    
    # ==========================================
    # 方法一：通过公众号后台"超链接"功能获取
    # ==========================================
    
    print("=" * 60)
    print("开始提取公众号文章链接")
    print("=" * 60)
    
    # 步骤1：打开公众号后台（假设已登录）
    # 影刀指令：打开网页
    # 网址：https://mp.weixin.qq.com
    
    # 步骤2：点击"新的创作" → "文章"
    # 影刀指令：点击元素(网页)
    # 目标：//span[contains(text(),'新的创作')]
    
    # 步骤3：点击编辑器"超链接"按钮
    # 影刀指令：点击元素(网页)
    # 目标：//a[@id='js_editor_insertlink']
    
    # 步骤4：点击"选择其他账号"
    # 影刀指令：点击元素(网页)
    # 目标：//a[contains(text(),'选择其他账号')]
    
    # 步骤5：搜索公众号
    # 影刀指令：填写输入框(网页)
    # 目标：//input[@placeholder='搜索公众号']
    # 内容：风控博士沙龙
    
    # 步骤6：发送回车
    # 影刀指令：键盘输入
    # 内容：{ENTER}
    
    # 步骤7：选择搜索结果中的公众号
    # 影刀指令：点击元素(网页)
    # 目标：//div[contains(@class,'account_item')][1]
    
    # 步骤8：循环翻页采集
    page = 1
    while True:
        print(f"正在采集第 {page} 页...")
        
        # 获取当前页文章列表
        # 影刀指令：获取相似元素列表(网页)
        # 目标：//ul[@id='js_link_list']/li
        # 保存到：article_elements
        
        # 遍历文章元素
        # 影刀指令：ForEach列表循环
        # 列表：article_elements
        
        # 提取文章信息
        # 影刀指令：获取元素信息(网页)
        # 目标：当前元素的标题部分
        # 保存到：title
        
        # 影刀指令：获取元素属性(网页)
        # 目标：当前元素的链接部分
        # 属性：href
        # 保存到：url
        
        # 影刀指令：获取元素信息(网页)
        # 目标：当前元素的时间部分
        # 保存到：publish_time
        
        # 添加到数据表格
        article_info = {
            "title": "文章标题",  # 从元素获取
            "url": "文章链接",     # 从元素获取
            "publish_time": "发布时间",  # 从元素获取
            "author": "斯文博士",  # 根据公众号信息
            "source": "风控博士沙龙"
        }
        articles_data.append(article_info)
        
        # 检查是否有下一页
        # 影刀指令：判断元素是否存在(网页)
        # 目标：//a[@class='btn_page_next']
        
        has_next_page = True  # 根据实际情况判断
        if not has_next_page:
            print("已到达最后一页")
            break
        
        # 点击下一页
        # 影刀指令：点击元素(网页)
        # 目标：//a[@class='btn_page_next']
        
        # 等待加载
        # 影刀指令：等待
        # 时间：3秒
        
        page += 1
        
        # 频率控制，避免触发反爬
        time.sleep(2)
    
    # 保存数据到JSON
    output_file = f"wechat_articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n采集完成！共获取 {len(articles_data)} 篇文章")
    print(f"数据已保存至：{output_file}")
    
    return articles_data


def generate_wechat_article_url(biz, mid, idx, sn):
    """
    生成微信公众号文章URL
    
    参数：
        biz: 公众号唯一标识
        mid: 消息ID
        idx: 文章位置（多篇图文中的第几篇）
        sn: 签名参数
    
    返回：
        完整的文章URL
    """
    base_url = "https://mp.weixin.qq.com/s"
    params = {
        '__biz': biz,
        'mid': mid,
        'idx': idx,
        'sn': sn
    }
    
    # 构建URL参数
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    full_url = f"{base_url}?{query_string}"
    
    return full_url


def update_website_articles_json(articles_data):
    """
    将采集到的文章数据转换为网站可用的JSON格式
    
    参数：
        articles_data: 采集到的文章列表
    
    返回：
        网站专用的articles数组JSON
    """
    
    website_articles = []
    
    for idx, article in enumerate(articles_data, 1):
        website_article = {
            "tag": "未分类",  # 需要手动分类
            "title": article.get("title", ""),
            "summary": "",  # 需要手动添加摘要
            "author": article.get("author", "斯文博士"),
            "date": article.get("publish_time", ""),
            "source": "风控博士沙龙",
            "url": article.get("url", "")
        }
        website_articles.append(website_article)
    
    # 保存为网站数据文件
    output = {
        "articles": website_articles,
        "update_time": datetime.now().isoformat(),
        "total_count": len(website_articles)
    }
    
    with open('website_articles_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("网站数据文件已生成：website_articles_data.json")
    return output


# ==========================================
# 影刀RPA可直接使用的简化版流程
# ==========================================

YINGDAO_RPA_WORKFLOW = """
【影刀RPA流程 - 微信公众号文章链接提取】

=== 前置条件 ===
1. 已安装影刀RPA（官网下载）
2. 已登录微信公众号后台（mp.weixin.qq.com）
3. Chrome浏览器已安装影刀自动化插件

=== 主流程 ===

1. 【打开网页】
   网址：https://mp.weixin.qq.com
   说明：打开公众号后台（需提前登录）

2. 【点击元素(网页)】
   目标：//span[contains(text(),'新的创作')]
   说明：展开创作菜单

3. 【点击元素(网页)】
   目标：//a[contains(text(),'文章')]
   说明：进入文章编辑页面

4. 【等待】
   时间：3秒
   说明：等待编辑器加载

5. 【点击元素(网页)】
   目标：//a[@id='js_editor_insertlink']
   说明：点击超链接按钮

6. 【等待】
   时间：2秒

7. 【点击元素(网页)】
   目标：//a[contains(text(),'选择其他账号')]
   说明：切换到选择其他账号

8. 【等待】
   时间：2秒

9. 【填写输入框(网页)】
   目标：//input[@placeholder='搜索公众号']
   内容：风控博士沙龙
   说明：输入公众号名称

10. 【键盘输入】
    内容：{ENTER}
    说明：发送回车搜索

11. 【等待】
    时间：3秒
    说明：等待搜索结果

12. 【点击元素(网页)】
    目标：//div[contains(@class,'account_item')][1]
    说明：选择第一个搜索结果

13. 【等待】
    时间：3秒
    说明：等待文章列表加载

14. 【设置变量】
    变量名：page_num
    值：1
    说明：初始化页码

15. 【循环】无限循环（带退出条件）
    
    15.1 【打印日志】
        信息：正在采集第 {page_num} 页
    
    15.2 【获取相似元素列表(网页)】
        目标：//ul[@id='js_link_list']/li
        保存到：article_list
        说明：获取当前页所有文章
    
    15.3 【ForEach列表循环】
        列表：article_list
        当前项：current_article
        
        15.3.1 【获取元素信息(网页)】
            目标：current_article → .//h4
            保存到：article_title
            说明：获取文章标题
        
        15.3.2 【获取元素属性(网页)】
            目标：current_article → .//a
            属性：href
            保存到：article_url
            说明：获取文章链接
        
        15.3.3 【获取元素信息(网页)】
            目标：current_article → .//span[@class='time']
            保存到：article_time
            说明：获取发布时间
        
        15.3.4 【写入数据表格】
            数据表格：articles_table
            行数据：[page_num, article_title, article_time, article_url]
    
    15.4 【判断元素是否存在(网页)】
        目标：//a[@class='btn_page_next' and not(contains(@class,'disabled'))]
        保存到：has_next
        说明：检查是否有下一页
    
    15.5 【If条件】
        条件：has_next 为 False
        
        15.5.1 【打印日志】
            信息：已到达最后一页，采集结束
        
        15.5.2 【退出循环】
        
        15.5.3 【Else】
            
            15.5.3.1 【点击元素(网页)】
                目标：//a[@class='btn_page_next']
                说明：点击下一页
            
            15.5.3.2 【等待】
                时间：3秒
                说明：等待下一页加载
            
            15.5.3.3 【设置变量】
                变量名：page_num
                值：page_num + 1
    
    15.6 【等待】
        时间：2秒
        说明：频率控制，避免触发反爬

16. 【导出数据表格】
    数据表格：articles_table
    文件路径：C:/Users/{用户名}/Desktop/风控博士沙龙_文章链接.xlsx
    说明：导出为Excel文件

17. 【打印日志】
    信息：采集完成！数据已保存至桌面

=== 异常处理 ===
- 每个点击操作后添加2-3秒等待
- 使用Try-Catch包裹关键操作
- 失败时截图保存

=== 注意事项 ===
1. 运行前确保已登录公众号后台
2. 不要最小化浏览器窗口
3. 保持网络稳定
4. 建议分批次采集，每批50篇左右
"""

if __name__ == "__main__":
    print(YINGDAO_RPA_WORKFLOW)
    print("\n" + "=" * 60)
    print("请将上述流程在影刀RPA中配置执行")
    print("=" * 60)
