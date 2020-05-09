#coding:utf-8

import random
import json    #用于保存settings
import os      #用于获取AppData目录和新建目录

def encode(num):
	#加密，接收int，返回str
	addNumber=random.randint(1,9)
	subNumber=random.randint(1,9)
	mulNumber=random.randint(1,9)
	result=str(num-subNumber*mulNumber+addNumber)+str(subNumber)+str(mulNumber)+str(addNumber)
	return result

def decode(num):
	#解密，接收int,返回str
	addetunum=str(num)[-1]
	subetunum=str(num)[-3]
	divetunum=str(num)[-2]
	lennum=len(str(num))
	isNum=str(num)[0:lennum-3]
	result=str(int(isNum)-int(addetunum)+int(subetunum)*int(divetunum))
	return result

def getText(language = '中文'):
	#引用文字的字典
	zh = {
	'welcome': '====================\n欢迎使用NUAEDC\n版本号：v2.0.0\n====================',
	'help': '命令列表：\n1.enc - 加密\n2.dec - 解密\n3.lan - 切换语言（Change Language）\n4.? - 帮助\n5.exit - 退出',
	'numberInput': '输入数字：',
	'switchLanguage': '中文/en：',
	'codeError': '失败。请输入一个整数。',
	'languageNotFound': '未找到该语言。'
	}
	en = {
	'welcome': '====================\nwelcome to NUAEDC\nversion: v2.0.0\n====================',
	'help': 'Command List:\n 1.enc - Encode\n2.dec - Decode\n3.lan - Change Language(切换语言)\n4.? - help\n5.exit - exit',
	'numberInput': 'Input number: ',
	'switchLanguage': '中文/en: ',
	'codeError': 'FAILED. Please input a integer.',
	'languageNotFound': 'Failed to find this language.'
	}
	if language == 'en':
		return en
	elif language == '中文':
		return zh
	#语言没对上就报错，回去except
	raise NotImplementError("Language Not Found")

def commandList():
	#命令表
	return {
	'encode': ['1', '加密', 'enc'],
	'decode': ['2', '解密', 'dec'],
	'switchLanguage': ['3', '切换语言', 'lan', 'language'],
	'help': ['4', 'help', '?', '？', '帮助'],
	'exit': ['5', '退出', 'exit'],

	'languages': {
	'中文': ['zh', 'cn', '中文', 'Chinese', 'zhcn', 'zh-cn'],
	'en': ['en', 'English', '英文']
	}

	}

def getInput(command,Text):
	#从命令中获取参数，失败就提示输入
	try:
		arg = command[1]
	except:
		arg = input(Text)
	return arg

def isNotCommand(command, language):
	#命令识别失败
	if language == '中文':
		print('不存在命令“' + command + '”。')
	else:
		print('Command "' + command + '" not found.')

def writeSettings(Setting,file):
	json.dump(Setting, file)

def getSettings(Path):
	#从Path指定的文件读取设置
	defautSetting = {
	'language': '中文'
	}
	if not os.path.exists(os.path.split(Path)[0]):    #判断目录是否存在，用os.path.split分离路径中目录与文件名
		os.mkdir(os.path.split(Path)[0])
	fSetting = open(Path, 'a+')
	fSetting.seek(0, 0)       #把文件指针放到文件开头
	setting = fSetting.read()
	if setting == '':
		writeSettings(defautSetting, fSetting)
		fSetting.close()
		return defautSetting
	fSetting.close()
	return json.loads(setting)


if __name__ == "__main__":    #排除被import时

	#初始化文本，命令表和语言
	settingsPath = os.getenv('APPDATA') + '\\NUAEDC\\settings.json'
	settings = getSettings(settingsPath)
	commands = commandList()
	text = getText(settings['language']) 

	print(text['welcome'])    #欢迎
	print(text['help'])

	while True:
		command = input('>>>').split(' ',1)
		command[0] = command[0].lower()    #命令转为小写，便于匹配

		#识别命令

		#避免空行造成程序退出
		if command[0] == '':
			continue

		elif command[0] in commands['encode']:
			try:
				num = getInput(command, text['numberInput'])
				print(encode(int(num)))
			except:
				print(text['codeError'])

		elif command[0] in commands['decode']:
			try:
				num = getInput(command, text['numberInput'])
				print(decode(int(num)))
			except:
				print(text['codeError'])

		elif command[0] in commands['switchLanguage']:
			Tlanguage = getInput(command, text['switchLanguage'])
			succeed = False
			for lan in commands['languages']:
				if Tlanguage in commands['languages'][lan]:
					text = getText(lan)
					settings['language'] = lan
					try:
						fSettings = open(settingsPath, 'w')
						writeSettings(settings, fSettings)
						fSettings.close()
					except:
						pass
					succeed = True
					break
			if succeed == False:
				print(text['languageNotFound'])


		elif command[0] in commands['help']:
			print(text['help'])

		elif command[0] in commands['exit']:
			exit()

		else:
			if command[0] != '':
				isNotCommand(command[0], settings['language'])
