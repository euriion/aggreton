# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DaumKeywordItem(Item):
    name = Field()
    female = Field()
    male = Field()
    age_00 = Field()
    age_10 = Field()
    age_20 = Field()
    age_30 = Field()
    age_40 = Field()
    age_50 = Field()
    label_1 = Field()
    label_2 = Field()
    label_3 = Field()
    label_4 = Field()
    label_5 = Field()
    label_6 = Field()
    label_7 = Field()
    label_8 = Field()
    label_9 = Field()
    month_1 = Field()
    month_2 = Field()
    month_3 = Field()
    month_4 = Field()
    month_5 = Field()
    month_6 = Field()
    month_7 = Field()
    month_8 = Field()
    month_9 = Field()
    last_updated = Field(serializer=str)
