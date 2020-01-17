import bs4
import requests as req
import pafy
import os
from time import time
import youtube_dl 

class Youtube_Downloader():
    def __init__(self, url, playlist_name="", _type="Local",folder=os.path.expanduser("~\\Videos").replace("\\", "/")):
        self._url = url 
        self._apikey = pafy.set_api_key("AIzaSyAm6pxYxNJS9oZIxwxGTpptJrP33C9ZyVw")
        self._path = ""
        self._folderType = _type
        self._folderName = folder
        self._playlist_name = playlist_name
        
        print(self._folderName)
        if self._folderType == "Local":
            self._folderName = self._folderName + "/" + "Local"
            if not os.path.exists(self._folderName):
                os.mkdir(self._folderName)
        elif self._folderType == "Playlist":
            self._folderName = self._folderName + "/" + "Playlist"
            if not os.path.exists(self._folderName):
                os.mkdir(self._folderName)
                
           
    def video_details(self):
        details = pafy.new(self._url)
        return details
    
    def download_video(self):
        
        vid_detail = self.video_details()
        best_stream = vid_detail.getbest(preftype="mp4")
        if self._folderType == "Playlist":
            self._path = self._folderName + "/" + self._playlist_name
            self._path = self._path.replace(",", "_").replace("|", "__")
            if not os.path.exists(self._path):
                os.mkdir(self._path)
            else:
                print("Playlist exists")
        else:
            self._path = self._folderName + "/" + vid_detail.title
            if os.path.exists(self._path):
                self._path = self._folderName + "/" + vid_detail.title + str(int(time()))
                self._path = self._path.replace(",", "_").replace("|", "__")
                os.mkdir(self._path)
            else:
                self._path = self._path.replace(",", "_").replace("|", "__") 
                os.mkdir(self._path)
        
        print(self._path)
        best_stream.download(filepath=self._path)

class Youtube_PlayList():
    def __init__(self,url):
        self._urlList = []
        self._playListUrl = url
        self._downloadFolder = ""
        
    def list_returner(self):
        res = req.get(self._playListUrl)
        parsed_data = bs4.BeautifulSoup(res.text, "html.parser")
        self._downloadFolder = parsed_data.findAll('h1')[1].text.strip()
        video_container = parsed_data.findAll("div", {'id': 'content'})
        for container in video_container:
            links = container.findAll('a', {'class': 'pl-video-title-link yt-uix-tile-link yt-uix-sessionlink spf-link'})
            for link in links:
                self._urlList.append("https://www.youtube.com/" + link['href'])
        return self._urlList
    
    def connector(self):
        urlList = []
        urlList = self.list_returner()
        for url in urlList:
            print(self._downloadFolder)
            obj = Youtube_Downloader(url, self._downloadFolder, "Playlist")
            obj.download_video()
            
    
def main():
    while True:
        print("-"*10 + "Welcome" + "-"*10)
        print("1. Want to download playlist: ")
        print("2. Want to download a single video")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            user_url = input("Enter playlist url: ")
            obj = Youtube_PlayList(user_url)
            obj.connector()
        elif choice == "2":
            user_url = input("Enter video url: ")
            obj = Youtube_Downloader(user_url)
            obj.download_video()
        elif choice == "3":
            break
        else:
            print("Invalid Choice")
        
if __name__ == "__main__":
    main()