import numpy as np
import cv2
import binascii

def text_to_bits(text, encoding='utf-8', errors='error'):
    '''
    hàm chuyển text thành chuỗi bit
    '''
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

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
eightbit_img = np.reshape(eightbitimg,(row,col))
cv2.imwrite("origin_images/8bitvalue(MBS).jpg" , eightbit_img )

# lưu ảnh bit plane thứ 7
sevenbit_img = np.reshape(sevenbitimg,(row,col))
cv2.imwrite("origin_images/7bitvalue.jpg",sevenbit_img)

# lưu ảnh bit plane thứ 6
sixbit_img = np.reshape(sixbitimg,(row,col))
cv2.imwrite("origin_images/6bitvalue.jpg",sixbit_img)

# lưu ảnh bit plane thứ 5
fivebit_img = np.reshape(fivebitimg,(row,col))
cv2.imwrite("origin_images/5bitvalue.jpg",fivebit_img)

# lưu ảnh bit plane thứ 4
fourbit_img = np.reshape(fourbitimg,(row,col))
cv2.imwrite("origin_images/4bitvalue.jpg",fourbit_img)

# lưu ảnh bit plane thứ 3
threebit_img = np.reshape(threebitimg,(row,col))
cv2.imwrite("origin_images/3bitvalue.jpg",threebit_img)

# lưu ảnh bit plane thứ 2
twobit_img = np.reshape(twobitimg,(row,col))
cv2.imwrite("origin_images/2bitvalue.jpg",twobit_img)

# lưu ảnh bit plane thứ 1
onebit_img = np.reshape(onebitimg,(row,col))
cv2.imwrite("origin_images/1bitvalue(LBS).jpg",onebit_img)

# ảnh grayscale của ảnh gốc
gray = cv2.imread("origin_images/spiderman-miles-lost-in-space-4k-0f.jpg",cv2.IMREAD_GRAYSCALE)
cv2.imwrite("origin_images/gray.jpeg",gray)

# giấu tin vào ảnh LBS

# đọc message và nén vào ảnh
embed_message = open("messages/message.txt", "r").read()
bit_messsage = text_to_bits(embed_message)
embedded_list = []

for i in range(row*col):
    if i < len(bit_messsage):
        embedded_list.append(int(bit_messsage[i]))
    else:
        embedded_list.append(0)

embedded = np.array(embedded_list) * 1
embeddedimg = np.reshape(embedded,(row,col))
cv2.imwrite("origin_images/embedded_image.jpg" , embeddedimg )

combine = eightbitimg + sevenbitimg + sixbitimg + fivebitimg + fourbitimg + threebitimg + twobitimg + embedded
comb = np.reshape(combine,(row,col))
# lưu ảnh gộp
cv2.imwrite("origin_images/embedded_comb.png",comb)

