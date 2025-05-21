import asyncio
from recipeScraper import scrape_recipes
from productScraper import scrape_products

async def main():
    # Run recipe scraper first
    # print("Starting recipe scraping...")
    # await scrape_recipes()
    # print("Recipe scraping completed!")
    
    # Then run product scraper
    print("Starting product scraping...")
    await scrape_products()
    print("Product scraping completed!")

if __name__ == '__main__':
    asyncio.run(main())