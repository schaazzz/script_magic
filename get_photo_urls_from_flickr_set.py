#--------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2015 Shahzeb Ihsan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#--------------------------------------------------------------------------
## @file    get_photo_urls_from_flickr_set.py
#  @brief   Retrieves image & thumbnail URLs from the specified set and saves
#           them in the specified file in a format that can be used directly
#           in a JSSOR image slider's HTML code.
#
#  @author  Shahzeb Ihsan [shahzeb.ihsan@gmail.com]
#  @version 0.1

#--------------------------------------------------------------------------
# Module Imports
import os, sys, urllib2
import flickrapi
from HTMLParser import HTMLParser

#--------------------------------------------------------------------------
# Module Global Attributes
# --- N/A

#--------------------------------------------------------------------------
# Module Global Variables
# --- N/A

#--------------------------------------------------------------------------
# Module Local Attributes
api_key = 'ea5bf9b1668161e323060ad2d91accb1'
api_secret = '17b2e7c7b5475b8b'
set_id = '72157622960195643'

#--------------------------------------------------------------------------
# Module Internal Variables
jssor_div_output = None
photo_ids = []
page_large = []
page_thumbnails = []
url_large = []
url_thumbnails = []

#--------------------------------------------------------------------------
# Function: print_progress_bar
class FlickrDwnldPgParser(HTMLParser):
    """
    Extending the HTMLParser class to parse the image download page returned by
    Flickr. Searches for the image link in the div "allsizes-photo".

    @param n int: Current step
    @param total int: Total number of steps
    @param step int: Number of "steps" after which to increment the progress bar
    @param msg String: Text to be printed at the "head" of the progress bar
    """
    div_found = False
    url = ''

    #----------------------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        """
        Over ridden start tag function, this is all we need.
        """
        if tag == 'div':
            if 'allsizes-photo' in attrs[0][1]:
                self.div_found = True

        if tag == "img" and self.div_found:
            self.url = attrs[0][1]
            self.div_found = False

    #----------------------------------------------------------------------
    def get_url(self):
        """
        Returns the URL extracted from the Flickr page
        """
        return self.url

#--------------------------------------------------------------------------
# Function: print_progress_bar
def print_progress_bar(n, total, step = 1, msg = ''):
    """
    Prints a progress bar in the console.

    @param n int: Current step
    @param total int: Total number of steps
    @param step int: Number of "steps" after which to increment the progress bar
    @param msg String: Text to be printed at the "head" of the progress bar
    """
    str = '' + msg

    # Calculate the current percentage
    percentage = (100 * n) / total

    # Takes care of "off-by-one erros (OBOEs)"
    if n == total - 1:
        percentage = 100

    # Create the progress bar...
    for p in range(percentage):
        if p == 0:
            str += '[%(n)3d%%] ' % {'n': percentage}

        if (p % step) == 0:
            str += '='

    # Clear the previously display progress bar and print the new one...
    sys.stdout.write('\r' + str)
    sys.stdout.flush()

#--------------------------------------------------------------------------
if __name__ == '__main__':

    print '\r\n----------------------------------------------------------------'

    # Open the output file
    if len(sys.argv) > 1:
        jssor_div_output = open(os.path.join('', sys.argv[1]), 'wr')
    else:
        sys.stderr.write('Error! No output file specified...')
        sys.stderr.flush()
        sys.exit(-1)

    # Initialize the Flickr API
    print 'Initializing Flickr API ....... ',
    sys.stdout.flush()
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='etree')
    print 'done!'

    # We'll use the iterator returned by walk_set() to read all photo IDs in the specified set
    print 'Get Flickr set with id = ' + set_id +  '....... ',
    sys.stdout.flush()
    set = flickr.walk_set(set_id)
    print 'done!'

    print 'Read all photo IDs .......',
    sys.stdout.flush()
    for photo in set:
        photo_ids.append(photo.get('id'))
    print 'done!'

    # Re-initialize the Flickr API (this time we request responses in parsed JSON format)
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

    # Now we'll retrieve photo sizes for all photo IDs and filter "Large" & "Thumbnail"
    for n in range(len(photo_ids)):
        print_progress_bar(
                    n,
                    len(photo_ids),
                    2,
                    'Retrieving URLs for image pages: ')

        sizes = flickr.photos.getSizes(photo_id = photo_ids[n])

        # Iterate through all sizes in the parsed JSON respones
        for m in range(len(sizes['sizes']['size'])):
            label = sizes['sizes']['size'][m]['label']
            url = sizes['sizes']['size'][m]['url']

            if label == 'Large':
                page_large.append(url)

            if label == 'Thumbnail':
                page_thumbnails.append(url)
    print ' ...... done!'

    # Retrieve and parse pages for the "Large" image
    for n in range(len(page_large)):
        print_progress_bar(
                    n,
                    len(page_large),
                    2,
                    'Retrieving image URLs (large): ')

        response = urllib2.urlopen(page_large[n])
        html = response.read()
        parser = FlickrDwnldPgParser()
        parser.feed(html)
        url_large.append(parser.get_url())
    print ' ...... done!'

    # Retrieve and parse pages for the "Thumbnail" image
    for n in range(len(page_thumbnails)):
        print_progress_bar(
                    n,
                    len(page_thumbnails),
                    2,
                    'Retrieving image URLs (thumbnails): ')

        response = urllib2.urlopen(page_thumbnails[n])
        html = response.read()
        parser = FlickrDwnldPgParser()
        parser.feed(html)
        url_thumbnails.append(parser.get_url())
    print ' ...... done!'

    # Create the HTML output for JSSOR slides
    for n in range(len(url_large)):
        jssor_div_output.write('    <div>\r\n')
        jssor_div_output.write('        <a href=\"https://www.flickr.com/photos/schaazzz/'  + photo_ids[n] + '\"><img u=\"image\" src=\"' + url_large[n] + '\" /></a>\r\n')
        jssor_div_output.write('        <div u=\"thumb\">\r\n')
        jssor_div_output.write('            <div style=\"width: 100%; height: 100%; background-image: url(' + url_thumbnails[n] + '); background-position: center center; background-repeat: no-repeat; \">\r\n')
        jssor_div_output.write('            </div>\r\n')
        jssor_div_output.write('        </div>\r\n')
        jssor_div_output.write('    </div>\r\n')

    # Close the output file
    jssor_div_output.close()
    print '----------------------------------------------------------------\r\n'
