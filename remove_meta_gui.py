from tkinter import filedialog
from tkinter import *
from PIL.ExifTags import TAGS
import tkinter.messagebox as msgbox
from PIL import Image
import os

#기본 세팅
root = Tk()
photo = PhotoImage(file = 'D://etc/python_code/remove_meta_gui/favicon.ico')
root.wm_iconphoto(False, photo)
root.title("메타데이터 제거기 - H4uN")
# root.geometry("540x300+100+100")
# root.geometry("350x100")
# root.resizable(False, False)

dirname = ""
filename = ""
Checkval = IntVar()

# 함수
def dir_ask():
	global dirname
	dirname = filedialog.askdirectory()
	if dirname:
		dir_txt['text'] = '디렉토리 경로 : ' + dirname

def file_ask():
	global filename
	filename = filedialog.askopenfile(
	initialdir='path', 
	title='select file', 
	# filetypes=[('jpg files', '*.jpg')]) 둘다 됨...
	filetypes=(('jpg files', '*.jpg'),))
	if filename:
		filename = filename.name
		file_txt['text'] = "파일 경로 : " + filename

def remove_data_dir(dirname):
	check_val = Checkval.get()
	save_val = 0
	if not dirname:
		msgbox.showwarning("Warning", "경로 선택을 해주세요!")
	else :
		if check_val == 1:
			file_list = os.listdir(dirname)
			msgbox.showinfo("Alert", "잠시만 기다려 주십시오.")
			for file in file_list:
				tmp = dirname + '/' + file
				image = Image.open(tmp)
				for k, v in image._getexif().items():
					if TAGS.get(k, k) == "Orientation":
						save_val = v
				data = list(image.getdata())
				image_new = Image.new(image.mode, image.size)
				image_new.putdata(data)
				exif = image_new.getexif()
				exif[0x0112] = save_val
				image_new.save(tmp, exif=exif)
			msgbox.showinfo("Alert", "회전 방향을 제외한 메타데이터가 삭제 완료되었습니다.")
		else :
			file_list = os.listdir(dirname)
			for file in file_list:
				image = Image.open(dirname + '/' + file).convert('RGB')
				image.save(dirname + '/' + file, 'jpeg')
			msgbox.showinfo("Alert", "메타데이터가 삭제 완료되었습니다.")

def remove_data_fil(filename):
	check_val = Checkval.get()
	save_val = 0
	if not filename:
		msgbox.showwarning("Warning", "경로 선택을 해주세요!")
	else :
		image = Image.open(filename)
		if check_val == 1:
			for k, v in image._getexif().items():
				if TAGS.get(k, k) == "Orientation":
					save_val = v
		data = list(image.getdata())
		image_new = Image.new(image.mode, image.size)
		image_new.putdata(data)
		if check_val == 1:
			exif = image_new.getexif()
			exif[0x0112] = save_val
			image_new.save(filename, exif=exif)
			msgbox.showinfo("Alert", "회전 방향을 제외한 메타데이터가 삭제 완료되었습니다.")
		else :
			image_new.save(filename)
			msgbox.showinfo("Alert", "메타데이터가 삭제 완료되었습니다.")

#디렉토리 프레임
dir_frame = Frame(root)
dir_frame.pack(side="top")

#파일 프레임
file_frame = Frame(root)
file_frame.pack(side="top")

#체크 박스 프레임
check_frame = Frame(root)
check_frame.pack(side="top")

#경로 선택 버튼
btn = Button(dir_frame, text="디렉토리 선택",command=dir_ask)
btn.pack(side=LEFT, padx=10, pady=10)
btn2 = Button(file_frame, text="파일 선택",command=file_ask)
btn2.pack(side=LEFT, padx=10, pady=10)

#라벨
dir_txt = Label(dir_frame, text="디렉토리 경로 : 경로를 선택해 주세요!")
dir_txt.pack(side=LEFT, padx=10, pady=10)
file_txt = Label(file_frame, text="파일 경로 : 파일 경로를 선택해 주세요!")
file_txt.pack(side=LEFT, padx=10, pady=10)

#메타 데이터 제거 버튼
btn3 = Button(dir_frame, text="제거",command=lambda: remove_data_dir(dirname))
btn3.pack(side=LEFT, padx=10, pady=10)
btn4 = Button(file_frame, text="제거",command=lambda: remove_data_fil(filename))
btn4.pack(side=LEFT, padx=10, pady=10)

#회전 체크 박스
Check1 = Checkbutton(check_frame, text="사진 회전 고정(해당 옵션은 시간이 오래 걸릴 수 있습니다)", variable = Checkval)
Check1.pack(side=LEFT, padx=10, pady=10)

root.mainloop()