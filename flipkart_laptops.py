from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

d = {
    'title': [], 'price': [], 'rating': [], 'link': [], 'img': [], 'scraped_at': [],
    'off': [], 'original_price': [], 'discount': [],
    "Processor": [], "Generation": [],
    "RAM Capacity": [], "RAM Type": [],
    "OS Name": [], "OS Version": [],
    "Storage": [], "Display": [], "Software": [], "Warranty": []
}

for files in os.listdir("data"):
    try:
        with open(os.path.join("data", files), "r", encoding="utf-8") as f:
            html_doc = f.read()
            soup = BeautifulSoup(html_doc, "html.parser")

            # Title
            t = soup.find("div", class_="KzDlHZ")
            ttle = t.get_text().strip() if t else "null"

            # Price
            p = soup.find("div", class_="_4b5DiR")
            price = p.get_text().strip() if p else "null"

            # Rating
            r = soup.find("div", class_="XQDdHH")
            rating = r.get_text().strip() if r else "null"

            # Link
            l = soup.find("a", href=True)
            link = "http://flipkart.com/" + l['href'] if l else "null"

            # Image
            im = soup.find("img", class_="_0CSTHy")
            img = im.get("src") if im else "no image"

            # Offer
            of = soup.find("div", class_="UkUFwK")
            off = of.get_text().strip() if of else "null"

            # Original price
            op = soup.find("div", class_="yRaY8j ZYYwLA")
            original_price = op.get_text().strip() if op else "null"

            # Discount calculation
            def clean_price(val):
                if val == "null":
                    return None
                return int(val.replace("₹", "").replace(",", "").strip())

            price_val = clean_price(price)
            original_val = clean_price(original_price)
            discount = original_val - price_val if price_val and original_val else "null"

            # Specs
            items = [li.get_text(strip=True) for li in soup.find_all("li", class_="J+igdf")]

            # Processor + Generation
            processor_text = items[0].replace("Processor", "").strip()
            if "(" in processor_text:
                processor, generation = processor_text.split("(")
                processor = processor.strip()
                generation = generation.replace(")", "").strip()
            else:
                processor, generation = processor_text, ""

            # RAM split
            ram_parts = items[1].split()
            ram_capacity = " ".join(ram_parts[0:2])   # "16 GB"
            ram_type = ram_parts[2]                   # "LPDDR4X"

            # OS split
            os_parts = items[2].split()
            os_name = os_parts[0]     # "Windows"
            os_version = os_parts[1]  # "11"

            # Storage, Display, Software, Warranty
            storage = items[3]
            display = items[4]
            software = items[5]
            warranty = items[6]

            # Timestamp
            scraped_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Append to dict
            d['title'].append(ttle)
            d['price'].append(price)
            d['rating'].append(rating)
            d['link'].append(link)
            d['img'].append(img)
            d['off'].append(off)
            d['original_price'].append(original_price)
            d['scraped_at'].append(scraped_time)
            d['discount'].append(discount)

            d["Processor"].append(processor)
            d["Generation"].append(generation)
            d["RAM Capacity"].append(ram_capacity)
            d["RAM Type"].append(ram_type)
            d["OS Name"].append(os_name)
            d["OS Version"].append(os_version)
            d["Storage"].append(storage)
            d["Display"].append(display)
            d["Software"].append(software)
            d["Warranty"].append(warranty)

    except Exception as e:
        print(f"Error processing {files}: {e}")

# Convert to DataFrame
df = pd.DataFrame(d)
print(df.head())

        
df=pd.DataFrame(d)
df.to_csv("flipkart_laptop_data.csv", index=False)

        
            
            