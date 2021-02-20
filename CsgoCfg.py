import os 
import getpass
from pathlib import Path
import sys
import time
import re
from pynput import keyboard
from pynput.keyboard import Key,Controller



class Csgocfg:

    def __init__(self):

        self.cfgPath = "henüz tanımlanmadı"
        self.cfg730 = "henüz tanımlanmadı"
        self.deskPath = "henüz tanımlanmadı"
        self.deskCfg = "henüz tanımlanmadı"
        self.keys = {}

    """Bu metodun amacı Csgo'nun içindeki cfg klasörüne ulaşmak burada os.walk() kullanarak bu dosyayı bulabilirdim
    fakat fazla zaman alıyordu. Ben de bu şekilde yaptım"""
    def findCfgPath(self):

        for i in (os.listdir("C:\\")): #Local diskleri elle yazmak istemezdim ama local disklere ulaşabileceğim bir fonksiyon bulamadım. 
            isCfgPath = os.sep.join(["C:",i,"Steam\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\cfg"])  

            # Yukarıda C'nin içindeki klasörleri tek tek deneyip cfg'ye ulaşıyorum fakat eğer Steam C'nin içindeki klasörlerin içindeki bir dizindeyse hata alırım bunun farkındayım.

            if os.path.exists(isCfgPath) == True: # Burada tek tek deniyoruz böyle bi dizin var mı? sorgusu yapılıyor. Varsa tahmin ettiğiniz gibi True döndürüyor.
                self.cfgPath = isCfgPath
                

        try:

          #Burada Steamin farklı D' diskine kurulu olma ihtimaline karşı yukarıdaki işlemi burada yaptım. 

            for i in (os.listdir("D:\\")): 
                isCfgPath = os.sep.join(["D:",i,"Steam\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\cfg"])
                
                if os.path.exists(isCfgPath) == True:
                    self.cfgPath = isCfgPath

                    

        except Exception: pass
      
    def findCfg730(self): 

        #Bu metodun amacı Cs-Go'daki en son kullandığımız ayarların saklı olduğu 730 klasörünün içindeki config.cfg dosyasını bulmak.

        self.findCfgPath() # Bunu yapmak için bu metodu çağırmam gerek çünkü constructor'ın içinde self.cfgPath = 'Henüz tanımlanmamış' olarak tanımlı.

        self.cfg730 = self.cfgPath.split("\\steamapps")[0]
        self.cfg730 = os.sep.join([self.cfg730,"userdata\\443151005\\730\\local\\cfg\\config.cfg"])
       
    def findDeskPath(self):

        #Bu metodun amacı Masaüstü yolunu bulmak  

        home = str(Path.home()) 

        #Bu fonksiyon bize 'C:\Users\Kullanıcı' sonucunu veriyor.Fakat Masaüstü bazen Kullanıcı Klasörünün içinde olmuyor Mesela bende 'Onedrive'ın klasöründe
        #Bundan dolayı try except kullandım.

        try:
            try:
                self.deskPath = (os.sep.join([home,"Masaüstü"])) #Bu fonksiyon home objesinden aldığımız sonuca verilen parametreyi ekliyor.
                if os.path.exists(self.deskPath) == False: #Eğer böyle bir dizin yoksa false dündürüp diğer bloklara geçişi sağladım
                    raise Exception
            except Exception:
                self.deskPath = (os.sep.join([home,"Desktop"]))
                if os.path.exists(self.deskPath) == False:
                    raise Exception
        except:
            try:
                self.deskPath = (os.sep.join([home,"Onedrive\\Desktop"]))
                if os.path.exists(self.deskPath) == False:
                    raise Exception

            except Exception: 
                self.deskPath = (os.sep.join([home,"Onedrive\\Masaüstü"]))
                if os.path.exists(self.deskPath) == False:
                    raise Exception
      
    def copyCfg(self,newcfgname,bindscripts=None): 


        #Bu metodun amacı kullanıcıdan dosya adı alarak 730 klasöründeki config dosyasının kopyasını
        # oyunu içinde exec komutuyla config dosyalarını çalıştırabildiğimiz cfg klasörüne atıyor.
        # Bunu neden yapıyorum. Ben oyun içinde çok sık ayar değiştiren birisiyim oyundan çıkıp tekrar girdiğimde ayarlarım kaybolmuyor
        # fakat oyundan çıkıp tekrar girdiğimde alias(özel komutlar,örn;jumpthrow) kodları çalışmıyor. Çünkü 730(Yani son ayarlarımızın kayıtlı olduğu config)
        # bu alias kodlarını saklayamıyor. Ben de bu yüzden böyle bir proje oluşturdum. Son kullandığım ayarları istediğim zaman oyun içinde kullanmak için 730'daki cfgyi kopyalayıp
        # özel kodları ve bind komutlarını da aşağıdaki bir metodla bu yeni config dosyasına ekleyerek /csgo/cfg klasörüne atacak.


        self.findCfg730()
        self.findCfgPath()

        self.newConfigFile = (f"{self.cfgPath}\\{newcfgname}.cfg")
        with open(self.cfg730,"r",encoding="utf-8") as seventhirty:
            with open(self.newConfigFile,"w",encoding="utf-8") as f:
                for satir in seventhirty:
                    f.write(satir)

                if bindscripts:
                    for i in bindscripts:
                        f.write(i)                    

    def copyDesktop(self,newcfgname,bindscripts=None): #Bu metod yukarıdaki metodun son kullanılan ayarları Masaüstüne atan modeli 
        
        self.findCfg730()
        self.findDeskPath()
  
        self.deskCfg = (f"{self.deskPath}\\{newcfgname}.cfg")

        with open(self.deskCfg,"w",encoding="utf-8") as deskCfg:
            with open(self.cfg730,"r",encoding="utf-8") as seventhirty:
                for satir in seventhirty:
                    deskCfg.write(satir)
                if bindscripts:
                    for i in bindscripts:
                        deskCfg.write(i)

    def binds(self,**kwargs): 
        
        #Burada 730 klasöründe tutulmayan özel kodları ve bind komutlarını yeni oluşturduğumuz config dosyasına ekliyor **kwargs almamın sebebi kullanıcıdan
        # hangi kodu eklemek istediği ve kodu atayacağı tuş olarak parametre almış olmam. Çalıştırılırken CsgoCfg.binds(f=jumpthrow)
        scripts = []
        
        for bindkey, bindscript in kwargs.items():
            script = ""

            if bindscript == "jumpthrow":
                script = (f'alias "+jumpthrow" "+jump;-attack"; alias "-jumpthrow" "-jump"; bind {bindkey} "+jumpthrow"\n')

            elif bindscript == "akm4":
                script = (f'bind "{bindkey}" "buy ak47; buy m4a1;"\n')

            elif bindscript == "scroll":
                script = (f'bind "{bindkey}" "+jump"\n')

            scripts.append(script)

        return scripts

    def showMenu(self):
        menu = """


        1- Halihazırda oyun içinde kullandığım ayarlarımı CFG dizinine at.
        2- Halihazırda oyun içinde kullandığım ayarlarımı Masaüstüne at.
        3- Programdan çıkış yap.


        """
        print(menu)

    def showFileName(self):
        menu = """

        Oluşturmak CFG dosyasının adını yazınız: 

        """
        print(menu)

    def showBinds(self):
        binds = """
        1 - Jumpthrow (Bu bind kodu ile atadığınız tuşa bastığınız zaman bombayı zıplayarak en tepe yükseklikte fırlatır.)
        2 - AK-47 / M4 Satın al (Bu bind kodu ile atadığınız tuşa bastığınız zaman CT/T tarafında paranız yeterliyse AK-47/M4 satın alır.)
        3 - Scroll ile zıplama (Mouse scroll tuşunu her çevirdiğinizde zıplar. Bunnyhop yapmak için kullanılabilir.)
        4 - Bind komutu eklemek istemiyorum.
        """
        print(binds)
        #Kaç adet seçenek olduğunu döndürür. askAddBinds Fonksiyonunda yapılan seçimi kontrol etmemize olanak sağlar.
        return 4
    
    def warningMessage(self,messageKey):

        messages = {
            "wrongProcessName" : "\tYanlış seçim yaptınız! Lütfen uygulamak yapmak istediğiniz işlemin numarasını doğru giriniz.",
            "wrongFilename" : "\tDosya adı yalnızca harfler ve rakamlardan oluşmalıdır.",
            "wrongBindNum" : "\tYanlış bind komut numarası girdiniz. Lütfen doğru bind komut numarası giriniz."
        }

        message = messages[messageKey]
        for i in range(4):
            print(message,"."*i)
            time.sleep(0.3)
        os.system("cls")

    def askWhere(self):
        self.showMenu()
        try:
            decision = int(input("\tUygulamak istediğiniz işlemin numarasını giriniz: "))
            print("\n"*2)
            if decision == 3:
                sys.exit()
            elif decision not in range (1,3):
                os.system("cls")
                self.warningMessage("wrongProcessName")      
                self.askWhere()
            else:
                return decision
        except Exception:
            self.askWhere()

    def checkFileName(self,filename):
        pattern = r'[a-zA-Z0-9_]'
        result = re.match(pattern,filename)
        if not result:
            self.warningMessage("wrongFilename")
            self.askFileName()
        
        else: return filename

    def askFileName(self):
        self.showFileName()
        os.system("cls")
        filename = str(input("\tOluşturmak istediğiniz dosya ismini giriniz: "))
        return self.checkFileName(filename)

    def askAddBinds(self):
        
        totalBinds = self.showBinds()
        try:
            bindNum = int(input("\tCFG dosyanıza eklemek istediğiniz bind komut numarasını giriniz? "))
            if bindNum not in range(1,totalBinds+1):
                self.warningMessage("wrongBindNum")
                self.askAddBinds()

            elif bindNum == 4:
                pass

            else:
                self.getBindKeys(bindNum)
        except Exception as err:
            print(err)
            self.warningMessage("wrongBindNum")
            self.askAddBinds()

    def askKeepGoing(self):
        try:
            isKeepGoing = str(input("\tBaşka bir bind komutu eklemek istiyor musunuz?(e/h) "))
        except Exception as err:
            self.askKeepGoing()

        if isKeepGoing.lower() == "e":
            return True

        else: return False

    def getBindKeys(self,bindNum):
        
        bindNumtoKey = {
            "1":"jumpthrow",
            "2":"akm4",
            "3":"scroll",
        }
        dictkey = bindNumtoKey[str(bindNum)]
        print("\tLütfen bind komutunu eşleştirmek istediğiniz tuşa basınız!")
        bindkey = self.getBindKey()
        keybo = keyboard.Controller()
        keybo.press(Key.esc)
        os.system("cls")
        print(f"\t{bindkey} tuşu bind key olarak atandı.")
        self.keys[bindkey] = dictkey
        # askAgain = self.askKeepGoing()
        if self.askKeepGoing():
            self.askAddBinds()
    
    def keysToScripts(self):
        scripts =self.binds(**self.keys)
        return scripts


    def on_press(self,key):
        
        try:
            # print(key.char)
            self.listener.stop()
            key = key.char
        except Exception as err:
            # print(key.name)
            self.listener.stop()
            key =  key.name

        self.key = key

    def getBindKey(self):
        with keyboard.Listener(on_press=self.on_press) as self.listener:
            self.listener.join()
        return self.key    
            

    def run(self):
        self.findCfgPath()
        self.findCfg730()
        self.findDeskPath()
        decision = self.askWhere()
        filename = self.askFileName()

        self.askAddBinds()
        scripts = self.keysToScripts()
        
        if decision == 1:
            self.copyCfg(filename,scripts)

        elif decision == 2:
            self.copyDesktop(filename,scripts)


a = Csgocfg()
a.run()

