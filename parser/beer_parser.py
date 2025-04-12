import asyncio
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import lxml

"""
Собираем данные о названии, стоимости (скидке и основной цены),  
"""

async def run(url):
    ua = UserAgent()
    random_ua = ua.random
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=random_ua)
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_selector('.subcategory-or-type__products')
        content = await page.content()
        # Анализируем страницу с помощью BeautifulSoup
        soup = BeautifulSoup(content, 'lxml')
        for product in soup.find_all('div', class_='product-item'):
            title = product.find('h2', class_='product-title').get_text(strip=True)
            price = product.find('span', class_='price').get_text(strip=True)
            print(f"Продукт: {title}, Цена: {price}")
        await browser.close()

