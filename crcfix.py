import zlib
import struct
import argparse
import itertools
print("///\n\
//                          _ooOoo_                          //\n\
//                         o8888888o                         //\n\
//                         88\" . \"88                         //\n\
//                         (| ^_^ |)                         //\n\
//                         O\\  =  /O                         //\n\
//                      ____/`---'\\____                      //\n\
//                    .'  \\\\|     |//  `.                    //\n\
//                   /  \\\\|||  :  |||//  \\                   //\n\
//                  /  _||||| -:- |||||-  \\                  //\n\
//                  |   | \\\\\\  -  /// |   |                  //\n\
//                  | \\_|  ''\\---/''  |   |                  //\n\
//                  \\  .-\\__  `-`  ___/-. /                  //\n\
//                ___`. .'  /--.--\\  `. . ___                //\n\
//               ."" '<  `.___\\_<|>_/___.'  >'"".                //\n\
//            | | :  `- \\`.;`\\ _ /`;.`/ - ` : | |            //\n\
//            \\  \\ `-.   \\_ __\\ /__ _/   .-` /  /            //\n\
//     ========`-.____`-.___\\_____/___.-`____.-'========     //\n\
//                          `=---='                          //\n\
//     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^     //\n\
//                       CTF永不爆零！！！                   //\n\
//\n")
def fix_png_dimensions(input_file, output_file):
    # 读取PNG文件
    bin_data = open(input_file, 'rb').read()
    
    # 计算CRC32
    crc32key = zlib.crc32(bin_data[12:29])  # 计算crc
    original_crc32 = int(bin_data[29:33].hex(), 16)  # 原始crc

    if crc32key == original_crc32:
        print('宽高没有问题!')
        return

    print('宽高被修改了，尝试修复...')

    # 遍历可能的宽高组合
    for i, j in itertools.product(range(4095), range(4095)):
        data = bin_data[12:16] + struct.pack('>i', i) + struct.pack('>i', j) + bin_data[24:29]
        crc32 = zlib.crc32(data)
        if crc32 == original_crc32:
            print(f"\nCRC32: {hex(original_crc32)}")
            print(f"宽度: {i}, hex: {hex(i)}")
            print(f"高度: {j}, hex: {hex(j)}")

            # 修改宽高
            fixed_data = bin_data[:16] + struct.pack('>i', i) + struct.pack('>i', j) + bin_data[24:]
            
            # 写入新的PNG文件
            with open(output_file, 'wb') as f:
                f.write(fixed_data)
            print(f"修复后的PNG文件已保存为: {output_file}")
            return

    print("未能找到正确的宽高组合，修复失败。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, required=True, help="输入PNG文件")
    parser.add_argument("-o", type=str, required=True, help="输出PNG文件")
    args = parser.parse_args()

    fix_png_dimensions(args.f, args.o)