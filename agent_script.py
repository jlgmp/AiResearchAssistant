import asyncio
import warnings
import os
from stagehand import Stagehand
import playwright
import json
import requests
import urllib.request
import urllib.error

def download_pdf_properly(url, save_path):
    try:
        response = requests.get(url,stream=True)
        response.raise_for_status()

        content_type = response.headers.get('content-type', '')
        print(f"type: {content_type}")
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"downloaded: {save_path}")
        
        # 验证文件
        verify_pdf(save_path)
        
        return True
        
    except Exception as e:
        print(f"fail: {e}")
        return False

def verify_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            header = file.read(4)
            if header == b'%PDF':
                print("PDF")
            else:
                print("Not PDF")
                print(f"name: {header}")
    except Exception as e:
        print(f"fail: {e}")


async def use_stagehand(keyword: str,stagehand) :
    try:
        

        save_path = "downloaded_document.pdf"
        await stagehand.page.goto("https://pubmed.ncbi.nlm.nih.gov/")

        await stagehand.page.act(f"type {keyword} into the search box")
        await stagehand.page.act("click the Search button")
        await asyncio.sleep(2)

        results = await stagehand.page.observe("click the Download PDF button with a fire icon")

        if results :

            await stagehand.page.act(results[0])
            await asyncio.sleep(5)
            await stagehand.page.act("click the DOWNLOAD PDF button")
            await asyncio.sleep(5)
            current_url = stagehand.page.url
            print(f"URL: {current_url}")
            download_pdf_properly(current_url, save_path)
      
   
        return save_path
        
    except Exception as e:
        print(f"xiba: {e}")
        return None

