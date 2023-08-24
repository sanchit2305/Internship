#pragma once
#include <string>
#define MAX_MESSAGE_SIZE 65536 

struct InitStruct
{
	int64_t initVal;
};

#pragma pack(push , 2)
struct LengthHeader
{
    int16_t         length;
    int32_t         sequence_number;
    char            checksum[16];
};
#pragma pack(pop)
#pragma pack(push , 2)
struct MessageHeader
{
    int16_t transaction_code;
    int32_t log_time;
    char    alpha_char[2];
    int32_t error_code;
    int16_t user_id;
    int64_t time_stamp;
    char    time_stamp1[8];
    char    time_stamp2[8];
    int16_t message_length;
};
#pragma pack(pop)
#pragma pack(push , 2)
struct BCAST_HEADER {
	char reserved_1[2];
	char reserved_2[2];
	int32_t LogTime ;
	char alphaChar[2];
	int16_t transactionCode;
	int16_t errorCode;
	int32_t bcSeqNo;
	char reserved_3[1];
	char reserved_4[3];
	char timeStamp2[8];
	char filler2[8];
	int16_t messageLength;

};
#pragma pack(pop)
struct BCastPackData
{
	//LengthHeader    length_Head;
	//MessageHeader header;
	//BCAST_HEADER bCastHeader;
	char cNetId[2] ;
	short iNoPackets ;
	char cPackData [512];
};

struct BCastCmpPacket
{
	short iCompLen;
	char cCompData[MAX_MESSAGE_SIZE] ;
};

#pragma pack(push , 2)
struct ST_TICKER_INDEX_INFO
{
	int32_t token;
	int16_t marketType;
	int32_t fillPrice;
	int32_t fillVolume;
	int32_t openInterest;
	int32_t dayHiOI;
	int32_t dayLoOI;

};
#pragma pack(pop)

#pragma pack(push , 2)
struct MS_TICKER_TRADE_DATA
{
	InitStruct initStruct;
	BCAST_HEADER bcast_header ;
	int16_t	noOfRecords ;
	ST_TICKER_INDEX_INFO stTickerInfo[17];
};
#pragma pack(pop)

#pragma pack(push , 2)
struct ST_INDICATOR
{
	int32_t reserved:4;
	int32_t sell:1;
	int32_t buy:1;
	int32_t lastTradeLess:1;
	int32_t lastTradeMore:1;
	char reserved1;
};
#pragma pack(pop)

#pragma pack(push , 2)
struct ST_MKT_WISE_INFO
{
	ST_INDICATOR stIndicator ;
	int32_t buyVolume;
	int32_t buyPrice;
	int32_t sellVolume;
	int32_t sellPrice;
	int32_t lastTradePrice;
	int32_t lastTradeTime;
};
#pragma pack(pop)

#pragma pack(push , 2)
struct ST_MARKET_WATCH_BCAST
{
	int32_t token;
	ST_MKT_WISE_INFO stMktWiseInfo[3];
	int32_t openInterest ;
};
#pragma pack(pop)

