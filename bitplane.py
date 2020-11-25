import numpy as np
import cv2
import binascii

def text_to_bits(text, encoding='utf-8', errors='error'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='error'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

# tạo mảng ảnh
img = cv2.imread("origin_images/spiderman-miles-lost-in-space-4k-0f.jpg",0)
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
# hệ số nhân là: 2 ^ (n-1) với n là số bit
# ví dụ, nếu giá trị pixel nhị phân là 11001010 và n = 3, thì factor = 2 ^ (3-1)

# ảnh biểu diễn bit plane thứ 8 (MBS)
eightbitimg = np.array( bitplane(0, imgIn1D ) ) * 128

# ảnh biểu diễn bit plane thứ 7
sevenbitimg = np.array( bitplane(1,imgIn1D) ) * 64

# ảnh biểu diễn bit plane thứ 6
sixbitimg = np.array( bitplane(2,imgIn1D) ) * 32

# ảnh biểu diễn bit plane thứ 5
fivebitimg = np.array( bitplane(3,imgIn1D) ) * 16

# ảnh biểu diễn bit plane thứ 4
fourbitimg = np.array( bitplane(4,imgIn1D) ) * 8

# ảnh biểu diễn bit plane thứ 3
threebitimg = np.array( bitplane(5,imgIn1D) ) * 4

# ảnh biểu diễn bit plane thứ 2
twobitimg = np.array( bitplane(6,imgIn1D) ) * 2

# ảnh biểu diễn bit plane thứ 1 (LBS)
onebitimg = np.array( bitplane(7,imgIn1D) ) * 1

# ảnh gộp lại bởi cả 8 bit plane, tương đương với ảnh gốc ở gray scale
combine = eightbitimg + sevenbitimg + sixbitimg + fivebitimg + fourbitimg + threebitimg + twobitimg + onebitimg
comb = np.reshape(combine,(row,col))

# lưu ảnh gộp
cv2.imwrite("origin_images/comb.jpeg",comb)

# lưu ảnh bit plane thứ 8
eightbitimg = np.reshape(eightbitimg,(row,col))
cv2.imwrite("origin_images/8bitvalue(MBS).jpg" , eightbitimg )

# lưu ảnh bit plane thứ 7
sevenbitimg = np.reshape(sevenbitimg,(row,col))
cv2.imwrite("origin_images/7bitvalue.jpg",sevenbitimg)

# lưu ảnh bit plane thứ 6
sixbitimg = np.reshape(sixbitimg,(row,col))
cv2.imwrite("origin_images/6bitvalue.jpg",sixbitimg)

# lưu ảnh bit plane thứ 5
fivebitimg = np.reshape(fivebitimg,(row,col))
cv2.imwrite("origin_images/5bitvalue.jpg",fivebitimg)

# lưu ảnh bit plane thứ 4
fourbitimg = np.reshape(fourbitimg,(row,col))
cv2.imwrite("origin_images/4bitvalue.jpg",fourbitimg)

# lưu ảnh bit plane thứ 3
threebitimg = np.reshape(threebitimg,(row,col))
cv2.imwrite("origin_images/3bitvalue.jpg",threebitimg)

# lưu ảnh bit plane thứ 2
twobitimg = np.reshape(twobitimg,(row,col))
cv2.imwrite("origin_images/2bitvalue.jpg",twobitimg)

# lưu ảnh bit plane thứ 1
onebitimg = np.reshape(onebitimg,(row,col))
cv2.imwrite("origin_images/1bitvalue(LBS).jpg",onebitimg)

# ảnh grayscale của ảnh gốc
gray = cv2.imread("origin_images/spiderman-miles-lost-in-space-4k-0f.jpg",cv2.IMREAD_GRAYSCALE)
cv2.imwrite("origin_images/gray.jpeg",gray)


# giấu tin vào ảnh LBS

# đọc message và ảnh
embed_message = open("messages/message.txt", "r").read()
print(text_to_bits(embed_message))
print(onebitimg.size)
