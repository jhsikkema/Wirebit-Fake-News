import os, os.path

class ModelConst(object):
	VERSION	       = ("model", "version")
	TYPE	       = ("model", "type")
	BASE_PATH      = ("model", "path")
	PLATFORM_ALL   = "all"
	
	TYPE_ANN       = "ann"
	TYPE_HEURISTIC = "heuristic"
	
	ANN_LAYERS     = ("model", "ann", "layers")
	ANN_EPOCHS     = ("model", "ann", "epochs")
	ANN_BATCHSIZE  = ("model", "ann", "batchsize")

	