#pragma pack(push , 2)
struct MS_BCAST_INQ_RESP
{
	int16_t noOfRecords ;
	ST_MARKET_WATCH_BCAST stMktWatchBcast[5] ;
};
#pragma pack(pop)
#pragma pack(push , 2)
struct MBP_INFORMATION
{
	int32_t quantity;
	int32_t price;
	int16_t numberOfOrders;
	int16_t bbSellFlag;
};
#pragma pack(pop)
#pragma pack(push , 2)
struct INTERACTIVE_ONLY_MBP_DATA
{
	int32_t token;
	int16_t bookType;
	int16_t tradingStatus;
	int32_t volumeTradedToday;
	int32_t lastTradedPrice ;
	char	netChangeIndicator;
	int32_t netPriceChangeFromClosingPrice;
	int32_t lastTradeQuantity;
	int32_t lastTradeTime;
	int32_t averageTradePrice;
	int16_t auctionNumber;
	int16_t auctionStatus;
	int16_t initiatorType;
	int32_t initiatorPrice;
	int32_t initiatorQuantiy;
	int32_t auctionPrice;
	int32_t auctionQuantity;
	char 	recordBuffer[sizeof(MBP_INFORMATION)*10];
	int16_t bbTotalBuyFlag;
	int16_t bbTotalSellFlag;
	double	totalBuyQuantity;
	double 	totalSellQuantity;
	ST_INDICATOR stIndicator;
	int32_t closingPrice;
	int32_t openPrice;
	int32_t highPrice;
	int32_t lowPrice;
};
#pragma pack(pop)
#pragma pack(push , 2)
struct MS_BCAST_ONLY_MBP
{
	InitStruct initStruct;
	BCAST_HEADER bcast_header ;
	int16_t noOfRecords ;
	INTERACTIVE_ONLY_MBP_DATA interactiveData[2] ;
};
#pragma pack(pop)
#pragma pack(push , 2)
struct SEC_INFO
{
	char instrumentName[6];
	char symbol[10];
	char series[2];
	int32_t expiryDate;
	int32_t strikePrice;
	char optionType[2];
	int16_t caLevel;
};
#pragma pack(pop)
#pragma pack(push , 2)
struct ST_SEC_ELIGIBILITY_PER_MARKET
{
	int16_t reserved:7 ;
	int16_t elegibilty:1 ;
	int16_t status ;
};
#pragma pack(pop)

#pragma pack(push , 2)
struct ST_ELIGIBLITY_INDICATORS
{
	int32_t reserved:5 ;
	int32_t minimumFill:1 ;
	int32_t AON:1 ;
	int32_t participateInMarketindex:1 ;
	char reserved_1;

};
#pragma pack(pop)
#pragma pack(push , 2)
struct ST_PURPOSE
{
	int32_t exerciseStyle:1 ;
	int32_t reserved:1 ;
	int32_t egm:1 ;
	int32_t AGM:1 ;
	int32_t interest:1 ;
	int32_t bonus:1 ;
	int32_t rights:1 ;
	int32_t dividend:1;
	int32_t reserved_1:3;
	int32_t isCorporateAdjusted:1 ;
	int32_t isThisAsset:1 ;
	int32_t piAllowed:1 ;
	int32_t exRejectionAllowed:1;
	int32_t exAllowed:1;	
};
#pragma pack(pop)
#pragma pack(push , 2)
struct MS_SECURITY_UPDATE_INFO
{
	MessageHeader header;
	int32_t token;
	SEC_INFO secInfo;
	int16_t permittedToTrade;
	double issuedCapital;
	int32_t warningQuantity;
	int32_t freezeQuantity;
	char CreditRating[12] ;
	ST_SEC_ELIGIBILITY_PER_MARKET  elegibiltyPerMarket[4]  ;
	int16_t IssueRate ;
	int32_t IssueStartDate ;
	int32_t InterestPaymentDate ;
	int32_t IssueMaturityDate ;
	int32_t MarginPercentage ;
	int32_t MinimumLotQuantity ;
	int32_t BoardLotQuantity ;
	int32_t TickSize ;
	char Name[25];
	char Reserved ;
	int32_t ListingDate ;
	int32_t ExpulsionDate ;
	int32_t ReAdmissionDate ;
	int32_t RecordDate ;
	int32_t LowPriceRange ;
	int32_t HighPriceRange ;
	int32_t ExpiryDate ;
	int32_t NoDeliveryStartDate ;
	int32_t NoDeliveryEndDate ;
	ST_ELIGIBLITY_INDICATORS elegibiltyIndicators ;
	int32_t BookClosureStartDate ;
	int32_t BookClosureEndDate ;
	int32_t ExerciseStartDate ;
	int32_t ExerciseEndDate ;
	int32_t OldToken;
	char AssetInstrument[6] ;
	char AssetName[10] ;
	int32_t AssetToken ;
	int32_t IntrinsicValue ;
	int32_t ExtrinsicValue ;
	ST_PURPOSE stPurpose ;
	int32_t LocalUpdateDateTime ;
	char DeleteFlag ;
	char Remark[25] ;
	int32_t BasePrice ;
};
#pragma pack(pop)
