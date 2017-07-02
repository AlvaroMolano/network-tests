#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

import csv
import os
import requests
import sys
import time

class DownloadTester():
    DEFAULT_LOCATION = "use"
    DEFAULT_DOWNLOAD_COUNT = 1
    VERBOSE = False
    localFilename = "100MB-newark.bin"
    locations = {
                 'london': 'http://speedtest.london.linode.com/100MB-london.bin',
                 'sanjose': 'http://speedtest.sjc01.softlayer.com/speedtest/speedtest/random500x500.jpg' ,
                 'tokyo': 'http://speedtest.tokyo.linode.com/100MB-tokyo.bin',
                 'use': 'http://speedtest.newark.linode.com/100MB-newark.bin',
                 'usw': 'http://speedtest.fremont.linode.com/100MB-fremont.bin',
                 'washington': 'http://speedtest.wdc01.softlayer.com/downloads/test500.zip'
                 }

    def get_download_url(self, location=None):
        if location is None:
            location = self.DEFAULT_LOCATION
        return self.locations.get(location)

    def get_local_filename(self, url);
        return localFilename = url.split('/')[-1]

    def download_file(self, url) :

      self.localFilename = localFilename
      with open('/tmp/' + localFilename, 'wb') as f:
        dl = 0
        dl_speed = 0
        start = time.clock()
        r = requests.get(url, stream=True)
        total_length = r.headers.get('content-length')

        if total_length is None: # no content length header
          f.write(r.content)
        else:
          for chunk in r.iter_content(1024):
            dl += len(chunk)
            f.write(chunk)
            done = int(50 * dl / int(total_length))
            dl_speed = dl/(time.clock() - start)
            #Convert to MB/s when printing
            if self.VERBOSE:
              sys.stdout.write("\r[%s%s] %s MB/s" % ('=' * done, ' ' * (50-done), round(dl_speed/8000000,2)))
              sys.stdout.flush()
          time_elapsed = (time.clock() - start)
          avr_speed = (dl/time_elapsed)/8000000
          self.cleanup(localFilename)
          results = (avr_speed,time_elapsed, "100MB")
      return results

    def cleanup(self, localFilename):
      #Cleanup
      os.remove("/tmp/" + localFilename)


    def csv_parser(self, results, csv_file):
        with open(csv_file, 'wb') as myfile:
            wr = csv.writer(myfile)
            header = ["Muestra", "Tamaño", "Velocidad Promedio (MB/sec)"]
            wr.writerow(header)
            n = 1
            for result in results:
                row = [n,result[2],round(result[0])]
                wr.writerow(row)
                n += 1