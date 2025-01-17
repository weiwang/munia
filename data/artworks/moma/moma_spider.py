import scraperwiki
import lxml.html
import urlparse
import json

def scrape_page(root):

    try:
        ##for p in root.xpath("//div[@id='omniture_caption']/h3//text()"):
        ##    title = p
        title = root.xpath("//div[@id='omniture_caption']/h3//text()")[0].strip()

        for p in root.xpath("//h4[text()='Works: ']/following-sibling::div/a[@href]//text()"):
            artist = p

        for p in root.xpath("//h4[text()='Classification: ']/following-sibling::div/a[@href]//text()"):
            material = p

        for p in root.xpath("//h4[text()='Permalink: ']/following-sibling::div/a[@href]/@href"):
            id = p

        for p in root.xpath("//p[@id='mainImage']//@src"):
            image = p

            item = {
            'id' : "http://www.moma.org/collection/"+id,
            'title' : title,
            'artist' : artist,
            #'location' : displayLoc,
            'image' : image,
            'material' : material,
            'venue' : "The Museum of Modern Art"
            }

        return item
        ## scraperwiki.sqlite.save(unique_keys=["title"], data=data)

    except:
        pass


# def scrape_and_look_for_next_link(url):
#     html = scraperwiki.scrape(url)
#     ## print html
#     root = lxml.html.fromstring(html)
#     scrape_page(root)

#     next_link = root.cssselect("a.next")

#     ## print next_link
#     if next_link:
#         next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
#         ## print next_url
#         scrape_and_look_for_next_link(next_url)

# def find_gallery_url(url):
#     html = scraperwiki.scrape(url)
#     print html
#     root = lxml.html.fromstring(html)
#     scrape_page(root)

#     gallery_url = root.cssselect("img.over")[0].attrib['src']

#     print gallery_url

def spider(starting_url):
    html = scraperwiki.scrape(starting_url)
    root = lxml.html.fromstring(html)
    dump = []
    dump.append(scrape_page(root))

    next_link = root.cssselect("a.next")
    
    while(next_link):
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        html = scraperwiki.scrape(next_url)
        root = lxml.html.fromstring(html)
        dump.append(scrape_page(root))
        next_link = root.cssselect("a.next")

    json.dump(dump, open('moma_paitning_and_sculpture_dump.json', "wb"))


base_url = 'http://www.moma.org/collection/'
starting_url = 'http://www.moma.org/collection/browse_results.php?criteria=O%3ADE%3AI%3A5%7CG%3AOV%3AE%3A1&page_number=1&template_id=1&sort_order=1'

if __name__ == "__main__":
    spider(starting_url)
