from PIL import Image

def convertToBinary(data):
    new_data = []
    data += 'endmsg'
    for i in data:
        new_data.append(format(ord(i), '08b'))
    return new_data

def saveFile(img_input, file_input):
    file, extension = img_input.split('.')
    file += 'copy.' + extension
    file_input.save(file)

def dataGet(img):
    w, h = img.size
    x = 0
    y = 0
    data = []
    for i in range(400):
        coord = (x, y)
        data.append(img.getpixel(coord))
        if y < h:
            y += 1
        else:
            x += 1
            y = 0
    return data

def dataPut(img, msg_encrypt):
    w, h = img.size
    x = 0
    y = 0
    for i in msg_encrypt:
        coord = (x, y)
        img.putpixel(coord, i)
        if y < h:
            y += 1
        else:
            x += 1
            y = 0
    return img

def encrypt():
    msg = input('Enter the message you would like encoded: ')
    msg_list = convertToBinary(msg)
    msg_len = len(msg_list)
    img_input = input('Enter image name(with extension) : ')
    img = Image.open(img_input, 'r')
    img_data = iter(dataGet(img))
    msg_encrypt = []

    for i in range(msg_len):
        pixel = [p for p in next(img_data) + next(img_data)]
        for j in range(8):
            if msg_list[i][j] == '0' and pixel[j] % 2 != 0:
                if pixel[j] == 0:
                    pixel[j] += 1
                else:
                    pixel[j] -= 1
            elif msg_list[i][j] == '1' and pixel[j] % 2 == 0:
                if pixel[j] == 0:
                    pixel[j] += 1
                else:
                    pixel[j] -= 1

        msg_encrypt.append(tuple(pixel[:4]))
        msg_encrypt.append(tuple(pixel[4:8]))

    dataPut(img, msg_encrypt)
    saveFile(img_input, img)
    print('Message encryption sucessful.')

def decrypt():
    image = input('Enter image name(with extension) : ')
    img = Image.open(image)
    img_data = iter(dataGet(img))
    msg = ''
    cont = True
    while cont == True:
        pixel = [p for p in next(img_data) + next(img_data)]
        bin_temp = ''
        for j in range(8):
            if pixel[j] % 2 == 0:
                bin_temp += '0'
            else:
                bin_temp += '1'
        msg += chr(int(bin_temp, 2))
        index = msg.find('endmsg')
        if index > 0:
            cont = False
    print('Decoded message: ', msg[:index])

def main():
    cmd = input('Would you like to (1) encrypt? or (2) decrypt? ')
    if cmd == '1':
        encrypt()
    elif cmd == '2':
        decrypt()
    else:
        print('You did not enter a valid command.')

if __name__ == "__main__":
    main()