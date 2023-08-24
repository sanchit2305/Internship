#include <sys/types.h>
#include <iostream>
#include <stdlib.h>

#ifdef _WIN32
#define bswap_16(x) _byteswap_ushort(x)
#define bswap_32(x) _byteswap_ulong(x)
#define bswap_64(x) _byteswap_uint64(x)
#else
// Define bswap macros for non-Windows platforms if needed
#endif

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <chrono>

#include "MulticastHeader.h"
#include <lzo/lzo1z.h>

bool DecompressBufferData(BCastCmpPacket* data, char *in_buffer)
{
    memset(in_buffer, 0, 65536);
    lzo_uint in_len = 0;
    auto compLen = (data->iCompLen);

    auto start = std::chrono::steady_clock::now();
    auto isDecompressOK = lzo1z_decompress(
        (uint8_t*)data->cCompData,
        compLen,
        (uint8_t*)in_buffer,
        &in_len,
        NULL
    );
    auto end = std::chrono::steady_clock::now();
    std::cout << "Elapsed time in nanoseconds: "
              << std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count()
              << " ns" << std::endl;

    return isDecompressOK == LZO_E_OK;
}


