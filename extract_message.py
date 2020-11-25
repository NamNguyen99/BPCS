import numpy as np
import cv2
import binascii

def text_from_bits(bits, encoding='utf-8', errors='error'):
    '''
    hàm chuyển chuỗi bit thành text
    '''
    n = int(bits, 2)
    return int2bytes(n).decode(encoding)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

# tạo mảng ảnh
img = cv2.imread("origin_images/embedded_comb.png",0)
row ,col = img.shape
# chuyển đổi từng giá trị pixel xen kẽ của hình ảnh thành giá trị pixel 8 bit
def intToBitArray(img) :
    list = []

    for i in range(row):
        for j in range(col):
             list.append (np.binary_repr( img[i][j] ,width=8  ) )

    return list 

imgIn1D = intToBitArray(img)
def bitplane(bitImgVal , img1D ):
    '''
    hàm này trích xuất bit cụ thể ra khỏi mỗi giá trị pixel nhị phân của ma trận
    ví dụ: nếu bitImgVal = 3, thì bit thứ ba của mỗi pixel được trích xuất

    : param bitImgVal: chỉ định vị trí của bit được trích xuất
    : param img1D: hình ảnh sẽ được nén
    : return: trả về danh sách bit 1 chiều
    '''
    bitList = [int(i[bitImgVal]) for i in img1D]

    return bitList

# ảnh biểu diễn bit plane thứ 1 (LBS)
onebitimg = np.array( bitplane(7,imgIn1D) ) * 1
print(onebitimg)

# lấy thông tin từ ảnh LBS
message = ''
for i in range(row*col):
    message += str(onebitimg[i])

print(text_from_bits(message))
