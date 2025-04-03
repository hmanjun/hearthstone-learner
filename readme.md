Steps for model training:
1) Change VERSION variable in both yolo_annotation_genrator.py and negatives_generator.py to same string
2) Run yolo_annotation_genrator.py then negatives_generator.py
*Failing to do in proper order will prevent negatives from generating



Steps for auto-clipping:
1) Add video file to "data/videos"
*Note update only 'file_name' variable in the below files
2) Run frame_export.py
3) Run y_cord_extractor.py
4) Run velocity_acceleration_finder.py