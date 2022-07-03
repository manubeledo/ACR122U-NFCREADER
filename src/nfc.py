import smartcard.System
from smartcard.util import toHexString
from smartcard.ATR import ATR
import time

import utils, option, error

class Reader:
    def __init__(self):
        """create an ACR122U object
        doc available here: http://downloads.acs.com.hk/drivers/en/API-ACR122U-2.02.pdf"""
        self.reader_name, self.connection = self.instantiate_reader()

    @staticmethod
    def instantiate_reader():
        readers = smartcard.System.readers()

        if len(readers) == 0:
            raise error.NoReader("No readers available")

        reader = readers[0]
        c = reader.createConnection()
        i = 0 

        while (i == 0) : 
            try:
                c.connect() 
            except:
                time.sleep(0.1)
                print ('Waiting card...')
            else:
                print ('Everything OK')
                i = 1

        return reader, c

    def command(self, mode, arguments=None):

        mode = option.alias.get(mode) or mode
        payload = option.options.get(mode)

        payload = utils.replace_arguments(payload, arguments)
        result = self.connection.transmit(payload)
        print('este es el resultado', result)


        """ACA SE GUARDA LA DATA QUE VIENE DE RESULT"""

        if len(result) == 3:
            data, sw1, sw2 = result
        else:
            data, n, sw1, sw2 = result

        if [sw1, sw2] == option.answers.get("fail"):
            raise error.InstructionFailed(f"Instruction {mode} failed")

        print(f"success: {mode}")
        if data:
            return data

        if [sw1, sw2] != option.answers.get("success"):
            return sw1, sw2

    def get_uid(self):
        """get the uid of the card"""
        return self.command("get_uid")

    @staticmethod
    def print_data(data):
        print(f"data:\n\t{data}")
        return

    @staticmethod
    def print_sw1_sw2(sw1, sw2):
            print(f"sw1 : {sw1} {hex(sw1)}\n"
                  f"sw2 : {sw2} {hex(sw2)}")
