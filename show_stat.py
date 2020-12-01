import yt

#ds = yt.load(input("Input data loaction: "))
ds = yt.load('./AGNCRe/crbub_hdf5_plt_cnt_0001')
ds.print_stats()
print(ds.field_list)
