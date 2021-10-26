# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class LeruaparserPipeline:
    def process_item(self, item, spider):
        item['specifications'] = dict(zip(item['specifications_dt'], item['specifications_dd']))
        del item['specifications_dt']
        del item['specifications_dd']
        print()
        return item


class LeruaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    img = img.replace('_82', '_640')  # w_82, h_82
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = request.url.split('/')[-1].split('.')[0]
        dir_name = item['link'].split('/')[-2]
        return f'full/{dir_name}/{image_guid}.jpg'
