MODEL_INFO = {
  'bucket'      : 'uswestbucket-suzuki',
  'model_key'   : os.environ.get('model_key','lib/object_detection_model/mahjong/ssdlite_mobilenet_v2.pb'),
  'label_key'   : os.environ.get('label_key','lib/object_detection_model/mahjong/label_map.pbtxt'),
  'model_path'  : '/tmp/frozen_inference_graph.pb',
  'label_path'  : '/tmp/label_map.pbtxt',
  'num_class'   : int(os.environ.get('num_class','40'))
}