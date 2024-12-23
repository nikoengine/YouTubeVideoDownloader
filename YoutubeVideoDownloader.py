import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess


class YoutubeDownloader:
    def __init__(self):
        self.videos = []

    def add_video(self, url: str):
        self.videos.append(url)

    def download(self, save_path="."):
        for url in self.videos:
            try:
                subprocess.run(
                    ["yt-dlp", "-o", f"{save_path}/%(title)s.%(ext)s", url],
                    check=True
                )
            except subprocess.CalledProcessError as e:
                print(f"Error downloading {url}: {e}")


class DownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("500x300")

        self.downloader = YoutubeDownloader()
        self.save_path = ""

        self.setup_labels()
        self.setup_entry()
        self.setup_buttons()
        self.setup_status_label()

    def setup_labels(self):
        self.url_label = tk.Label(self, text="YouTube URL:")
        self.url_label.pack(pady=5)

    def setup_entry(self):
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack(pady=5)

    def setup_buttons(self):
        self.download_button = tk.Button(self, text="Download", command=self.download_videos)
        self.download_button.pack(pady=5)

    def setup_status_label(self):
        self.status_label = tk.Label(self, text="No videos added yet.", fg="red")
        self.status_label.pack(pady=10)

    def download_videos(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Invalid Input", "Please enter a valid YouTube URL.")
            return
        
        # Add video URL to the downloader
        self.downloader.add_video(url)

        # Open folder dialog to select save location
        self.save_path = filedialog.askdirectory()
        if not self.save_path:
            messagebox.showwarning("No Location", "Please select a save location.")
            return
        
        try:
            self.status_label.config(text="Downloading videos...", fg="blue")
            self.downloader.download(self.save_path)
            self.status_label.config(text="All videos downloaded successfully!", fg="green")
        except Exception as e:
            self.status_label.config(text="Error occurred during download.", fg="red")
            messagebox.showerror("Download Error", f"An error occurred: {e}")


if __name__ == "__main__":
    app = DownloaderApp()
    app.mainloop()
