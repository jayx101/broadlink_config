import simplejson as json  
import base64  
  
buttonIDS = []  
buttonNames = []  
  
# Reading JSON data  
with open("jsonSubIr", "r") as file:  
    jsonSubIrData = json.load(file)  
  
# Printing ID and Name  
for item in jsonSubIrData:  
    print("ID:", item['id'], "| Name:", item['name'])  
  
choice = input("Select accessory ID: ")  
  
accessory_name = ""  
for item in jsonSubIrData:  
    if str(item['id']) == choice:  
        accessory_name = item['name']  
        print("[+] You selected: ", accessory_name)  
  
with open("jsonButton", "r") as file:  
    jsonButtonData = json.load(file)  
  
for item in jsonButtonData:  
    if str(item['subIRId']) == choice:  
        buttonIDS.append(item['id'])  
        buttonNames.append(item['name'])  
  
with open("jsonIrCode", "r") as file:  
    jsonIrCodeData = json.load(file)  
  
print("[+] Dumping codes to " + accessory_name + ".txt")  
print("[+] Dumping yaml to " + accessory_name + ".yaml")  
  
# Writing to files  
with open(accessory_name + '.txt', 'w') as codesFile, open(accessory_name + '.yaml', 'w') as yamlFile:  
    groupstext = "\n\n\ngroup:\n  " + accessory_name + ":\n    name: " + accessory_name + "\n    view: yes\n    entities:\n"  
    yamltext = "    switches:\n"  
  
    for i in range(len(jsonIrCodeData)):  
        for j in range(len(buttonIDS)):  
            if jsonIrCodeData[i]['buttonId'] == buttonIDS[j]:  
                code_hex = ''.join('%02x' % (byte & 0xff) for byte in jsonIrCodeData[i]['code'])  
                code_b64 = base64.b64encode(bytes.fromhex(code_hex)).decode('utf-8')  
                result = "Button Name: " + buttonNames[j] + " | Button ID: " + str(jsonIrCodeData[i]['buttonId']) + " | Code: " + code_hex  
                namepart = buttonNames[j].replace(" ", "_")  
                yamltext += "      " + accessory_name + "_" + namepart + ":\n"  
                yamltext += "        friendly_name: " + accessory_name + " " + buttonNames[j] + "\n"  
                yamltext += "        command_on: '" + code_b64 + "'\n"  
                groupstext += "      - switch." + accessory_name + "_" + namepart + "\n"  
                codesFile.write(result + '\n')  
    yamlFile.write(yamltext)  
    yamlFile.write(groupstext)  