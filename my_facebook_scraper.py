# my_facebook_scraper.py
import requests
from bs4 import BeautifulSoup
from facebook_page_scraper import Facebook_scraper
import databases
import sqlalchemy
from sqlalchemy import Column, String, Integer, JSON, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

class FacebookScraper:
    def extract_page_description(self, soup):
        desc_element = soup.find("meta", property="og:description")
        if desc_element:
            description = desc_element["content"]
            return description
        return "Description not found"

    def extract_profile_picture(self, soup):
        image_element = soup.find("meta", property="og:image")
        if image_element:
            profile_picture_url = image_element["content"]
            return profile_picture_url
        return "Profile picture not found"

    def scrape_facebook_page(self, posts_count=10):
        try:
            # Set the parameters for scraping
            page_name = "Nasa"
            browser = "firefox"
            timeout = 600  # 600 seconds
            headless = True

            # Instantiate the Facebook_scraper class
            meta_ai = Facebook_scraper(page_name, posts_count, browser, timeout=timeout, headless=headless)

            # Scrape the data
            json_data = meta_ai.scrap_to_json()

            # Return the scraped data
            return json_data
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

    def scrape_data(self, page_url, posts_count=10):
        try:
            # Scrape data from the provided URL
            response = requests.get(page_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                page_title = soup.title.string if soup.title else "Title not found"
                page_description = self.extract_page_description(soup)
                profile_picture = self.extract_profile_picture(soup)

                # Call the scrape_facebook_page function to get additional data
                facebook_page_data = self.scrape_facebook_page(posts_count)

                # Combine the data
                combined_data = {
                    "page_title": page_title,
                    "page_description": page_description,
                    "profile_picture": profile_picture,
                    "posts_data": facebook_page_data
                }

                # Save the scraped data to the database
                self.save_to_database(combined_data)

                # Return the combined data
                return combined_data
            else:
                return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

    def save_to_database(self, data: dict):
        try:
            # SQLite database setup
            database_url = "sqlite:///./test.db"
            database = databases.Database(database_url)
            metadata = sqlalchemy.MetaData()

            Base = declarative_base()

            class FacebookScrapingData(Base):
                __tablename__ = "facebook_scraping_data"

                id = Column(Integer, primary_key=True, index=True)
                page_title = Column(String, index=True)
                page_description = Column(String)
                profile_picture = Column(String)
                posts_data = Column(JSON)
                created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

            # Database URL to be used for connecting to the database
            DATABASE_URL = "sqlite:///./test.db"

            # SQLAlchemy database engine
            engine = create_engine(DATABASE_URL)

            # Create the table
            Base.metadata.create_all(bind=engine)

            with Session(engine) as session:
                scraping_data = FacebookScrapingData(**data)
                session.add(scraping_data)
                session.commit()
        except Exception as e:
            return {"error": f"An error occurred while saving to the database: {str(e)}"}
