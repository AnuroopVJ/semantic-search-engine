import requests
import bs4
from sqlalchemy import create_engine, Table, Column, String, MetaData
import time
import random


# Target URL and crawling parameters
target_url = "https://finance.yahoo.com/"
target_robot_txt = "https://finance.yahoo.com/robots.txt"
rate_limit = 5
response = requests.get(target_robot_txt)
disallow_rules = ['/wiki/Wikipedia:Contents','wiki/Wikipedia:About','wiki/Wikipedia:Community_portal','wiki/Wikipedia:Help','wiki/Wikipedia:Contact_us','wiki/Wikipedia:Current_events']
if response.status_code == 200:
    info = response.text
    print("robots.txt file found")
    if "User-agent: *" in info:
        i_lines = info.splitlines()
        capture_disallow = False
        for line in i_lines:
            if line.startswith("User-agent: *"):
                capture_disallow = True
            elif line.startswith("User-agent"):
                capture_disallow = False
            elif capture_disallow and line.startswith("Disallow"):
                disallow_rules.append(line.split(":")[1].strip())

        print("Disallow rules for 'User-agent: *':")
        print(disallow_rules)
else:
    print("robots.txt file not found")
    print(f"Status code: {response.status_code}")
    print("--------------------------------------------STOP-----------------------------------------------")


sites_to_visit = [target_url]
max_crawl = 55
data = []  # Will store dictionaries with url, title, description

# Set up database
engine = create_engine("sqlite:///C:\\Users\\neela\Desktop\\Miscellaneous\\File_scanner\\Vector_search\\crawls.db", echo=True)
metadata = MetaData()

urls_table = Table(
    'crawlsTB', metadata,
    Column('urls', String, primary_key=True),
    Column('title', String),
    Column('description', String) 
)
# Create the table
metadata.create_all(engine)

def fetch_data_crawler():
    site_count = 0
    global data
    global sites_to_visit
    
    # Keep track of visited URLs to avoid duplicates
    visited_urls = set()
    
    print(f"Starting crawler with target: {target_url}")
    
    while sites_to_visit and site_count < max_crawl:
        current_url = sites_to_visit.pop(0)
        
        # Extract the path part of the current URL
        current_path = requests.utils.urlparse(current_url).path
        
        # Skip if already visited
        if current_url in visited_urls:
            continue
        
        # Skip if the path matches any disallow rule, but allow the target_url
        if current_url != target_url and any(current_path.startswith(rule) for rule in disallow_rules):
            print(f"Skipping disallowed URL: {current_url}")
            continue
        
        visited_urls.add(current_url)
        print(f"Crawling: {current_url}")

        delay = 5 + random.random() * 3
        print(f"Waiting {delay:.2f} seconds before next request...")
        time.sleep(delay)
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(current_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"Failed to fetch {current_url}: Status code {response.status_code}")
                continue
                
            content = bs4.BeautifulSoup(response.content, "html.parser")
            
            # Extract page title
            if content.find("title"):
                title = content.find("title").text
            else:
                title = "No title found"
            print(f"Title found: {title}")
            
            # Extract page description
            if content.find("p"):
                description = content.find("p").text.strip()
                print(f"Found paras: {description}")
            else:
                description = ""
            
            # Store the current page data
            page_data = {
                "urls": current_url,
                "title": title,
                "description": description
            }
            data.append(page_data)
            
            # Find links on the page
            links_found = 0
            target_domain = target_url.split("//")[-1].split("/")[0]
            
            for link in content.find_all("a", href=True):
                href = link["href"]
                
                # Handle relative URLs
                if not href.startswith("http"):
                    absolute_url = requests.compat.urljoin(current_url, href)
                else:
                    absolute_url = href
                
                # Only add URLs from the same domain that haven't been visited or queued
                current_domain = absolute_url.split("//")[-1].split("/")[0]
                if (target_domain in current_domain and 
                    absolute_url not in visited_urls and 
                    absolute_url not in sites_to_visit):
                    sites_to_visit.append(absolute_url)
                    links_found += 1
            
            site_count += 1
            print(f"Found {links_found} new links on {current_url}")
            print(f"Crawled {site_count}/{max_crawl} sites")
            
        except Exception as e:
            print(f"Error crawling {current_url}: {e}")
    
    print(f"Crawling complete. Found {len(data)} URLs.")
    
    # Add URLs to database
    if data:
        with engine.connect() as conn:
            for item in data:
                try:
                    # Use SQLite's "INSERT OR IGNORE" to skip duplicates silently
                    conn.execute(urls_table.insert().prefix_with('OR IGNORE'), item)
                except Exception as e:
                    print(f"Error inserting {item['urls']}: {e}")
            conn.commit()
            print(f"Added URLs to crawls.db database (duplicates ignored)")
    else:
        print("No URLs to add to database")

# Run the crawler
if __name__ == "__main__":
    fetch_data_crawler()
    print("Crawler finished execution")