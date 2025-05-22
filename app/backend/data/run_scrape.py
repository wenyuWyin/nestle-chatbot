import asyncio
from app.backend.data.recipe_scraper import scrape_recipes
from app.backend.data.product_scraper import scrape_products

async def main():
    # Run recipe scraper first
    print("Starting recipe scraping...")
    await scrape_recipes()
    print("Recipe scraping completed!")
    
    # Then run product scraper
    print("Starting product scraping...")
    await scrape_products()
    print("Product scraping completed!")

if __name__ == '__main__':
    asyncio.run(main())