#include <sys/types.h>
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h> // for sleep()

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <chrono>

#include "MulticastHeader.h"
#include <lzo/lzo1z.h>

bool DecompressBufferData(BCastCmpPacket* data, char *in_buffer)
{
	memset(in_buffer,0,65536);
	lzo_uint in_len = 0  ;
	auto compLen = __builtin_bswap16(data->iCompLen) ;

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


int main(int argc, char *argv[])
{
    if (argc != 4) {
       printf("Command line args should be multicast group and port and filename\n");
       printf("(e.g. for SSDP, `sender 239.255.255.250 1900`)\n");
       return 1;
    }
    std::ifstream m_SnapShotFileR;
    m_SnapShotFileR.open(argv[3], std::ios::in | std::ios::binary);

    char* group = argv[1]; // e.g. 239.255.255.250 for SSDP
    int port = atoi(argv[2]); // 0 if error, which is an invalid port

    // !!! If test requires, make these configurable via args
    //
    const int delay_secs = 1;

    // create what looks like an ordinary UDP socket
    //
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) {
        perror("socket");
        return 1;
    }

    // set up destination address
    //
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr(group);
    addr.sin_port = htons(port);

    char publish_buffer[512];
    char decompressed_buffer[65536];

    while(1) {

        while (m_SnapShotFileR.good()) {

            memset(publish_buffer, '\0', 512);
            m_SnapShotFileR.read(publish_buffer, 512);
    
            BCastPackData *bcast_pack_data = reinterpret_cast<BCastPackData *>(publish_buffer);
            BCastCmpPacket *bcast_cmp_packet = reinterpret_cast<BCastCmpPacket *>(bcast_pack_data->cPackData);
            auto complen = __builtin_bswap16(bcast_cmp_packet->iCompLen);
            std::cout << "Complen is " << complen << std::endl; 
            if(complen > 0){
                if(DecompressBufferData( bcast_cmp_packet, decompressed_buffer)) {
                    printf("Decompressed Succesfully...\n");
                }
                else {
                    printf("Failed To Decompress..\n");
                    exit(-1);
                }
            }
            else {
                memset(decompressed_buffer, '\0', 512);
                memcpy(decompressed_buffer, publish_buffer, 512);
                printf("Recieved Non-Compressed Buffer...\n");
            }

            /*auto bcast_header = reinterpret_cast<BCAST_HEADER*>(decompressed_buffer + 8);
            auto transcode = __builtin_bswap16(bcast_header->transactionCode); 
            auto msTickerIndex = reinterpret_cast<MS_BCAST_ONLY_MBP*>(decompressed_buffer);
            std::cout << "Transaction Code is " << transcode << std::endl;
            std::cout << "MsTickerIndex no. of records is " << __builtin_bswap16(msTickerIndex->noOfRecords)<< std::endl;
            auto interactive = msTickerIndex->interactiveData[0];
            auto token = __builtin_bswap32(interactive.token);
            std::cout << "Token is " << token << std::endl;*/

            int nbytes = sendto(
                    fd,
                    publish_buffer,
                    512,
                    0,
                    (struct sockaddr*) &addr,
                    sizeof(addr)
            );

            if (nbytes < 0) {
                perror("sendto");
                return 1;
            }
            printf("Sent %d bytes\n", nbytes);
            sleep(delay_secs); // Unix sleep is seconds
        }   
    m_SnapShotFileR.clear();
    m_SnapShotFileR.seekg(0);
    }
}

