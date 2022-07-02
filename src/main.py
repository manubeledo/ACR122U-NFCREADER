import nfc
import time

reader = nfc.Reader()
reader.print_data(reader.get_uid()) 

# reader.print_data(reader.get_uid())
# reader.info()
