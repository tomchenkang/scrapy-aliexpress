from bs4 import BeautifulSoup
import threading
from time import sleep
from queue import Queue
import requests

class Getip():
	def __init__(self,page):
		self.ips = []
		self.urls = []
		for i in range(1, page+1):
			self.urls.append("http://www.xicidaili.com/nn/%s"%i)
		self.header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
		self.q = Queue()
		self.Lock = threading.Lock()
	def get_ips(self):
        #获取代理
		for url in self.urls:			
			res = requests.get(url, headers=self.header)
			sleep(3)
			soup = BeautifulSoup(res.text, 'lxml')
			ips = soup.findAll('tr')
			for i in range(1, len(ips)):
				ip = ips[i]
				tds = ip.find_all("td")				
				ip_temp = tds[5].contents[0].lower() + '://' + tds[1].contents[0] + ":" + tds[2].contents[0]
				self.q.put(ip_temp)
	def check_second(self):
		while not self.q.empty():
			ip = self.q.get()
			scheme = ip.split(':')[0]
			proxy={scheme: ip}
			try:				
				res = requests.get("https://www.aliexpress.com", proxies=proxy,timeout=5)
				self.Lock.acquire()
				if res.status_code == 200:
					self.ips.append(ip)
					print(ip)
					self.Lock.release()
			except Exception:
				pass
		
	def main(self):
        #多线程运行检测
		self.get_ips()
		threads=[]
		for i in range(5):
			t = threads.append(threading.Thread(target=self.check_second, args=[]))
		for t in threads:
			t.start()
		for t in threads:
			t.join()
		# self.check_second()
		return self.ips
def write_ip():
	my = Getip(1)
	f = open('proxy.txt', 'w')
	for i in my.main():
		f.write(i+'\n')
	f.close()
if __name__ == '__main__':
	write_ip()

