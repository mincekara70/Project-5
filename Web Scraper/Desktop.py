import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from multiprocessing import Pool

import Product


class Desktop(Product.Product):
    def __init__(self):
        self.page = "https://www.coolblue.nl/producttype:desktops"

    def run(self):
        filename = "Data/product_desktops.csv"
        file = open(filename, "w")
        file.write("product_type,product_name,product_price,product_brand,product_model,product_wifi,product_bluetooth,product_cpu,product_graphicscard,product_graphicsmemory,product_memory,product_storage,product_dimensions,product_weight\n")
        file.close()

        page_soup_first = self.bsPage(self.page)

        cards = page_soup_first.findAll(
            "div", {"class": "product-grid__item card"})
        page_count_buffer = page_soup_first.find(
            "ul", {"class": "pagination js-pagination"}).findAll("li")
        page_count = int(page_count_buffer[len(
            page_count_buffer) - 2].text.strip())

        for i in range(page_count):
            self.getPageData(i)

    def getCardData(self, card_link):
        if len(card_link) < 16:
            card_detail = self.bsPage(self.page[:23] + card_link)
            product_specs = ["Desktop"]

            self.addSpec(product_specs,
                         card_detail.h1.text.strip())
            self.addSpec(product_specs,
                         card_detail.find("strong", {"class": "sales-price--current"}).text.strip())
            self.addSpec(product_specs,
                         self.getSpec(card_detail, "Merk"))
            self.addSpec(product_specs,
                         self.getSpec(card_detail, "Fabrikantcode"))
            self.addSpec(product_specs,
                         self.getSpec(card_detail, "Wifi-standaard"))
            self.addSpec(product_specs,
                         self.getSpec(card_detail, "Bluetooth-versie"))
            self.addSpec(product_specs,
                         self.getSpec(card_detail, "Processor") + " " + self.getSpec(card_detail, "Processornummer"))
            self.addSpec(product_specs,
                         self.getSpec(card_detail, "Videokaart"))
            self.addSpec(product_specs,
                         self.getSpec(card_detail, "Videogeheugen"))
            self.addSpec(product_specs,
                         self.getSpec(card_detail, "RAM-geheugen"))
            self.addSpec(product_specs,
                         self.getSpec(card_detail, "Opslagcapaciteit"))
            self.addSpec(product_specs, "{0} x {1} x {2}".format(
                self.getSpec(card_detail, "Breedte"), self.getSpec(card_detail, "Diepte"), self.getSpec(card_detail, "Hoogte")))
            self.addSpec(product_specs, self.getSpec(
                card_detail, "Gewicht"))

            filename = "Data/product_desktops.csv"
            file = open(filename, "a")
            file.write(",".join(product_specs) + "\n")
            file.close()

            print("product_name: " + product_specs[1])