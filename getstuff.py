
import simplejson as json


buttonIDS = []
buttonNames = []


jsonSubIr = open("jsonSubIr").read()
jsonSubIrData = json.loads(jsonSubIr)


for i in range(0, len(jsonSubIrData)):
    print "ID:", jsonSubIrData[i]['id'], "| Name:", jsonSubIrData[i]['name']


choice = input("Select accessory ID: ")

for i in range(0, len(jsonSubIrData)):
    if jsonSubIrData[i]['id'] == choice:
        accessory_name = jsonSubIrData[i]['name']
        print "[+] You selected: ", accessory_name


jsonButton = open("jsonButton").read()
jsonButtonData = json.loads(jsonButton)


for i in range(0, len(jsonButtonData)):
    if jsonButtonData[i]['subIRId'] == choice:
        buttonIDS.append(jsonButtonData[i]['id'])
        buttonNames.append(jsonButtonData[i]['name'])


jsonIrCode = open("jsonIrCode").read()
jsonIrCodeData = json.loads(jsonIrCode)


print "[+] Dumping codes to " + accessory_name + ".txt"
print "[+] Dumping yaml to " + accessory_name + ".yaml"


codesFile = open(accessory_name + '.txt', 'w')
yamlFile = open(accessory_name + '.yaml', 'w')

groupstext = "\n\n\ngroup:\n"
groupstext = groupstext + "  " + accessory_name + ":\n"
groupstext = groupstext + "    name: " + accessory_name + "\n"
groupstext = groupstext + "    view: yes\n"
groupstext = groupstext + "    entities:\n"

yamltext = "    switches:\n"

for i in range(0, len(jsonIrCodeData)):
    for j in range(0, len(buttonIDS)):
        if jsonIrCodeData[i]['buttonId'] == buttonIDS[j]:
            code = ''.join('%02x' % (i & 0xff) for i in jsonIrCodeData[i]['code'])
            code_b64 = code.decode("hex").encode("base64")
            result = "Button Name: " + buttonNames[j] + " | Button ID: " + str(jsonIrCodeData[i]['buttonId']) + " | Code: " + code
            namepart = buttonNames[j].replace(" ","_")
            yamltext = yamltext + "      " + accessory_name + "_" + namepart + ":\n"
            yamltext = yamltext + "        friendly_name: " + accessory_name + " " + buttonNames[j] + "\n"
            yamltext = yamltext + "        command_on: '" + code_b64[:-1] + "'" + "\n"
            groupstext = groupstext + "      - switch." + accessory_name + "_" + namepart + "\n"
            codesFile.writelines(result.encode('utf-8'))
yamlFile.writelines(yamltext.encode('utf-8'))
yamlFile.writelines(groupstext.encode('utf-8'))

