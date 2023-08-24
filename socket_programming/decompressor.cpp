#include <lzo1z.h>
// #include <lzoconf.h>
#include <iostream>

using namespace std;

extern "C" {

void decompress_data(const char* compressed_data, int compressed_size, char* decompressed_data, int* decompressed_size) {
    // Decompress using lzo1z algorithm
    lzo_uint in_len = 0;



    *decompressed_size = static_cast<int>(in_len);
}

}