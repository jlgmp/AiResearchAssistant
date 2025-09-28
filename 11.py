import asyncio
import warnings
from stagehand import Stagehand


warnings.filterwarnings("ignore", category=ResourceWarning)

async def use_stagehand():
    stagehand = None
    try:
        stagehand = Stagehand(
            env="LOCAL",
            local_browser_launch_options={"cdp_url": "http://localhost:9222"}
        )
        
        await stagehand.init()
        print("born")
        
     
        await stagehand.page.goto('https://mp.weixin.qq.com/s/z_bIwwxz3L0DWShY9jtPhg')
        title = await stagehand.page.title()
        print(f"name?: {title}")
            
       
        await stagehand.page.screenshot(path='naru.png')
      
   
        return stagehand
        
    except Exception as e:
        print(f"xiba: {e}")
        return None

async def main():
    stagehand = await use_stagehand()
    
    if stagehand:
      
        print("lets go")
        
      

# 运行主函数
if __name__ == "__main__":
    asyncio.run(main())