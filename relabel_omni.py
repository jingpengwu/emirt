import pandas
import numpy as np
import h5py


def make_set_of_segid_to_not_blackout(path_to_segments_txt):
  """
  Reads segments txt exported from omni
  FIXME it is necesary to remove the first two rows manually
  #segID, 1 == working, 2 == valid, 3 == uncertain
  """
  status =  pandas.read_csv(path_to_segments_txt)
  status = np.array(status)

  valid =  set()
  for row in status:  
    _id, stat = row
    if stat == 2:
      valid.add(_id)

  return valid

def blacker(keep_set):
  def pixel_blacker(val):
    if val not in keep_set:
      return 0
    return val

  return np.vectorize(pixel_blacker)


def relabel(mappings):
  def pixel_relabel(val):
    return mappings[ val ]
  return np.vectorize(pixel_relabel)


if __name__ == '__main__':

  with h5py.File('/usr/people/tmacrina/seungmount/Omni/TracerTasks/pinky/ground_truth/stitched_vol19-vol34/seg.h5') as f:
    seg = f['main'][:]
    
    # # comment out this lines if you don't want to blackout anything
    # keep_set = make_set_of_segid_to_not_blackout('/usr/people/tmacrina/seungmount/Omni/TracerTasks/pinky/ground_truth/stitched_vol19-vol34/segments.txt')
    # _blacker =  blacker(keep_set)
    # seg = _blacker(seg)

    otpt = np.zeros(shape=seg.shape, dtype=seg.dtype)
    

    # Create mapping dictionary where key is the old id, and the
    # value is the id to be relabel to
    # we want to enforce the 0 -> 0 mapping
    # and to order the values by the volume of the supervoxel
    unique, unique_counts = np.unique(seg, return_counts=True)
    id_size = zip(unique, unique_counts)
    id_size.sort(key=lambda x: x[1], reverse=True)
    #remove 0 id
    id_size = filter(lambda seg_id_size: seg_id_size[0]!=0, id_size )
    mappings = dict({0:0})
    for new_id, old_id in enumerate(id_size):
      old_id = old_id[0]
      mappings[old_id] = new_id

    _relabel = relabel(mappings)
    seg = _relabel(seg)

    f.create_dataset('relabeled', data=seg)