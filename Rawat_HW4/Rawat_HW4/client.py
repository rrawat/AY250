#Client

#import SimpleXMLRPCServer
from PIL import Image
import numpy as np
import pickle
  

import xmlrpclib

port = 8201
s = xmlrpclib.ServerProxy('http://localhost:%i' % port)

# PIL to array and array to PIL functions
def PIL2array(img):
	"""takes in a PIL instance and returns an array"""
	return np.array(img.getdata(),
					np.uint8).reshape(img.size[1], img.size[0], 3)

def array2PIL(arr, size):
	"""takes in an array and returns a PIL instance"""
	mode = 'RGBA'
	arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
	if len(arr[0]) == 3:
		arr = np.c_[arr, 255*np.ones((len(arr),1), np.uint8)]
	return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)


#take in a user-determined path (These two are the ones in the folder and can be used as demos)


file='demo_color.png'
#file='demo_bw.jpg'

#even if the file is B/W, the functions will work on it when converted to RGB

orig_img=Image.open(file).convert("RGB")
orig_img_size=orig_img.size
orig_img_array=PIL2array(orig_img)


class imagestring:
	"""combines information that will be sent from client to server"""
	def __init__(self, nparray, size,name):
		"""instantiate the class, include all information that has to be sent to the server: the img array, its size, and the desired root filename"""
		self.img_array=nparray
		self.img_size=size
		self.filename='%s' %str(name)

##inputs=everything that must get passed to the server
inputs = imagestring(orig_img_array, orig_img_size,file)

pickledinstance=pickle.dumps(inputs)


print "sending to server"

#send to the server	

pickled_rot90_img, rot90_img_array_size = s.turn90(pickledinstance)


rot90_img_array=pickle.loads(pickled_rot90_img)
rot90_img_size=(rot90_img_array_size[0],rot90_img_array_size[1])
rot90_img=array2PIL(rot90_img_array, rot90_img_size)
rot90_img.save("server/%s_%s" %('rot90_client',file), "JPEG")

#start reconstruction
rot90_reconst_img=rot90_img.rotate(270)
rot90_reconst_img.save("server/%s_%s" %('rot90_reconst_client',file), "JPEG")



####

pickled_rot270_img, rot270_img_array_size = s.rot270(pickledinstance)


rot270_img_array=pickle.loads(pickled_rot270_img)
rot270_img_size=(rot270_img_array_size[0],rot270_img_array_size[1])
rot270_img=array2PIL(rot270_img_array, rot270_img_size)
rot270_img.save("server/%s_%s" %('rot270_client',file), "JPEG")

#start reconstruction
rot270_reconst_img=rot270_img.rotate(90)
rot270_reconst_img.save("server/%s_%s" %('rot270_reconst_client',file), "JPEG")

####

pickled_transposed_img, transposed_img_array_size = s.transpose(pickledinstance)


transposed_img_array=pickle.loads(pickled_transposed_img)

transposed_img_size=(transposed_img_array_size[0],transposed_img_array_size[1])
transposed_img=array2PIL(transposed_img_array, transposed_img_size)
transposed_img.save("server/%s_%s" %('transposed_client',file), "JPEG")

#start reconstruction
transposed_reconst_img=transposed_img.transpose(Image.FLIP_LEFT_RIGHT)
transposed_reconst_img.save("server/%s_%s" %('transposed_reconst_client',file), "JPEG")


####
print "files have been saved"






