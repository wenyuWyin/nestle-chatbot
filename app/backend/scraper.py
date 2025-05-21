import asyncio
import re
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
from datetime import datetime, timezone

async def main() -> None:
    crawler = PlaywrightCrawler(
        headless=True,  # Set to True for production
        max_requests_per_crawl=3,  # Adjust as needed
    )

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        url = context.request.url
        context.log.info(f'Processing {url}')

        if context.request.label == 'DETAIL':  # Recipe detail page
            # Extract basic info
            title = await context.page.locator('h1.coh-heading').text_content()
            context.log.info(f'Processing {title.strip()}')
            recipe_data = {'title': title.strip()}

            selectors = {
                'description': 'div.display-info p.coh-paragraph',
                'prep_time': 'span[class*="prep-time-value"]',
                'cook_time': 'span[class*="cook-time-value"]',
                'total_time': 'span[class*="total-time-value"]',
                'servings': 'span[class*="serving-value"]',
                'difficulty': 'span[class*="skill-level-value"]'
            }
            
            for field, selector in selectors.items():
                locator = context.page.locator(selector)
                content = await locator.text_content() if await locator.count() > 0 else None
                # Remove special chars
                content = re.sub(r'[.\n⇆]', '', content) if content else None
                # Collapse multiple spaces
                recipe_data[field] = re.sub(r'\s+', ' ', content).strip() if content else None
                context.log.info(f'Get {field}: {recipe_data[field]}')
            
            # Extract ingredients
            ingredients = []
            ingredient_items = await context.page.locator('div.field--name-field-ingredient-fullname.field__item').all()
            for item in ingredient_items:
                if await item.locator('a').count() > 0:
                    ingredient = await item.locator('a').text_content()
                else:
                    ingredient = await item.text_content()
                context.log.info(ingredient)
                ingredients.append(ingredient.strip())
            recipe_data['ingredients'] = ingredients
            
            # Extract preparation steps #TODO separate steps and tips
            steps = []
            step_elements = await context.page.locator('div.recipe-content p.coh-paragraph').all()
            for step in step_elements:
                step_text = await step.text_content()
                context.log.info(step_text)
                steps.append(step_text.strip())
            recipe_data['instructions'] = steps
            
            # Extract recipe tags
            tags = []
            tag_items = await context.page.locator('div.coh-style-recipe-tags-button').all()
            for item in tag_items:
                tag = await item.text_content()
                context.log.info(tag)
                tags.append(tag.strip())
            recipe_data['tags'] = tags
            
            # Add metadata
            recipe_data['url'] = url
            recipe_data['scraped_at'] = datetime.now(timezone.utc).isoformat()
            
        #     await context.push_data(recipe_data)
        #     context.log.info(f'Successfully scraped: {title}')

        else:  # Main page or category page
            # Enqueue recipe links
            await context.enqueue_links(
                selector='a[href*="/recipe/"]',
                label='DETAIL'
            )

    # Start with the main recipes page
    await crawler.run(['https://www.madewithnestle.ca/recipes'])

if __name__ == '__main__':
    asyncio.run(main())