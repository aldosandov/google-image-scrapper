from icrawler.builtin import GoogleImageCrawler
from dataclasses import dataclass
from ast import literal_eval
import pandas as pd
import os


@dataclass
class ImageScrapper:
    config_path: str = "config.csv"
    n_images: int = 150

    def __load_config(self):
        try:
            df = pd.read_csv(self.config_path)
            df["keywords"] = df["keywords"].apply(literal_eval) 

            return df
        except Exception as e:
            raise Exception(e)

    
    def __crawl_images(self, row):
        print(row)

        class_name = row["class_name"]
        keywords = row["keywords"]

        crawler = GoogleImageCrawler(
                feeder_threads=2,
                parser_threads=2,
                downloader_threads=4,
                storage = {
                    'root_dir': f'{os.getcwd()}/images/{class_name}'
                })

        for keyword in keywords:
            crawler.crawl(
                keyword=keyword, 
                max_num=self.n_images
                )


    def start(self):
        df = self.__load_config()
        df.apply(self.__crawl_images, axis=1)
