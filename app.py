# app.py
import os
import asyncio


from first_demo import download_pdf_properly
from quart import Quart, render_template,request, send_file
from stagehand import Stagehand
import requests

app = Quart(__name__)
stagehand = None


@app.before_serving
async def startup():
    global stagehand
    stagehand = Stagehand(
        model_name="openai/gpt-4.1",
        env="LOCAL",
        model_api_key=os.getenv("OPENAI_API_KEY"),
        local_browser_launch_options={"cdp_url": "http://localhost:9222"}
    )
    await stagehand.init()
    if stagehand.page is None:
        print("stagehand.page 初始化失败")
    else:
        print("stagehand.page 初始化成功")

def download_pdf_from_url(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"PDF saved: {save_path}")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False

# ---------------------------
# 异步 Stagehand 使用函数
# ---------------------------
async def use_stagehand(keyword: str, stagehand):
    try:
        if stagehand.page is None:
            print("stagehand.page is None! Cannot continue.")
            return None

        save_path = "static/downloaded_document.pdf"

    

       
        await stagehand.page.goto("https://pubmed.ncbi.nlm.nih.gov/")
        await stagehand.page.act(f"type {keyword} into the search box")
        await stagehand.page.act("click the Search button")
        await asyncio.sleep(2)

        results = await stagehand.page.observe("click the Download PDF button with a fire icon")
        if results:
            await stagehand.page.act(results[0])
            current_url = stagehand.page.url
            print(f"URL: {current_url}")
            if current_url.endswith(".pdf"):
                pdf_url = current_url
                download_pdf_from_url(pdf_url, save_path)
                return save_path
            else:

                await asyncio.sleep(5)
                await stagehand.page.act("click the DOWNLOAD PDF button")
                await asyncio.sleep(5)
                current_url = stagehand.page.url
                print(f"URL: {current_url}")
                download_pdf_properly(current_url, save_path)
                return save_path

            
    except Exception as e:
        print(f"Stagehand error: {e}")
        return None


@app.route("/")
async def index():
    return await render_template("index.html")

@app.route("/search", methods=["POST"])
async def search():
    form = await request.form
    keyword = form.get("keyword")
    if not keyword:
        return "请输入关键词"

    # 直接 await use_stagehand，使用同一事件循环
    save_path = await use_stagehand(keyword, stagehand)
    if save_path:
        return '<a href="/download">下载 PDF</a>'
    else:
        return "搜索或下载失败"

@app.route("/download")
async def download():
    return await send_file("static/downloaded_document.pdf", as_attachment=True)


if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(host="0.0.0.0", port=5000)
