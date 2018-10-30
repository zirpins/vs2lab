import rpc
from context import lab_logging

lab_logging.setup()

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
result_list = cl.append('bar', base_list)

print("Result: {}".format(result_list.value))

cl.stop()
