from PIL import Image
import numpy as np

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import pickle
import PIL.ImageOps   


class imagestring:
	"""transfers information from client to server"""
	def __init__(self, nparray, size,name):
		"""instantiate the class, include all information that has to be sent to the server: the img array, its size, and the desired root filename"""
		self.img_array=nparray
		self.img_size=size
		self.filename='%s' %str(name)



port = 8201

## Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", port),
							requestHandler=RequestHandler)
server.register_introspection_functions()


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



class MyFunctsClass:
		
	def method1(self, pickledinstance):
		"""convert array to pil, save unchanged version"""

		pobj = pickle.loads(pickledinstance)
		
		orig_array=pobj.img_array
		
		orig_img=array2PIL(orig_array,pobj.img_size)
	
		orig_img.save("server/orig_on_server_%s" %str(pobj.filename), "JPEG") 
		return orig_img, pobj.filename
	
	def turn90(self, pickledinstance):
		"""rotate the image 90deg ccw"""
		#unpack
		orig_img, filename=self.method1(pickledinstance)
		self.method1(pickledinstance)
		#rotate
		rotated_img=orig_img.rotate(90)
		#save
		rotated_img.save("server/%s_%s" %('rot90_img_onserver',str(filename)), "JPEG") 
		
		rotated_img=rotated_img.convert("RGB")
		rotated_img_size=rotated_img.size
		rotated_img_array=PIL2array(rotated_img)
		#repackage to send back
		pickled_array=pickle.dumps(rotated_img_array)
		return pickled_array, rotated_img.size	
		
	def rot270(self, pickledinstance):
		"""rotate the image 270deg ccw"""
 		#unpack
		orig_img, filename=self.method1(pickledinstance)
		#rotate
		rotated_img=orig_img.rotate(270)
		#save
		rotated_img.save("server/%s_%s" %('rot270_img_onserver', str(filename)), "JPEG") 
		rotated_img=rotated_img.convert("RGB")
		rotated_img_size=rotated_img.size
		#package and send back
		rotated_img_array=PIL2array(rotated_img)
				
		pickled_array=pickle.dumps(rotated_img_array)
		
		return pickled_array, rotated_img.size	
		
	def transpose(self, pickledinstance):
 		"""flip the image horizontally"""
		#unpack
		orig_img, filename=self.method1(pickledinstance)
		#flip horizontally
		transposed_img=orig_img.transpose(Image.FLIP_LEFT_RIGHT)
		transposed_img.save("server/%s_%s" %('transposed_img_onserver', str(filename)), "JPEG") 
		
		transposed_img=transposed_img.convert("RGB")
		transposed_img_size=transposed_img.size
		#repack
		transposed_img_array=PIL2array(transposed_img)
				
		pickled_array=pickle.dumps(transposed_img_array)
		#send back
		return pickled_array, transposed_img.size		

server.register_instance(MyFunctsClass())


print "listening on port", port

# Run the server's main loop
server.serve_forever()


