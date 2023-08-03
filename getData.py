# to get and store data 


import entsoeAPI as e

def optionToFile(opt):
    return opt["country"]+"-"+opt["start"]+"-"+opt["end"]

def test():
    option1 = {"start":"202301010000","end":"202301020000","country":"DE"}
    option2 = {"start":"202301010000","end":"202303010000","country":"DE"}

    print()
    a = e.getActualRenewableValues(option1)
    a.to_csv("./test/"+optionToFile(option1)+".csv")

    b = e.getActualRenewableValues(option2)
    b.to_csv("./test/"+optionToFile(option2)+".csv")

test()