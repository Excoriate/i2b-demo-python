import httpx
import json
import re
import unicodedata
from typing import List, Dict, Any, Tuple

from ..models.job_offer import JobOffer, Skill
from ..db.session import get_db
from ..core.config import settings # Although not used directly here, good practice

# URL provided by the user
JOB_OFFERS_URL = "https://www.i2btech.com/_next/data/xcVkS-YDlttXeQubs5JFO/es/conoce-i2b/ofertas-laborales.json?wordpressNode=conoce-i2b&wordpressNode=ofertas-laborales"

def slugify(value: str) -> str:
    """
    Basic slugify function to create a safe ID component.
    Converts to lowercase, removes non-word characters (alphanumeric + underscore),
    replaces whitespace with hyphens.
    """
    value = unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

async def fetch_and_store_job_offers() -> Tuple[int, int]:
    """
    Fetches job offers from the specified URL, parses them,
    and stores new offers in CouchDB.

    Returns:
        Tuple[int, int]: Number of offers processed, Number of new offers added.
    """
    processed_count = 0
    added_count = 0

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'dnt': '1', # Do Not Track
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'purpose': 'prefetch',
        'referer': 'https://www.i2btech.com/conoce-i2b/ofertas-laborales',
        'sec-ch-ua': '"Not:A-Brand";v="24", "Chromium";v="134"', # Example, might need adjustment if server validates strictly
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"', # Example platform
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1', # Global Privacy Control
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'x-nextjs-data': '1', # Specific to Next.js sites
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(JOB_OFFERS_URL, timeout=30.0, headers=headers)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()

    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
        return processed_count, added_count
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
        return processed_count, added_count

    try:
        # Navigate through the nested structure to get the items list
        items = data.get("pageProps", {}).get("__TEMPLATE_QUERY_DATA__", {}).get("page", {}).get("acf_ofertasLaborales", {}).get("groupJobOpenings", {}).get("items", [])
        if not isinstance(items, list):
            print("Error: Job items data is not a list or not found at the expected path.")
            return processed_count, added_count

        processed_count = len(items)
        if processed_count == 0:
            print("No job offers found in the response data.")
            return processed_count, added_count

        # Get CouchDB database instance
        db = get_db() # This might raise ConnectionError if DB is unavailable

        for item in items:
            try:
                # Map skills
                skills_data = item.get("skills", [])
                skills_list = [Skill(title=skill.get("title", "N/A")) for skill in skills_data if isinstance(skill, dict)]

                # Create JobOffer model instance
                job_data = {
                    "title": item.get("title", "N/A"),
                    "hour": item.get("hour"),
                    "modo": item.get("modo"),
                    "time": item.get("time"),
                    "detail": item.get("detail"),
                    "skills": skills_list,
                    "location": item.get("location")
                }
                job_offer = JobOffer(**job_data)

                # Create a unique ID for CouchDB (e.g., based on title and location)
                # Ensure title and location exist before creating slug
                title_slug = slugify(job_offer.title)
                location_slug = slugify(job_offer.location or "unknown")
                doc_id = f"job:{title_slug}:{location_slug}"

                # Check if the document already exists
                if not db.exists(doc_id):
                    # Save the new job offer to CouchDB
                    # Convert Pydantic model to dict for saving
                    job_offer_dict = job_offer.model_dump(mode='json')
                    db.save({'_id': doc_id, **job_offer_dict})
                    added_count += 1
                    print(f"Added job offer: {doc_id}")
                # else:
                #     print(f"Job offer already exists: {doc_id}") # Optional: Log skipped offers

            except Exception as e: # Catch errors during processing/saving individual items
                print(f"Error processing or saving item '{item.get('title', 'N/A')}': {e}")
                continue # Continue with the next item

    except ConnectionError as e:
        print(f"Database connection error: {e}")
    except KeyError as e:
        print(f"Error accessing expected key in JSON data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")

    print(f"Finished processing. Processed: {processed_count}, Added: {added_count}")
    return processed_count, added_count
