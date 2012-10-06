import os,sys
import hashlib

class fileGroups():
	checkSumMap = {}
	buckets = {}
	dirRoot = ""
	def __init__(self,dirRoot="/"):
		self.dirRoot = dirRoot
	def getFileList(self,currentPath=""):
		currentPath = currentPath or self.dirRoot
		
		print currentPath
		for dirname, dirnames, filenames in os.walk(currentPath):
			#print dirname, dirnames, filenames
			for filename in filenames:
				curFilePath = os.path.join(dirname, filename)
				statinfo =  os.stat(curFilePath)
				fileInfo = [curFilePath,statinfo,'null']
				if statinfo.st_size not in self.buckets:
					self.buckets[statinfo.st_size] = {'defaultSet':[fileInfo]}
				else:
					self.updateDuplicateFile(fileInfo)
		return self.buckets
				
	def updateDuplicateFile(self,fileInfo):
		fileInfo[2] = self.checkHash(fileInfo[0])
		bucketObj = self.buckets[fileInfo[1].st_size]
		
		if fileInfo[2] in bucketObj:
			bucketObj[fileInfo[2]].append(fileInfo)
		else:
			
			defaultSetObj = bucketObj["defaultSet"][0]
			#print
			#print defaultSetObj
			if defaultSetObj[2] == "null":
				#print defaultSetObj
				defaultSetObj[2] = self.checkHash(defaultSetObj[0])
				#print defaultSetObj
			if defaultSetObj[2] == fileInfo[2]:
				self.buckets[fileInfo[1].st_size]["defaultSet"].append(fileInfo)				
			else:
				self.buckets[fileInfo[1].st_size][fileInfo[2]]=[fileInfo]			
					
	def checkHash(self,curFilePath):
		block_size=2**20
		f = open(curFilePath,'rb')
		md5 = hashlib.md5()
		while True:
			data = f.read(block_size)
			if not data:
				break
			md5.update(data)
		return md5.digest()
		
		
def onExecute(args=None):	
	if args is None:
		args = sys.argv[1:]
		if args: args= args[0]
	if not args: args = raw_input('enter the folder path:')
	getFiles = fileGroups(dirRoot=args)
	
	print getFiles.getFileList()
		
		
	
if __name__ == "__main__":
	onExecute()
        