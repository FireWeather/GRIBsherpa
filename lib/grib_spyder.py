__author__ = 'MCP'
import urllib.request
import urllib.error
import lib.html_parser
import os


#() holds any inheritance
class GribSpyder(object):

    def __init__(self, args):
        self.link_parser = lib.html_parser.GRIBLinkParser()
        self.url = args['url']
        self.tmp_dir = self.__build_tmp_path()

    # -opens url in try catch block. Will need to extend catches based on request type
    # -error object can hold server response. There is a dict of common responses (see bookmark)
    def get_html(self, url):
        try:
            response = urllib.request.urlopen(url)
        except urllib.error.HTTPError as err:
            return err
        except urllib.error.URLError as err:
            return err
        except ValueError as err:
            return err
        return str(response.readall())

    # Gets html, makes sure link exists, attempts to download it.
    def download_file_by_link(self, link):
        html = self.get_html(self.url)
        print("url response type: " + str(type(html)))
        #link_exists = self.link_parser.grib_link_exists(link, html)
        if self.__link_exists_in_html(link, html):
            to_download = self.__build_link(self.url, link)
            self.__download(to_download)
        else:
            print("link to download does not seem to exist.")


    # Private -------------------------------------------------------

    def __build_link(self, url, link):
        return url + link

    # builds a path to 'tmp' which should be in project tree
    # NOTE: this expects tmp to exist one dir above location of this file, this
    # may need to be more flexible in the future...
    def __build_tmp_path(self):
        tmp_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'tmp/')
        if os.path.exists(tmp_dir):
            print("found tmp for storage: " + tmp_dir)
            return tmp_dir
        else:
            print("ERROR in GribSpyder.__build_tmp_path: tmp directory not found")
            return None

    # 1. expects there to be a temp directory
    # 2. builds storage file path based on tmp path and base of url being downloaded
    # 3. attempts to download file
    def __download(self, url):
        store_loc = self.tmp_dir + self.__get_url_base(url)
        print("attempting to download to tmp: " + url)
        urllib.request.urlretrieve(url, store_loc)

    # gets part of url after last slash
    def __get_url_base(self, url):
        return url.rsplit('/', 1)[1]

    # verifies that a link (text) exists in the html
    def __link_exists_in_html(self, link, html):
        return self.link_parser.grib_link_exists(link, html)



