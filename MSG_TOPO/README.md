# Multi-Scale Guided convolutional network (MSG)

## Hierarchy
- src <br>
  - depth_utils: original implementation from voyleg, could be potentially useful for further research regarding uncertainty, etc. Not used in this project though.
  - losses: original implementation from voyleg, could be potentially useful for further research regarding visaully favored loss function.
  - msg: backbone of the neural network.


- TEST_simple_geometry.ipynb
  test on the simple geometry dataset with fine plotting.
- TEST_topo.ipynb
  first test only one image, then implement a pipeline to automatically analyze all the images in the indicated data folder. Some uncommenting is needed if want to switch data folder.
