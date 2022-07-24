import hashlib
import os
import requests
import sys
import time
import zipfile

parent_dir = os.path.dirname(__file__)
input_dir = os.path.join(parent_dir, "input files")


def blakedigest(s):
    """use the blake2b algorithm to get the hexdigest of string s, encoded as
    utf-8"""
    # hashlib hash algorithms only accept bytes as input
    return hashlib.blake2b(bytes(s, encoding="utf-8")).hexdigest()


urlfiles = {
    "da": [
        os.path.join(input_dir, "District_Attorney_Incoming_Caseload.csv"),
        "https://data.sfgov.org/api/views/muc9-d8xi/rows.csv?accessType=DOWNLOAD",
    ],
    "police": [
        os.path.join(
            input_dir, "Police_Department_Incident_Reports__2018_to_Present.csv"
        ),
        "https://data.sfgov.org/api/views/wg3w-h783/rows.csv?accessType=DOWNLOAD",
    ],
    "arrests": [
        os.path.join(input_dir, "Arrests_Presented_and_Prosecutions.csv"),
        "https://data.sfgov.org/api/views/6r4m-yzvk/rows.csv?accessType=DOWNLOAD",
    ],
}


def main(files=None):
    """files: str in {'both', 'police', 'da'}
    If files is 'both', check both the da_download_url and
    the police_download_url for their datasets, and check if they hash to the
    same value as the current dataset.
    If a dataset hashes differently than the current one, replace the current
    version with the new version.
    If any files were modified, zip them all together in a zip file.
    """
    if files is None:
        files = set(urlfiles.keys())
    modified = {title: False for title in urlfiles}
    for title, (fname, url) in urlfiles.items():
        if title not in files:
            continue
        print(f"Getting data for {title} after a 45-second nap")
        time.sleep(45)  # to avoid spamming the website
        # the download is slow so it's really not that much of a time increase
        try:
            with open(fname) as f:
                hash_cur = blakedigest(f.read())
                # blakedigest(a) == blakedigest(b) is actually much slower than
                # than just a == b, but this way we
                # don't need to keep two multi-hundred-MB strings in memory.
                # hash(a) == hash(b) is faster than a == b, but hash() is
                # not cryptographically safe. 
            resp = requests.get(url)
            hash_url = blakedigest(resp.text)
            print(f"Comparing to {fname}")
            if hash_cur != hash_url:
                modified[title] = True
                print(f"Hash is different, overwriting {fname}")
                with open(fname, "w") as f:
                    f.write(resp.text)
            else:
                print("Hash is same, doing nothing")
        except Exception as ex:
            print(ex)
            continue
    if any(modified.values()):
        zip_fname = "input files/all_big_csvs.zip"
        print(f'zipping all csv files together at "{zip_fname}"')
        ogdir = os.getcwd()
        os.chdir(input_dir)
        with zipfile.ZipFile(zip_fname, 
                             mode='w', 
                             compression=zipfile.ZIP_LZMA) as zf:
            for _, (fname, url) in urlfiles.items():
                zf.write(os.path.basename(fname))
        os.chdir(ogdir)
    
    return modified


if __name__ == "__main__":
    files = sys.argv[1:]
    main(files)
