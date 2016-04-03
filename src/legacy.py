# legacy.py  17/03/2016  D.J.Whale
#
# Note: This is a test harness only, to prove that the underlying OOK
# radio support for legacy plugs is working.
# Please don't use this as a basis for building your applications from.
# Another higher level device API will be designed once this has been
# completely verified.

import time

from energenie import encoder
from energenie import radio


#----- TEST APPLICATION -------------------------------------------------------

# Prebuild all possible message up front, to make switching code faster

HOUSE_ADDRESS = None # default

ALL_ON     = encoder.build_switch_msg(True,                    house_address=HOUSE_ADDRESS)
ONE_ON     = encoder.build_switch_msg(True,  device_address=1, house_address=HOUSE_ADDRESS)
TWO_ON     = encoder.build_switch_msg(True,  device_address=2, house_address=HOUSE_ADDRESS)
THREE_ON   = encoder.build_switch_msg(True,  device_address=3, house_address=HOUSE_ADDRESS)
FOUR_ON    = encoder.build_switch_msg(True,  device_address=4, house_address=HOUSE_ADDRESS)
ON_MSGS    = [ALL_ON, ONE_ON, TWO_ON, THREE_ON, FOUR_ON]

ALL_OFF    = encoder.build_switch_msg(False,                   house_address=HOUSE_ADDRESS)
ONE_OFF    = encoder.build_switch_msg(False, device_address=1, house_address=HOUSE_ADDRESS)
TWO_OFF    = encoder.build_switch_msg(False, device_address=2, house_address=HOUSE_ADDRESS)
THREE_OFF  = encoder.build_switch_msg(False, device_address=3, house_address=HOUSE_ADDRESS)
FOUR_OFF   = encoder.build_switch_msg(False, device_address=4, house_address=HOUSE_ADDRESS)
OFF_MSGS   = [ALL_OFF, ONE_OFF, TWO_OFF, THREE_OFF, FOUR_OFF]


def get_yes_no():
    """Get a simple yes or no answer"""
    answer = raw_input() # python2
    if answer.upper() in ['Y', 'YES']:
        return True
    return False


def legacy_learn_mode():
    """Give the user a chance to learn any switches"""
    print("Do you want to program any switches?")
    y = get_yes_no()
    if not y:
        return

    for switch_no in range(1,5):
        print("Learn switch %d?" % switch_no)
        y = get_yes_no()
        if y:
            print("Press the LEARN button on any switch %d for 5 secs until LED flashes" % switch_no)
            raw_input("press ENTER when LED is flashing")

            for i in range(8):
                print("ON")
                radio.transmit(ON_MSGS[switch_no])
                time.sleep(1)

            print("Device should now be programmed")
            
            print("Testing....")
            for i in range(4):
                time.sleep(1)
                print("OFF")
                radio.transmit(OFF_MSGS[switch_no])
                time.sleep(1)
                print("ON")
                radio.transmit(ON_MSGS[switch_no])
            print("Test completed")


def legacy_switch_loop():
    """Turn all switches on or off every few seconds"""

    while True:
        for switch_no in range(5):
            # switch_no 0 is ALL, then 1=1, 2=2, 3=3, 4=4
            # ON
            print("switch %d ON" % switch_no)
            radio.transmit(ON_MSGS[switch_no])
            time.sleep(2)

            # OFF
            print("switch %d OFF" % switch_no)
            radio.transmit(OFF_MSGS[switch_no])
            time.sleep(2)
        

def pattern_test():
    """Test all patterns"""
    while True:
        p = raw_input("number 0..F")
        p = int(p, 16)
        msg = encoder.build_test_message(p)
        print("pattern %s payload %s" % (str(hex(p)), encoder.ashex(msg)))
        radio.transmit(msg)
            

if __name__ == "__main__":

    print("starting legacy switch tester")
    print("radio init")
    radio.init()
    print("radio as OOK")
    radio.transmitter(ook=True)

    try:
        #pattern_test()
        #legacy_learn_mode()
        legacy_switch_loop()

    finally:
        radio.finished()


# END

