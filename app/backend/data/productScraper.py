import asyncio
import re
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
from crawlee.storages import Dataset
from datetime import datetime, timezone


async def scrape_category(context: PlaywrightCrawlingContext) -> dict:
    brand_category = {}
    
    first_menu_container = context.page.locator('div.sub-menu-container-inner.coh-ce-3f13c9f3').first
    
    # Get all top-level category items
    category_items = await first_menu_container.locator('> ul > li').all()
    
    for category_item in category_items:
        # Extract category name from span
        category_name = await category_item.locator('span').first.text_content()
        category_name = category_name.strip()
        context.log.info(f'Retrieve category: {category_name}')
        
        # Initialize category entry
        brand_category[category_name] = []
        
        # Get all brand links in submenu
        brand_links = await category_item.locator(
            'div.sub-sub-menu-container a'
        ).all()
        
        for link in brand_links:
            brand_name = await link.locator('span.menu-link-3-level').text_content()
            brand_url = await link.get_attribute('href')
            context.log.info(f'Retrieve brand + url: {brand_name}: {brand_url}')
            
            if brand_name and brand_url:
                brand_category[category_name].append({
                    'name': brand_name.strip(),
                    'url': brand_url,
                    'scraped_at': datetime.now(timezone.utc).isoformat()
                })

    return brand_category


async def scrape_products() -> None:
    crawler = PlaywrightCrawler(
        headless=True,  # Set to True for production
        max_requests_per_crawl=50,  # Adjust as needed
    )
    dataset = await Dataset.open(name='products')

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        url = context.request.url
        context.log.info(f'Processing {url}')
        if context.request.label == 'PRODUCTS':
            pass
            #TODO scrape products info for each brand
            # may have same link
            # use #products to locate products -> href to different page -> list out all items 

            # nescafe, hagen-das, pet, water, natural bounty,  different url
            # drumstick?, infant, 
        else:
            brand_category = await scrape_category(context)
        
            # Save to dataset
            await dataset.push_data(brand_category)
            
            # # Enqueue all brand links
            # all_brands = [
            #     brand['url'] 
            #     for brands in brand_category.values() 
            #     for brand in brands
            #     if 'nestle' in brand['url'].lower()  # Only Nestle brands
            # ]
            
            # await context.enqueue_links(
            #     urls=all_brands,
            #     label='PRODUCTS'
            # )
            
            # await context.enqueue_links(
            #     selector='div.coh-container.sub-menu-container-inner.coh-ce-3f13c9f3 a[href]',
            #     label='PRODUCTS'
            # )
            
        

    # Start with the main recipes page
    await crawler.run([
        'https://www.madewithnestle.ca',
    ])

if __name__ == '__main__':
    asyncio.run(scrape_products())