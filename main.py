from tkinter import *
from tkinter import filedialog as fd

import pathlib
import os

from cryptography.fernet import Fernet

# Получаем пользователя
userName = os.environ.get("USERNAME")
# Создаём путь к новой папке
path = "C:/Users/" + userName + "/Documents/ForEra"
# Создаём папку игнорируя факт её существования
pathlib.Path(path).mkdir(parents=True, exist_ok=True)

splitKey = "§"  # после этого обозначения идет зашифрованный документ

def AskForOpen(title, filetypes):
    _path = fd.askopenfilename(initialdir=path, title=title, filetypes=filetypes)
    return _path

def SaveOutFile(path, outputText):
    file = open(path, "w")
    file.write(outputText)
    file.close()


def OnButtonOpenBaseClick():
    _path = AskForOpen("Выберите базу данных", (("Файлы базы данных", "*.fe"), ("Все файлы", "*.*")))
    if _path == '': return

    file = open(_path, "r")
    text = file.read()

    splittedText = text.split(splitKey)
    cipherKey = bytes(splittedText[0], encoding='utf-8')
    encryptedText = bytes(splittedText[1], encoding='utf-8')

    cipher = Fernet(cipherKey)
    decryptedText = cipher.decrypt(encryptedText).decode('utf-8')

    _filesTypes = [('Text files', '*.txt'),
                   ('Doc files', '*.doc; *.docx'),
                   ('All Files', '*.*')]
    _path = fd.asksaveasfilename(initialdir=path, title="Выберите куда итоговый файл",
                                 defaultextension=".txt", filetypes=_filesTypes)

    SaveOutFile(_path, decryptedText)



def OnButtonCreateBase():
    _path = AskForOpen("Выберите файл для кодирования", (("Text","*.txt"), ("Все файлы", "*.*")))
    if _path == '': return

    file = open(_path, "rb")
    text = file.read()

    cipherKey = Fernet.generate_key()
    cipher = Fernet(cipherKey)
    encryptedText = cipher.encrypt(text)

    _filesTypes = [('FE Base Type', '*.fe'), ('FE Old Base Type', '*.ofe')]
    _path = fd.asksaveasfilename(initialdir=path, title="Выберите куда сохранить базу",
                                 defaultextension = ".fe", filetypes = _filesTypes)

    outputText = str(cipherKey.decode("utf-8") ) + splitKey + str(encryptedText.decode("utf-8") )

    SaveOutFile(_path, outputText)

# Создаём окно приложения
window = Tk()

# Задаём заглавие окна
window.title("{Название приложения}")
# Задаём размер окна
window.geometry('400x250')

# Отключаем изменение размера окна
window.resizable(False, False)

_tempTextVar = StringVar()
textHeader = Label(window, textvariable=_tempTextVar)
textHeader.place(x=200, y=50, anchor=CENTER)
_tempTextVar.set("Добро пожаловать в {Название приложения}!" + "\n" +
                 "Здесь вы можете создать небольшую базу данных," + "\n" +
                 "Для хранения в зашифрованном виде.")

# Создаём кнопку "Открыть базу"
buttonOpenBase = Button(window, text="Открыть базу данных", command=OnButtonOpenBaseClick, justify=LEFT)

# Настраиваем её расположение
buttonOpenBase.grid(row=1, column=1)
buttonOpenBase.place(x=50, y=200)

# Создаём кнопку "Создать базу"
buttonCreateBase = Button(window, text="Создать базу данных", command=OnButtonCreateBase, justify=RIGHT)

# Настраиваем её расположение
buttonCreateBase.grid(row=2, column=2)
buttonCreateBase.place(x=200, y=200)

# Запускаем основной поток приложение
window.mainloop()
