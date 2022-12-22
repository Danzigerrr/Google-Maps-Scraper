from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Make browser open in background
options = webdriver.ChromeOptions()
options.add_argument('headless')

# Create the webdriver object
driver = webdriver.Chrome(ChromeDriverManager().install())
from scrapfly import ScrapflyClient, ScrapeConfig

scrapfly = ScrapflyClient(key="YOUR_SCRAPFLY_KEY", max_concurrency=2)
script = """
function waitCss(selector, n=1, require=false, timeout=5000) {
  console.log(selector, n, require, timeout);
  var start = Date.now();
  while (Date.now() - start < timeout){
  	if (document.querySelectorAll(selector).length >= n){
      return document.querySelectorAll(selector);
    }
  }
  if (require){
      throw new Error(`selector "${selector}" timed out in ${Date.now() - start} ms`);
  } else {
      return document.querySelectorAll(selector);
  }
}
"""
def search(query):
    result = scrapfly.scrape(
        ScrapeConfig(
            url="https://www.google.com/maps/search/" + query.replace(" ", "+")+"/?hl=en",
            render_js=True,
            js=script,
        )
    )
    urls = result.scrape_result['browser_data']['javascript_evaluation_result']
    return urls
print(search("louvre museum in paris"))
print(search("mcdonalds in paris"))
