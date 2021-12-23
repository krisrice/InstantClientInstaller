import json
import platform
import requests
import re
import hashlib
import os


def getType(url):
    if "jdbc" in url:
        return "jdbc"
    if "sqlplus" in url:
        return "sqlplus"
    if "sdk" in url:
        return "sdk"
    if "odbc" in url:
        return "odbc"
    if "tools" in url:
        return "tools"
    if "lite" in url:
        return "lite"
    if "basic" in url:
        return "basic"
    return "unknown"

def md5sum(filename):
    h  = hashlib.md5()
    with open(filename, 'rb') as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            h.update(byte_block)
    return h.hexdigest()

def sha256sum(filename):
    h  = hashlib.sha256()
    with open(filename, 'rb') as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            h.update(byte_block)
    return h.hexdigest()

def download(url):
     r = requests.get(url)
     output =  os.path.basename(url)
     with open(output, 'wb') as f:
         f.write(r.content)
     sums={};
     sums['md5'] = md5sum(output);
     sums['sha1'] = sha256sum(output);
     return sums
def getVersion(p,v,type):
     for version in downloads['downloads']['platform'][p.lower()]['versions']:
         if ( version['version'] == v and version['type'] == type):
             return version


def printRecord(rec,url):
    global tryDownload
    version = re.findall("\-([\d][\d]\.[\d]+)", url)[0]
    v = getVersion(rec["platform"],version,getType(url))
    if 'download' in v and 'md5' in v :
        print("Skipping:"  + v['download'])
        print("\tMD5:"  + v['md5'])
        print("\tSHA1:"  + v['sha1'])
        return;
    ret = rec.copy()
    ret["version"] = version;
    ret["type"] = getType(url);
    ret["download"] ="https:" + url.lstrip();
    print("Processing : " + ret["download"])
    if  not "platform" in downloads['downloads'] :
        downloads['downloads']['platform'] = {}

    if not ret["platform"] in downloads['downloads']['platform'] :
        downloads['downloads']['platform'][ret["platform"]] = {"latest":version,"versions":[]}

    if  downloads['downloads']['platform'][ret["platform"]]['latest'] < version:
        downloads['downloads']['platform'][ret["platform"]]['latest'] = version

    if  tryDownload > 0  :
        sums = download(ret["download"]);
        ret["md5"] = sums['md5'];
        ret["sha1"] = sums['sha1'];
        tryDownload = tryDownload - 1;

    downloads['downloads']['platform'][ret["platform"]]["versions"].append(ret)


    return ret

p = platform.system()
m = platform.machine()
downloads = {}
downloads = json.load(open('fullDownloads.json'))
if not 'downloads' in downloads:
    downloads['downloads'] = {};

tryDownload=1000


data = json.load(open('downloads.json'))
for rec in data:
    r = requests.get(rec["url"])
    files = re.findall("href='(.*tgz|.*tar.gz|.*zip)'", r.text)
    for dwnld in (files):
        printRecord(rec,dwnld)
    files = re.findall("data-file='(.*tgz|.*tar.gz|.*zip)'", r.text)
    for dwnld in (files):
        printRecord(rec,dwnld)

with open('fullDownloads.json', 'w') as outfile:
    json.dump(downloads, outfile)
    