import pandas as pd

'''
DATA SOURCES
'''
raw_df = pd.read_csv('../data/college-scorecard.csv', sep=',',
                     dtype={'ZIP': str,
                            'NPCURL': str,
                            'C150_L4_POOLED_SUPP': str,
                            'C150_4_POOLED_SUPP': str,
                            'C200_L4_POOLED_SUPP': str,
                            'C200_4_POOLED_SUPP': str,
                            'ALIAS': str,
                            'T4APPROVALDATE': str
                            })
majors_mapping = pd.read_excel('../data/scorecard-majors-mapping.xlsx')


'''
COLUMN COLLECTIONS
'''
importantColumns = ['INSTNM',           # Institution Name
                    'CITY',             # City
                    'STABBR',           # State Abbreviation
                    'ZIP',              # Zip Code
                    'INSTURL',          # Institution Homepage URL
                    'NPCURL',           # Institution Price Calculator
                    'ADM_RATE_ALL',     # Admission Rate
                    'SAT_AVG_ALL'       # SAT Average
                    ]

dropout_columns = ["REGION",            # Geographic region
                   "ACCREDAGENCY",      # Agency that accredits school
                   "HCM2",              # Under Heightened Cash Monitoring investigation
                   "MAIN",              # Main campus or not
                   "NUMBRANCH",         # # of branch campuses
                   "PREDDEG",           # Predominant degree type
                   "HIGHDEG",           # Highest degree type
                   "CONTROL",           # School ownership type
                   "ST_FIPS",           # State code
                   "LOCALE",            # city/suburb/town/rural TODO normalize?
                   "CCUGPROF",          # Carnegie undergrad profile TODO normalize?
                   "CCSIZSET",          # Carnegie size
                   # RACE FLAGS
                   "HBCU",
                   "PBI",
                   "ANNHI",
                   "TRIBAL",
                   "AANAPII",
                   "HSI",
                   "NANTI",
                   "MENONLY",
                   "WOMENONLY",
                   "RELAFFIL",
                   # SCORES & DEGREES
                   "ADM_RATE",
                   "ADM_RATE_ALL",
                   "SATVR25",
                   "SATVR75",
                   "SATMT25",
                   "SATMT75",
                   "SATWR25",
                   "SATWR75",
                   "SATVRMID",
                   "SATMTMID",
                   "SATWRMID",
                   "ACTCM25",
                   "ACTCM75",
                   "ACTEN25",
                   "ACTEN75",
                   "ACTMT25",
                   "ACTMT75",
                   "ACTWR25",
                   "ACTWR75",
                   "ACTCMMID",
                   "ACTENMID",
                   "ACTMTMID",
                   "ACTWRMID",
                   "SAT_AVG",
                   "SAT_AVG_ALL",
                   "PCIP01",
                   "PCIP03",
                   "PCIP04",
                   "PCIP05",
                   "PCIP09",
                   "PCIP10",
                   "PCIP11",
                   "PCIP12",
                   "PCIP13",
                   "PCIP14",
                   "PCIP15",
                   "PCIP16",
                   "PCIP19",
                   "PCIP22",
                   "PCIP23",
                   "PCIP24",
                   "PCIP25",
                   "PCIP26",
                   "PCIP27",
                   "PCIP29",
                   "PCIP30",
                   "PCIP31",
                   "PCIP38",
                   "PCIP39",
                   "PCIP40",
                   "PCIP41",
                   "PCIP42",
                   "PCIP43",
                   "PCIP44",
                   "PCIP45",
                   "PCIP46",
                   "PCIP47",
                   "PCIP48",
                   "PCIP49",
                   "PCIP50",
                   "PCIP51",
                   "PCIP52",
                   "PCIP54",
                   # ENROLLMENT
                   "UGDS",
                   "UG",
                   "UGDS_WHITE",
                   "UGDS_BLACK",
                   "UGDS_HISP",
                   "UGDS_ASIAN",
                   "UGDS_AIAN",
                   "UGDS_NHPI",
                   "UGDS_2MOR",
                   "UGDS_NRA",
                   "UGDS_UNKN",
                   "UGDS_WHITENH",
                   "UGDS_BLACKNH",
                   "UGDS_API",
                   "UGDS_AIANOLD",
                   "UGDS_HISPOLD",
                   "UG_NRA",
                   "UG_UNKN",
                   "UG_WHITENH",
                   "UG_BLACKNH",
                   "UG_API",
                   "UG_AIANOLD",
                   "UG_HISPOLD",
                   "PPTUG_EF",
                   # TUITION
                   "NPT4_PUB",
                   "NUM4_PUB",
                   "NUM4_PRIV",
                   "NUM4_PROG",
                   "NUM4_OTHER",
                   "COSTT4_A",
                   "COSTT4_P",
                   "TUITIONFEE_IN",
                   "TUITIONFEE_OUT",
                   "TUITIONFEE_PROG",
                   "TUITFTE",
                   "INEXPFTE",
                   "AVGFACSAL",
                   "PFTFAC",
                   "PCTPELL",
                   # LOAN
                   "DEBT_MDN",
                   "GRAD_DEBT_MDN",
                   "WDRAW_DEBT_MDN",
                   # DETAILS
                   "UG25ABV",                   # percentage 25 or older
                   "DEATH_YR4_RT",              # death rate across 4 yrs
                   "DEATH_YR6_RT",              # death rate across 6 yrs
                   "DEATH_YR8_RT",              # death rate across 8 yrs
                   "PAR_ED_PCT_1STGEN",         # percentage first generation students
                   "DEP_STAT_PCT_IND",          # student is independent
                   "IND_INC_PCT_LO",            # student is independent, family poor
                   "DEP_INC_PCT_LO",            # student is dependent, family poor
                   "AGE_ENTRY",
                   # DEMOGRAPHICS
                   "AGE_ENTRY",
                   "AGE_ENTRY_SQ",
                   "AGEGE24",
                   "FEMALE",
                   "MARRIED",
                   "DEPENDENT",
                   "VETERAN",
                   "FIRST_GEN",
                   "FAMINC",
                   "MD_FAMINC",
                   "FAMINC_IND",
                   "LNFAMINC",
                   "LNFAMINC_IND",
                   "PCT_WHITE",
                   "PCT_BLACK",
                   "PCT_ASIAN",
                   "PCT_HISPANIC",
                   "PCT_BA",
                   "PCT_GRAD_PROF",
                   "PCT_BORN_US",
                   "MEDIAN_HH_INC",
                   "POVERTY_RATE",
                   "UNEMP_RATE",
                   "D_PCTPELL_PCTFLOAN",
                   "UGNONDS",
                   "GRADS",
                   "COUNT_NWNE_P10",
                   "COUNT_WNE_P10",
                   "MN_EARN_WNE_P10",
                   "MD_EARN_WNE_P10",
                   "PCT10_EARN_WNE_P10",
                   "PCT25_EARN_WNE_P10",
                   "PCT75_EARN_WNE_P10",
                   "PCT90_EARN_WNE_P10",
                   "SD_EARN_WNE_P10"
                   ]


def filterForDropout(df):
    RETENTION = "RET_FT4"
    df = df[(df[RETENTION].notnull()) & (df[RETENTION] != 0)]
    df = df.dropna(axis=1, how='any')

    IS_OPERATING = "CURROPER"
    df = df[df[IS_OPERATING] == 1]
    filterByColumn = pd.DataFrame(df, columns=dropout_columns)

    nullCols = filterByColumn.columns[filterByColumn.isnull().sum() > (len(filterByColumn) / 2)].tolist()
    filterByColumn.drop(nullCols, axis=1, inplace=True)

    return filterByColumn

