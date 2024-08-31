import requests
from bs4 import BeautifulSoup
import urllib.parse
from getpass import getpass
import os
import time

def get_redirected_url(url):
    """Mengambil URL setelah redirect, jika ada."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.url
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil redirect URL: {e}")
        return "loading"

def clean_url(url):
    """Membersihkan URL dari parameter yang tidak perlu."""
    url = urllib.parse.unquote(url)
    url = url.split('&sa=U&')[0]
    url = url.split('&usg=')[0]
    url = url.split('?_rdc=1&_rdr')[0]
    return url

def get_google_search_results(query):
    """Mengambil hasil pencarian Google berdasarkan query."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(query, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(5)  # Tambahkan delay 5 detik antar permintaan untuk menghindari error 429
        return soup.find_all('a')
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil hasil pencarian: {e}")
        return []

def print_social_media_links(platform, links, nama_input):
    """Mencetak link akun sosial media yang ditemukan."""
    if links:
        print(f"Akun {platform} untuk nama '{nama_input}':")
        for link in links:
            print(link)
        print()
    else:
        print(f"Tidak ditemukan akun {platform} untuk '{nama_input}'.")

def search_social_media_accounts(nama_input, key):
    """Melakukan pencarian akun sosial media berdasarkan nama."""
    if key != '0737':
        print("Kunci tidak valid. Access denied.")
        return

    platforms = {
        'Facebook': 'site:facebook.com',
        'Twitter': 'site:twitter.com',
        'Instagram': 'site:instagram.com'
    }

    for platform, search_query in platforms.items():
        query = f'intext:"{nama_input}" {search_query}'
        url = f'https://www.google.com/search?q={urllib.parse.quote(query)}'
        search_results = get_google_search_results(url)
        social_media_links = []

        for link in search_results:
            href = link.get('href')
            if href and href.startswith('/url?q='):
                url = href[7:].split('&')[0]
                url = clean_url(url)
                if 'google.com' not in url:
                    url = get_redirected_url(url)
                    if url != "loading":
                        social_media_links.append(url)

        print_social_media_links(platform, social_media_links, nama_input)

def main():
    """Main function untuk menjalankan program."""
    os.system("clear")
    print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
    print("    Tools Osint SOCIAL Media")
    print("        -CREATE BY MRY07XPLOIT -")
    print("    MEDAN CYBER TEAM  ")
    print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")

    nama_input = input("Masukkan nama akun yang ingin dicari: ").strip()
    kunci = getpass("Masukkan key: ").strip()
    search_social_media_accounts(nama_input, kunci)

if __name__ == "__main__":
    main()
