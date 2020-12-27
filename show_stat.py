import yt
import My_Plugin as M

#ds = yt.load(input("Input data loaction: "))

ds = yt.load('/data/yhlin/Sedov/sedov_hdf5_chk_0001')
ds.print_stats()

print(ds.field_list)
