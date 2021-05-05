import os
import sys
import csv
from librarything_crawler import settings
from librarything_crawler.items import LibrarythingReview


class CSVExportPipeline(object):

    def __init__(self):
        csv_store = settings.CSV_STORE_LOCATION
        self.results = open(os.path.join(csv_store, 'user_reviews.csv'), 'a')

    def open_spider(self, spider):
        header_keys = ','.join(LibrarythingReview.field_order)
        self.results.write(('%s\n' % header_keys))


    def process_item(self, item, spider):
        csv_line = [item.get(field, '') for field in item.field_order]

        csvwriter = csv.writer(self.results)
        csvwriter.writerow(csv_line)

        return item

    def close_spider(self, spider):
        self.results.close()
