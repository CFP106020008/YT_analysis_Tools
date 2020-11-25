import yt

ds = yt.load(input("Input data loaction: "))
ds.print_stats()
print(ds.field_list)
