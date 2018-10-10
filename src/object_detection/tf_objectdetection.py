print('tf_objectdetection loading...')
import sys
import os
import common
import zipfile
import base64
bucket = 'samplebucket-suzuki'

def myimport(zipkey):
  temppath = os.path.join('/tmp', os.path.basename(zipkey))
  tempdir = os.path.splitext(temppath)[0]
  if not os.path.exists(tempdir):
    print('downloading ', zipkey)
    os.makedirs(tempdir)
    common.download_s3file(bucket,zipkey,temppath)
    with zipfile.ZipFile(temppath) as existing_zip:
      existing_zip.extractall(tempdir)
  else:
    print('already exist ',zipkey)
  sys.path.append(tempdir)

#def module_import():
print('modules importing...')
myimport('lib/numpy.zip')
import numpy as np
myimport('lib/tensorflow.zip')
import tensorflow as tf
myimport('lib/PIL.zip')
import PIL.Image as Image
sys.path.append(".")
from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util

threshold = float(os.environ.get('threshold','0.08'))

MODEL_INFO = {
  'bucket'      : 'samplebucket-suzuki',
  'model_key'   : os.environ.get('model_key','lib/object_detection_model/mahjong/ssdlite_mobilenet_v2.pb'),
  'label_key'   : os.environ.get('label_key','lib/object_detection_model/mahjong/label_map.pbtxt'),
  'model_path'  : '/tmp/frozen_inference_graph.pb',
  'label_path'  : '/tmp/label_map.pbtxt',
  'num_class'   : int(os.environ.get('num_class','40'))
}
def model_download():
  print('model downloading...')
  common.download_s3file(bucket,MODEL_INFO['model_key'],MODEL_INFO['model_path'])
  common.download_s3file(bucket,MODEL_INFO['label_key'],MODEL_INFO['label_path'])

class image_classifier():
    def __init__(self, model_info):
        detection_graph = tf.Graph()
        with detection_graph.as_default():
          od_graph_def = tf.GraphDef()
          with tf.gfile.GFile(MODEL_INFO['model_path'], 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
            
          self.session = tf.Session(graph=detection_graph)
          # Get handles to input and output tensors
          ops = detection_graph.get_operations()#tf.get_default_graph().get_operations()
          all_tensor_names = {output.name for op in ops for output in op.outputs}
          self.tensor_dict = {}
          for key in ['num_detections', 'detection_boxes', 'detection_scores','detection_classes']:
            tensor_name = key + ':0'
            if tensor_name in all_tensor_names:
              self.tensor_dict[key] = detection_graph.get_tensor_by_name(tensor_name)#tf.get_default_graph().get_tensor_by_name(tensor_name)
          self.image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
          
          print('creating label_map.')
          label_map = label_map_util.load_labelmap(model_info['label_path'])
          #print(label_map)
          categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=model_info['num_class'], use_display_name=True)
          #print(categories)
          self.category_index = label_map_util.create_category_index(categories)
          
          
    def run_inference(self,imagetensor):
          output_dict = self.session.run(self.tensor_dict,
                                 feed_dict={self.image_tensor: imagetensor})#np.expand_dims(image, 0)})

          # all outputs are float32 numpy arrays, so convert types as appropriate
          output_dict['num_detections']    = int(output_dict['num_detections'][0])
          output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
          output_dict['detection_boxes']   = output_dict['detection_boxes'][0]
          output_dict['detection_scores']  = output_dict['detection_scores'][0]
          return output_dict
    def get_image_tensor(self,image_path):
        image = Image.open(image_path)
        (im_width, im_height) = image.size
        image_np = np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)
        #image_np_expanded = np.expand_dims(image_np, axis=0)
        return image_np
    def run_inference_file(self,image_path):
        print('run_inference_file',image_path)
        image_tensor = self.get_image_tensor(image_path)
        image_tensor = np.expand_dims(image_tensor, axis=0)
        output_dict = self.run_inference(image_tensor)
        boxes   = output_dict['detection_boxes'][:output_dict['num_detections']]
        classes = output_dict['detection_classes'][:output_dict['num_detections']]
        scores  = output_dict['detection_scores'][:output_dict['num_detections']]
        #result = [(category_index[clsid]['name'],score,box.tolist()) for (clsid,score,box) in zip(classes,scores,boxes)]
        #print(result)
        results = []
        for idx in range(output_dict['num_detections']):
          print(self.category_index[classes[idx]]['name'],'{0:.3f}'.format(scores[idx]),boxes[idx].tolist())
          if threshold > scores[idx]:
            continue
          result = {
            'Name':self.category_index[classes[idx]]['name'],
            'Confidence':'{0:.3f}'.format(scores[idx]),
            'Box':{
              'xmin': '{0:.3f}'.format(boxes[idx].tolist()[0]),
              'ymin': '{0:.3f}'.format(boxes[idx].tolist()[1]),
              'xmax': '{0:.3f}'.format(boxes[idx].tolist()[2]),
              'ymax': '{0:.3f}'.format(boxes[idx].tolist()[3])
            }
          }
          results.append(result)
        
        return results

print('module preparing...')
model_download()
#module_import()
classifier = image_classifier(MODEL_INFO)

'''
classifier = None
def initializer():
  if not os.path.exists(MODEL_INFO['model_path']):
    model_download()
  module_import()
  if classifier == None:
    classifier = image_classifier(MODEL_INFO)
'''
  
def handler(event):
    
    httpMethod = event['httpMethod']
    resourcePath = event.get('path','')
    queryStrings = event.get('queryStringParameters',None)
    targetKey = event['queryStringParameters'].get('model','') if queryStrings != None else ''
    print('{}:{}/{}'.format(httpMethod,resourcePath,targetKey))

    response = ''
    if httpMethod == 'POST':
        imageBody = base64.b64decode(event["body"])
        tmp_file = '/tmp/target.jpg'
        with open(tmp_file,"wb") as f:
          f.write(imageBody)
        
        #im = Image.open(tmp_file)
        #print('image size:{}, mode:{}, format:{}'.format(im.size,im.mode,im.format))
        results = classifier.run_inference_file(tmp_file)
        print(results)
        response = results

        response = common.create_response(common.OK, response)
    else:
        response = common.create_response(common.METHOD_NOT_ALLOWED)
    return response


