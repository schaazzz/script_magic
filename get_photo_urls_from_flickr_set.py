import sys, urllib2
import flickrapi
from HTMLParser import HTMLParser

api_key = 'ea5bf9b1668161e323060ad2d91accb1'
api_secret = '17b2e7c7b5475b8b'

set_id = '72157622960195643'

photo_ids = []
page_large_1600 = []
page_thumbnails = []
url_large_1600 = []
url_thumbnails = []

print '\r\n'
print 'Initializing Flickr API ....... ',
sys.stdout.flush()
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='etree')
print 'done!'

print 'Get Flickr set with id = ' + set_id +  '....... ',
sys.stdout.flush()
set = flickr.walk_set(set_id)
print 'done!'

print 'Read all photo IDs .......',
sys.stdout.flush()
for photo in set:
    photo_ids.append(photo.get('id'))
print 'done!'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
for n in range(len(photo_ids)):
    str = 'Retrieving photo URLs: '
    percentage = (100 * n) / len(photo_ids)

    if n == len(photo_ids) - 1:
        percentage = 100

    for p in range(percentage):
        if p == 0:
            str += '[%(n)3d%%] ' % {'n': percentage}

        if (p % 2) == 0:
            str += '='

    sys.stdout.write('\r' + str)
    sys.stdout.flush()

    sizes = flickr.photos.getSizes(photo_id = photo_ids[n])

    for m in range(len(sizes['sizes']['size'])):
        label = sizes['sizes']['size'][m]['label']
        url = sizes['sizes']['size'][m]['url']

        if label == 'Large 1600':
            page_large_1600.append(url)

        if label == 'Thumbnail':
            page_thumbnails.append(url)

print ' ...... done!'
