import yt
import My_Plugin as M

#ds = yt.load(input("Input data loaction: "))

ds = yt.load('/data/yhlin/CRp_Streaming/crbub_hdf5_plt_cnt_0000')
ds.print_stats()

print(ds.field_list)
