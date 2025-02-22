from pathlib import Path
import urllib.request
import urllib
import imghdr
import posixpath
import re

'''
Python api to download image form Bing.
Author: Guru Prasad (g.gaurav541@gmail.com)
'''

def find_urls_captions ( s, first, last ):
    


        captions=[]
        urls=[]
        tmp1 = s.split("murl&quot;:&quot;")

        for e in tmp1:
          try:
            captions.append (e.split("&quot;t&quot;:&quot;")[1].split("&quot")[0])
            urls.append (e.split("&quot;")[0])
            #print("xxx")
            #print(e.split("&quot;t&quot;:&quot;")[1].split("&quot")[0])
           
            #print(e.split("&quot;")[0])
            #print("xxx")
          except:
            pass
        
        start1= s.find(first)
        
        return captions, urls
        
class Bing:
    def __init__(self, query, limit, output_dir, adult, timeout,  filters='', verbose=True):
        self.download_count = 0
        self.query = query
        self.output_dir = output_dir
        self.adult = adult
        self.filters = filters
        self.verbose = verbose

        assert type(limit) == int, "limit must be integer"
        self.limit = limit
        assert type(timeout) == int, "timeout must be integer"
        self.timeout = timeout

        # self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        self.page_counter = 0
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}

    def save_image(self, link, file_path):
        request = urllib.request.Request(link, None, self.headers)
        image = urllib.request.urlopen(request, timeout=self.timeout).read()
        if not imghdr.what(None, image):
            print('[Error]Invalid image, not saving {}\n'.format(link))
            raise ValueError('Invalid image, not saving {}\n'.format(link))
        with open(str(file_path), 'wb') as f:
            f.write(image)

    
    def download_image(self, link):
        self.download_count += 1
        # Get the image link
        try:
            path = urllib.parse.urlsplit(link).path
            filename = posixpath.basename(path).split('?')[0]
            file_type = filename.split(".")[-1]
            if file_type.lower() not in ["jpe", "jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "webp", "jpg"]:
                file_type = "jpg"
                
            if self.verbose:
                # Download the image
                print("[%] Downloading Image #{} from {}".format(self.download_count, link))
                
            self.save_image(link, self.output_dir.joinpath("Image_{}.{}".format(
                str(self.download_count), file_type)))
          


            if self.verbose:
                print("[%] File Downloaded !\n")

        except Exception as e:
            self.download_count -= 1
            print("[!] Issue getting: {}\n[!] Error:: {}".format(link, e))

    
    def run(self):
        while self.download_count < self.limit:
            if self.verbose:
                print('\n\n[!!]Indexing page: {}\n'.format(self.page_counter + 1))
            # Parse the page source and download pics
            request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(self.query) \
                          + '&first=' + str(self.page_counter) + '&count=' + str(self.limit) \
                          + '&adlt=' + self.adult + '&qft=' + ('' if self.filters is None else str(self.filters))
            request = urllib.request.Request(request_url, None, headers=self.headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf8')
            print("##### HTML #######")


            captions, urls=  find_urls_captions( html, ",&quot;desc&quot;:&quot;", "&quot" ) 
            for i in range(len(captions)):
 

              print("Caption "+str(i))
              print(captions[i])
              print(urls[i])
            #print(html)
            if html ==  "":
                print("[%] No more images are available")
                break
            #links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)
            if self.verbose:
                print("[%] Indexed {} Images on Page {}.".format(len(urls), self.page_counter + 1))
                print("\n===============================================\n")

            for i in range(len(urls)):
                if self.download_count < self.limit:
                    try:
                      cap= captions[i]
                    except:
                      cap=self.query
                    self.download_image(urls[i])
                    # save caption
                    
                    with open(self.output_dir.joinpath("Image_{}.{}".format(str(self.download_count), "txt")) , "w") as file_object:
                        file_object.write(cap)


            self.page_counter += 1
        print("\n\n[%] Done. Downloaded {} images.".format(self.download_count))
        print("===============================================\n")
        print("Please show your support here")
        print("https://www.buymeacoffee.com/gurugaurav")
        print("\n===============================================\n")
