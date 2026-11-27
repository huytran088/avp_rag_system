# Generated from Pseudocode.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,55,489,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,1,0,1,0,5,0,67,
        8,0,10,0,12,0,70,9,0,1,0,1,0,1,1,5,1,75,8,1,10,1,12,1,78,9,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,91,8,1,1,1,5,1,94,8,
        1,10,1,12,1,97,9,1,1,2,5,2,100,8,2,10,2,12,2,103,9,2,1,2,1,2,1,2,
        1,2,3,2,109,8,2,1,3,1,3,1,3,1,3,1,3,1,3,3,3,117,8,3,1,4,1,4,1,4,
        5,4,122,8,4,10,4,12,4,125,9,4,1,4,1,4,1,4,5,4,130,8,4,10,4,12,4,
        133,9,4,1,4,1,4,5,4,137,8,4,10,4,12,4,140,9,4,1,4,1,4,1,4,1,4,1,
        4,5,4,147,8,4,10,4,12,4,150,9,4,1,4,1,4,1,4,5,4,155,8,4,10,4,12,
        4,158,9,4,1,4,3,4,161,8,4,1,4,5,4,164,8,4,10,4,12,4,167,9,4,1,4,
        1,4,1,4,1,4,1,4,5,4,174,8,4,10,4,12,4,177,9,4,1,4,3,4,180,8,4,1,
        4,5,4,183,8,4,10,4,12,4,186,9,4,1,4,3,4,189,8,4,1,5,1,5,1,5,1,5,
        3,5,195,8,5,1,5,1,5,1,6,1,6,1,6,5,6,202,8,6,10,6,12,6,205,9,6,1,
        7,1,7,1,8,5,8,210,8,8,10,8,12,8,213,9,8,1,9,1,9,1,9,1,9,3,9,219,
        8,9,1,9,1,9,1,9,4,9,224,8,9,11,9,12,9,225,1,9,1,9,1,9,1,9,1,10,1,
        10,1,10,5,10,235,8,10,10,10,12,10,238,9,10,1,11,5,11,241,8,11,10,
        11,12,11,244,9,11,1,11,1,11,1,12,1,12,5,12,250,8,12,10,12,12,12,
        253,9,12,1,12,3,12,256,8,12,1,12,1,12,1,12,1,12,3,12,262,8,12,1,
        12,1,12,4,12,266,8,12,11,12,12,12,267,1,12,1,12,1,12,1,12,1,13,1,
        13,5,13,276,8,13,10,13,12,13,279,9,13,1,13,1,13,1,13,1,13,1,13,1,
        13,1,13,1,13,1,13,4,13,290,8,13,11,13,12,13,291,1,13,1,13,1,13,1,
        13,1,14,1,14,3,14,300,8,14,1,14,1,14,3,14,304,8,14,1,14,1,14,4,14,
        308,8,14,11,14,12,14,309,1,14,1,14,1,14,1,14,1,15,1,15,3,15,318,
        8,15,1,15,4,15,321,8,15,11,15,12,15,322,1,15,1,15,1,15,1,15,1,15,
        1,15,1,16,1,16,3,16,333,8,16,1,16,1,16,3,16,337,8,16,1,16,1,16,4,
        16,341,8,16,11,16,12,16,342,1,16,1,16,1,16,3,16,348,8,16,1,16,1,
        16,3,16,352,8,16,1,16,1,16,4,16,356,8,16,11,16,12,16,357,1,16,1,
        16,5,16,362,8,16,10,16,12,16,365,9,16,1,16,1,16,1,16,4,16,370,8,
        16,11,16,12,16,371,1,16,3,16,375,8,16,1,16,1,16,1,16,1,17,1,17,1,
        17,3,17,383,8,17,1,17,1,17,1,18,5,18,388,8,18,10,18,12,18,391,9,
        18,1,18,1,18,1,18,1,19,1,19,1,20,1,20,1,21,1,21,1,21,5,21,403,8,
        21,10,21,12,21,406,9,21,1,21,5,21,409,8,21,10,21,12,21,412,9,21,
        1,22,1,22,1,23,1,23,1,23,5,23,419,8,23,10,23,12,23,422,9,23,1,24,
        1,24,1,24,5,24,427,8,24,10,24,12,24,430,9,24,1,25,1,25,1,25,5,25,
        435,8,25,10,25,12,25,438,9,25,1,26,1,26,1,26,5,26,443,8,26,10,26,
        12,26,446,9,26,1,27,1,27,1,27,5,27,451,8,27,10,27,12,27,454,9,27,
        1,28,1,28,1,28,5,28,459,8,28,10,28,12,28,462,9,28,1,29,1,29,1,29,
        3,29,467,8,29,1,30,1,30,1,30,1,30,1,30,1,30,1,30,3,30,476,8,30,1,
        30,1,30,1,30,1,30,1,30,1,30,1,30,3,30,485,8,30,1,31,1,31,1,31,0,
        0,32,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,
        44,46,48,50,52,54,56,58,60,62,0,8,2,0,31,31,53,53,1,0,33,35,1,0,
        49,52,1,0,30,31,2,0,36,37,43,46,1,0,38,39,2,0,41,42,47,47,2,0,22,
        24,49,52,527,0,68,1,0,0,0,2,76,1,0,0,0,4,101,1,0,0,0,6,116,1,0,0,
        0,8,188,1,0,0,0,10,190,1,0,0,0,12,198,1,0,0,0,14,206,1,0,0,0,16,
        211,1,0,0,0,18,214,1,0,0,0,20,231,1,0,0,0,22,242,1,0,0,0,24,247,
        1,0,0,0,26,273,1,0,0,0,28,297,1,0,0,0,30,315,1,0,0,0,32,330,1,0,
        0,0,34,379,1,0,0,0,36,389,1,0,0,0,38,395,1,0,0,0,40,397,1,0,0,0,
        42,399,1,0,0,0,44,413,1,0,0,0,46,415,1,0,0,0,48,423,1,0,0,0,50,431,
        1,0,0,0,52,439,1,0,0,0,54,447,1,0,0,0,56,455,1,0,0,0,58,466,1,0,
        0,0,60,484,1,0,0,0,62,486,1,0,0,0,64,67,3,2,1,0,65,67,5,53,0,0,66,
        64,1,0,0,0,66,65,1,0,0,0,67,70,1,0,0,0,68,66,1,0,0,0,68,69,1,0,0,
        0,69,71,1,0,0,0,70,68,1,0,0,0,71,72,5,0,0,1,72,1,1,0,0,0,73,75,3,
        10,5,0,74,73,1,0,0,0,75,78,1,0,0,0,76,74,1,0,0,0,76,77,1,0,0,0,77,
        90,1,0,0,0,78,76,1,0,0,0,79,91,3,4,2,0,80,91,3,18,9,0,81,91,3,34,
        17,0,82,91,3,24,12,0,83,91,3,26,13,0,84,91,3,30,15,0,85,91,3,32,
        16,0,86,91,3,28,14,0,87,91,3,36,18,0,88,91,3,38,19,0,89,91,3,40,
        20,0,90,79,1,0,0,0,90,80,1,0,0,0,90,81,1,0,0,0,90,82,1,0,0,0,90,
        83,1,0,0,0,90,84,1,0,0,0,90,85,1,0,0,0,90,86,1,0,0,0,90,87,1,0,0,
        0,90,88,1,0,0,0,90,89,1,0,0,0,91,95,1,0,0,0,92,94,7,0,0,0,93,92,
        1,0,0,0,94,97,1,0,0,0,95,93,1,0,0,0,95,96,1,0,0,0,96,3,1,0,0,0,97,
        95,1,0,0,0,98,100,3,10,5,0,99,98,1,0,0,0,100,103,1,0,0,0,101,99,
        1,0,0,0,101,102,1,0,0,0,102,104,1,0,0,0,103,101,1,0,0,0,104,105,
        3,6,3,0,105,108,7,1,0,0,106,109,3,44,22,0,107,109,3,8,4,0,108,106,
        1,0,0,0,108,107,1,0,0,0,109,5,1,0,0,0,110,117,5,49,0,0,111,112,5,
        49,0,0,112,113,5,25,0,0,113,114,3,44,22,0,114,115,5,26,0,0,115,117,
        1,0,0,0,116,110,1,0,0,0,116,111,1,0,0,0,117,7,1,0,0,0,118,119,5,
        6,0,0,119,123,5,25,0,0,120,122,5,53,0,0,121,120,1,0,0,0,122,125,
        1,0,0,0,123,121,1,0,0,0,123,124,1,0,0,0,124,126,1,0,0,0,125,123,
        1,0,0,0,126,127,3,44,22,0,127,131,5,7,0,0,128,130,5,53,0,0,129,128,
        1,0,0,0,130,133,1,0,0,0,131,129,1,0,0,0,131,132,1,0,0,0,132,134,
        1,0,0,0,133,131,1,0,0,0,134,138,3,44,22,0,135,137,5,53,0,0,136,135,
        1,0,0,0,137,140,1,0,0,0,138,136,1,0,0,0,138,139,1,0,0,0,139,141,
        1,0,0,0,140,138,1,0,0,0,141,142,5,26,0,0,142,189,1,0,0,0,143,144,
        5,6,0,0,144,148,5,27,0,0,145,147,5,53,0,0,146,145,1,0,0,0,147,150,
        1,0,0,0,148,146,1,0,0,0,148,149,1,0,0,0,149,151,1,0,0,0,150,148,
        1,0,0,0,151,160,3,44,22,0,152,156,5,30,0,0,153,155,5,53,0,0,154,
        153,1,0,0,0,155,158,1,0,0,0,156,154,1,0,0,0,156,157,1,0,0,0,157,
        159,1,0,0,0,158,156,1,0,0,0,159,161,3,44,22,0,160,152,1,0,0,0,160,
        161,1,0,0,0,161,165,1,0,0,0,162,164,5,53,0,0,163,162,1,0,0,0,164,
        167,1,0,0,0,165,163,1,0,0,0,165,166,1,0,0,0,166,168,1,0,0,0,167,
        165,1,0,0,0,168,169,5,28,0,0,169,189,1,0,0,0,170,171,5,6,0,0,171,
        175,5,25,0,0,172,174,5,53,0,0,173,172,1,0,0,0,174,177,1,0,0,0,175,
        173,1,0,0,0,175,176,1,0,0,0,176,179,1,0,0,0,177,175,1,0,0,0,178,
        180,3,42,21,0,179,178,1,0,0,0,179,180,1,0,0,0,180,184,1,0,0,0,181,
        183,5,53,0,0,182,181,1,0,0,0,183,186,1,0,0,0,184,182,1,0,0,0,184,
        185,1,0,0,0,185,187,1,0,0,0,186,184,1,0,0,0,187,189,5,26,0,0,188,
        118,1,0,0,0,188,143,1,0,0,0,188,170,1,0,0,0,189,9,1,0,0,0,190,191,
        5,32,0,0,191,192,5,49,0,0,192,194,5,45,0,0,193,195,3,12,6,0,194,
        193,1,0,0,0,194,195,1,0,0,0,195,196,1,0,0,0,196,197,5,46,0,0,197,
        11,1,0,0,0,198,203,3,14,7,0,199,200,5,30,0,0,200,202,3,14,7,0,201,
        199,1,0,0,0,202,205,1,0,0,0,203,201,1,0,0,0,203,204,1,0,0,0,204,
        13,1,0,0,0,205,203,1,0,0,0,206,207,7,2,0,0,207,15,1,0,0,0,208,210,
        3,2,1,0,209,208,1,0,0,0,210,213,1,0,0,0,211,209,1,0,0,0,211,212,
        1,0,0,0,212,17,1,0,0,0,213,211,1,0,0,0,214,215,5,8,0,0,215,216,5,
        49,0,0,216,218,5,27,0,0,217,219,3,20,10,0,218,217,1,0,0,0,218,219,
        1,0,0,0,219,220,1,0,0,0,220,221,5,28,0,0,221,223,5,29,0,0,222,224,
        5,53,0,0,223,222,1,0,0,0,224,225,1,0,0,0,225,223,1,0,0,0,225,226,
        1,0,0,0,226,227,1,0,0,0,227,228,3,16,8,0,228,229,5,15,0,0,229,230,
        5,8,0,0,230,19,1,0,0,0,231,236,3,22,11,0,232,233,5,30,0,0,233,235,
        3,22,11,0,234,232,1,0,0,0,235,238,1,0,0,0,236,234,1,0,0,0,236,237,
        1,0,0,0,237,21,1,0,0,0,238,236,1,0,0,0,239,241,3,10,5,0,240,239,
        1,0,0,0,241,244,1,0,0,0,242,240,1,0,0,0,242,243,1,0,0,0,243,245,
        1,0,0,0,244,242,1,0,0,0,245,246,5,49,0,0,246,23,1,0,0,0,247,251,
        5,9,0,0,248,250,3,10,5,0,249,248,1,0,0,0,250,253,1,0,0,0,251,249,
        1,0,0,0,251,252,1,0,0,0,252,255,1,0,0,0,253,251,1,0,0,0,254,256,
        5,27,0,0,255,254,1,0,0,0,255,256,1,0,0,0,256,257,1,0,0,0,257,258,
        5,49,0,0,258,259,5,10,0,0,259,261,5,49,0,0,260,262,5,28,0,0,261,
        260,1,0,0,0,261,262,1,0,0,0,262,263,1,0,0,0,263,265,5,29,0,0,264,
        266,5,53,0,0,265,264,1,0,0,0,266,267,1,0,0,0,267,265,1,0,0,0,267,
        268,1,0,0,0,268,269,1,0,0,0,269,270,3,16,8,0,270,271,5,15,0,0,271,
        272,5,9,0,0,272,25,1,0,0,0,273,277,5,9,0,0,274,276,3,10,5,0,275,
        274,1,0,0,0,276,279,1,0,0,0,277,275,1,0,0,0,277,278,1,0,0,0,278,
        280,1,0,0,0,279,277,1,0,0,0,280,281,5,27,0,0,281,282,3,4,2,0,282,
        283,7,3,0,0,283,284,3,44,22,0,284,285,7,3,0,0,285,286,3,4,2,0,286,
        287,5,28,0,0,287,289,5,29,0,0,288,290,5,53,0,0,289,288,1,0,0,0,290,
        291,1,0,0,0,291,289,1,0,0,0,291,292,1,0,0,0,292,293,1,0,0,0,293,
        294,3,16,8,0,294,295,5,15,0,0,295,296,5,9,0,0,296,27,1,0,0,0,297,
        299,5,16,0,0,298,300,5,27,0,0,299,298,1,0,0,0,299,300,1,0,0,0,300,
        301,1,0,0,0,301,303,3,44,22,0,302,304,5,28,0,0,303,302,1,0,0,0,303,
        304,1,0,0,0,304,305,1,0,0,0,305,307,5,29,0,0,306,308,5,53,0,0,307,
        306,1,0,0,0,308,309,1,0,0,0,309,307,1,0,0,0,309,310,1,0,0,0,310,
        311,1,0,0,0,311,312,3,16,8,0,312,313,5,15,0,0,313,314,5,16,0,0,314,
        29,1,0,0,0,315,317,5,17,0,0,316,318,5,29,0,0,317,316,1,0,0,0,317,
        318,1,0,0,0,318,320,1,0,0,0,319,321,5,53,0,0,320,319,1,0,0,0,321,
        322,1,0,0,0,322,320,1,0,0,0,322,323,1,0,0,0,323,324,1,0,0,0,324,
        325,3,16,8,0,325,326,5,16,0,0,326,327,5,27,0,0,327,328,3,44,22,0,
        328,329,5,28,0,0,329,31,1,0,0,0,330,332,5,11,0,0,331,333,5,27,0,
        0,332,331,1,0,0,0,332,333,1,0,0,0,333,334,1,0,0,0,334,336,3,44,22,
        0,335,337,5,28,0,0,336,335,1,0,0,0,336,337,1,0,0,0,337,338,1,0,0,
        0,338,340,5,29,0,0,339,341,5,53,0,0,340,339,1,0,0,0,341,342,1,0,
        0,0,342,340,1,0,0,0,342,343,1,0,0,0,343,344,1,0,0,0,344,363,3,16,
        8,0,345,347,5,13,0,0,346,348,5,27,0,0,347,346,1,0,0,0,347,348,1,
        0,0,0,348,349,1,0,0,0,349,351,3,44,22,0,350,352,5,28,0,0,351,350,
        1,0,0,0,351,352,1,0,0,0,352,353,1,0,0,0,353,355,5,29,0,0,354,356,
        5,53,0,0,355,354,1,0,0,0,356,357,1,0,0,0,357,355,1,0,0,0,357,358,
        1,0,0,0,358,359,1,0,0,0,359,360,3,16,8,0,360,362,1,0,0,0,361,345,
        1,0,0,0,362,365,1,0,0,0,363,361,1,0,0,0,363,364,1,0,0,0,364,374,
        1,0,0,0,365,363,1,0,0,0,366,367,5,12,0,0,367,369,5,29,0,0,368,370,
        5,53,0,0,369,368,1,0,0,0,370,371,1,0,0,0,371,369,1,0,0,0,371,372,
        1,0,0,0,372,373,1,0,0,0,373,375,3,16,8,0,374,366,1,0,0,0,374,375,
        1,0,0,0,375,376,1,0,0,0,376,377,5,15,0,0,377,378,5,11,0,0,378,33,
        1,0,0,0,379,380,5,49,0,0,380,382,5,27,0,0,381,383,3,42,21,0,382,
        381,1,0,0,0,382,383,1,0,0,0,383,384,1,0,0,0,384,385,5,28,0,0,385,
        35,1,0,0,0,386,388,3,10,5,0,387,386,1,0,0,0,388,391,1,0,0,0,389,
        387,1,0,0,0,389,390,1,0,0,0,390,392,1,0,0,0,391,389,1,0,0,0,392,
        393,5,14,0,0,393,394,3,44,22,0,394,37,1,0,0,0,395,396,5,18,0,0,396,
        39,1,0,0,0,397,398,5,21,0,0,398,41,1,0,0,0,399,410,3,44,22,0,400,
        404,5,30,0,0,401,403,5,53,0,0,402,401,1,0,0,0,403,406,1,0,0,0,404,
        402,1,0,0,0,404,405,1,0,0,0,405,407,1,0,0,0,406,404,1,0,0,0,407,
        409,3,44,22,0,408,400,1,0,0,0,409,412,1,0,0,0,410,408,1,0,0,0,410,
        411,1,0,0,0,411,43,1,0,0,0,412,410,1,0,0,0,413,414,3,46,23,0,414,
        45,1,0,0,0,415,420,3,48,24,0,416,417,5,20,0,0,417,419,3,48,24,0,
        418,416,1,0,0,0,419,422,1,0,0,0,420,418,1,0,0,0,420,421,1,0,0,0,
        421,47,1,0,0,0,422,420,1,0,0,0,423,428,3,50,25,0,424,425,5,19,0,
        0,425,427,3,50,25,0,426,424,1,0,0,0,427,430,1,0,0,0,428,426,1,0,
        0,0,428,429,1,0,0,0,429,49,1,0,0,0,430,428,1,0,0,0,431,436,3,52,
        26,0,432,433,7,4,0,0,433,435,3,52,26,0,434,432,1,0,0,0,435,438,1,
        0,0,0,436,434,1,0,0,0,436,437,1,0,0,0,437,51,1,0,0,0,438,436,1,0,
        0,0,439,444,3,54,27,0,440,441,7,5,0,0,441,443,3,54,27,0,442,440,
        1,0,0,0,443,446,1,0,0,0,444,442,1,0,0,0,444,445,1,0,0,0,445,53,1,
        0,0,0,446,444,1,0,0,0,447,452,3,56,28,0,448,449,7,6,0,0,449,451,
        3,56,28,0,450,448,1,0,0,0,451,454,1,0,0,0,452,450,1,0,0,0,452,453,
        1,0,0,0,453,55,1,0,0,0,454,452,1,0,0,0,455,460,3,58,29,0,456,457,
        5,40,0,0,457,459,3,58,29,0,458,456,1,0,0,0,459,462,1,0,0,0,460,458,
        1,0,0,0,460,461,1,0,0,0,461,57,1,0,0,0,462,460,1,0,0,0,463,464,5,
        39,0,0,464,467,3,58,29,0,465,467,3,60,30,0,466,463,1,0,0,0,466,465,
        1,0,0,0,467,59,1,0,0,0,468,469,5,27,0,0,469,470,3,44,22,0,470,471,
        5,28,0,0,471,485,1,0,0,0,472,473,5,49,0,0,473,475,5,27,0,0,474,476,
        3,42,21,0,475,474,1,0,0,0,475,476,1,0,0,0,476,477,1,0,0,0,477,485,
        5,28,0,0,478,479,5,49,0,0,479,480,5,25,0,0,480,481,3,44,22,0,481,
        482,5,26,0,0,482,485,1,0,0,0,483,485,3,62,31,0,484,468,1,0,0,0,484,
        472,1,0,0,0,484,478,1,0,0,0,484,483,1,0,0,0,485,61,1,0,0,0,486,487,
        7,7,0,0,487,63,1,0,0,0,59,66,68,76,90,95,101,108,116,123,131,138,
        148,156,160,165,175,179,184,188,194,203,211,218,225,236,242,251,
        255,261,267,277,291,299,303,309,317,322,332,336,342,347,351,357,
        363,371,374,382,389,404,410,420,428,436,444,452,460,466,475,484
    ]

class PseudocodeParser ( Parser ):

    grammarFileName = "Pseudocode.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'arr'", "'to'", "'fun'", 
                     "'for'", "'in'", "'if'", "'else'", "<INVALID>", "'return'", 
                     "'end'", "'while'", "'do'", "'break'", "'and'", "'or'", 
                     "'continue'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'['", "']'", "'('", "')'", "':'", "','", "';'", "'@'", 
                     "'+='", "'-='", "'='", "'=='", "'!='", "'+'", "'-'", 
                     "'**'", "'*'", "'/'", "'<='", "'>='", "'<'", "'>'", 
                     "'%'", "'%='" ]

    symbolicNames = [ "<INVALID>", "TYPE_INT", "TYPE_FLOAT", "TYPE_STRING", 
                      "TYPE_BOOL", "TYPE_DOUBLE", "ARR", "TO", "FUN", "FOR", 
                      "IN", "IF", "ELSE", "ELSEIF", "RETURN", "END", "WHILE", 
                      "DO", "BREAK", "AND", "OR", "CONTINUE", "TRUE", "FALSE", 
                      "NULL_VAL", "LBRACK", "RBRACK", "LPAREN", "RPAREN", 
                      "COLON", "COMMA", "SEMI", "AT", "PLUS_EQ", "MINUS_EQ", 
                      "EQ", "EQEQ", "NOTEQ", "PLUS", "MINUS", "POWER", "STAR", 
                      "SLASH", "LESS_EQ", "GREATER_EQ", "LT", "GT", "MOD", 
                      "MOD_EQ", "ID", "FLOAT", "INT", "STRING", "NL", "WS", 
                      "COMMENT" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_assignment = 2
    RULE_assignable = 3
    RULE_arrayInitialization = 4
    RULE_metadata = 5
    RULE_metadataParams = 6
    RULE_metadataParam = 7
    RULE_block = 8
    RULE_functionDecl = 9
    RULE_paramList = 10
    RULE_param = 11
    RULE_forEachLoop = 12
    RULE_forLoop = 13
    RULE_whileLoop = 14
    RULE_doWhileLoop = 15
    RULE_ifStatement = 16
    RULE_functionCallStmt = 17
    RULE_returnStatement = 18
    RULE_breakStatement = 19
    RULE_continueStatement = 20
    RULE_expressionList = 21
    RULE_expression = 22
    RULE_logicalOrExpression = 23
    RULE_logicalAndExpression = 24
    RULE_comparisonExpression = 25
    RULE_additiveExpression = 26
    RULE_multiplicativeExpression = 27
    RULE_powerExpression = 28
    RULE_unaryExpression = 29
    RULE_primaryExpression = 30
    RULE_atom = 31

    ruleNames =  [ "program", "statement", "assignment", "assignable", "arrayInitialization", 
                   "metadata", "metadataParams", "metadataParam", "block", 
                   "functionDecl", "paramList", "param", "forEachLoop", 
                   "forLoop", "whileLoop", "doWhileLoop", "ifStatement", 
                   "functionCallStmt", "returnStatement", "breakStatement", 
                   "continueStatement", "expressionList", "expression", 
                   "logicalOrExpression", "logicalAndExpression", "comparisonExpression", 
                   "additiveExpression", "multiplicativeExpression", "powerExpression", 
                   "unaryExpression", "primaryExpression", "atom" ]

    EOF = Token.EOF
    TYPE_INT=1
    TYPE_FLOAT=2
    TYPE_STRING=3
    TYPE_BOOL=4
    TYPE_DOUBLE=5
    ARR=6
    TO=7
    FUN=8
    FOR=9
    IN=10
    IF=11
    ELSE=12
    ELSEIF=13
    RETURN=14
    END=15
    WHILE=16
    DO=17
    BREAK=18
    AND=19
    OR=20
    CONTINUE=21
    TRUE=22
    FALSE=23
    NULL_VAL=24
    LBRACK=25
    RBRACK=26
    LPAREN=27
    RPAREN=28
    COLON=29
    COMMA=30
    SEMI=31
    AT=32
    PLUS_EQ=33
    MINUS_EQ=34
    EQ=35
    EQEQ=36
    NOTEQ=37
    PLUS=38
    MINUS=39
    POWER=40
    STAR=41
    SLASH=42
    LESS_EQ=43
    GREATER_EQ=44
    LT=45
    GT=46
    MOD=47
    MOD_EQ=48
    ID=49
    FLOAT=50
    INT=51
    STRING=52
    NL=53
    WS=54
    COMMENT=55

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(PseudocodeParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.StatementContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.StatementContext,i)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.NL)
            else:
                return self.getToken(PseudocodeParser.NL, i)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = PseudocodeParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 9570153505704704) != 0):
                self.state = 66
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [8, 9, 11, 14, 16, 17, 18, 21, 32, 49]:
                    self.state = 64
                    self.statement()
                    pass
                elif token in [53]:
                    self.state = 65
                    self.match(PseudocodeParser.NL)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 70
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 71
            self.match(PseudocodeParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment(self):
            return self.getTypedRuleContext(PseudocodeParser.AssignmentContext,0)


        def functionDecl(self):
            return self.getTypedRuleContext(PseudocodeParser.FunctionDeclContext,0)


        def functionCallStmt(self):
            return self.getTypedRuleContext(PseudocodeParser.FunctionCallStmtContext,0)


        def forEachLoop(self):
            return self.getTypedRuleContext(PseudocodeParser.ForEachLoopContext,0)


        def forLoop(self):
            return self.getTypedRuleContext(PseudocodeParser.ForLoopContext,0)


        def doWhileLoop(self):
            return self.getTypedRuleContext(PseudocodeParser.DoWhileLoopContext,0)


        def ifStatement(self):
            return self.getTypedRuleContext(PseudocodeParser.IfStatementContext,0)


        def whileLoop(self):
            return self.getTypedRuleContext(PseudocodeParser.WhileLoopContext,0)


        def returnStatement(self):
            return self.getTypedRuleContext(PseudocodeParser.ReturnStatementContext,0)


        def breakStatement(self):
            return self.getTypedRuleContext(PseudocodeParser.BreakStatementContext,0)


        def continueStatement(self):
            return self.getTypedRuleContext(PseudocodeParser.ContinueStatementContext,0)


        def metadata(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.MetadataContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.MetadataContext,i)


        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.SEMI)
            else:
                return self.getToken(PseudocodeParser.SEMI, i)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.NL)
            else:
                return self.getToken(PseudocodeParser.NL, i)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = PseudocodeParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 73
                    self.metadata() 
                self.state = 78
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

            self.state = 90
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.state = 79
                self.assignment()
                pass

            elif la_ == 2:
                self.state = 80
                self.functionDecl()
                pass

            elif la_ == 3:
                self.state = 81
                self.functionCallStmt()
                pass

            elif la_ == 4:
                self.state = 82
                self.forEachLoop()
                pass

            elif la_ == 5:
                self.state = 83
                self.forLoop()
                pass

            elif la_ == 6:
                self.state = 84
                self.doWhileLoop()
                pass

            elif la_ == 7:
                self.state = 85
                self.ifStatement()
                pass

            elif la_ == 8:
                self.state = 86
                self.whileLoop()
                pass

            elif la_ == 9:
                self.state = 87
                self.returnStatement()
                pass

            elif la_ == 10:
                self.state = 88
                self.breakStatement()
                pass

            elif la_ == 11:
                self.state = 89
                self.continueStatement()
                pass


            self.state = 95
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 92
                    _la = self._input.LA(1)
                    if not(_la==31 or _la==53):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume() 
                self.state = 97
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignable(self):
            return self.getTypedRuleContext(PseudocodeParser.AssignableContext,0)


        def EQ(self):
            return self.getToken(PseudocodeParser.EQ, 0)

        def PLUS_EQ(self):
            return self.getToken(PseudocodeParser.PLUS_EQ, 0)

        def MINUS_EQ(self):
            return self.getToken(PseudocodeParser.MINUS_EQ, 0)

        def expression(self):
            return self.getTypedRuleContext(PseudocodeParser.ExpressionContext,0)


        def arrayInitialization(self):
            return self.getTypedRuleContext(PseudocodeParser.ArrayInitializationContext,0)


        def metadata(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.MetadataContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.MetadataContext,i)


        def getRuleIndex(self):
            return PseudocodeParser.RULE_assignment

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = PseudocodeParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_assignment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 101
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32:
                self.state = 98
                self.metadata()
                self.state = 103
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 104
            self.assignable()
            self.state = 105
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 60129542144) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 108
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [22, 23, 24, 27, 39, 49, 50, 51, 52]:
                self.state = 106
                self.expression()
                pass
            elif token in [6]:
                self.state = 107
                self.arrayInitialization()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(PseudocodeParser.ID, 0)

        def LBRACK(self):
            return self.getToken(PseudocodeParser.LBRACK, 0)

        def expression(self):
            return self.getTypedRuleContext(PseudocodeParser.ExpressionContext,0)


        def RBRACK(self):
            return self.getToken(PseudocodeParser.RBRACK, 0)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_assignable

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignable" ):
                return visitor.visitAssignable(self)
            else:
                return visitor.visitChildren(self)




    def assignable(self):

        localctx = PseudocodeParser.AssignableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_assignable)
        try:
            self.state = 116
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 110
                self.match(PseudocodeParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 111
                self.match(PseudocodeParser.ID)
                self.state = 112
                self.match(PseudocodeParser.LBRACK)
                self.state = 113
                self.expression()
                self.state = 114
                self.match(PseudocodeParser.RBRACK)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayInitializationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PseudocodeParser.RULE_arrayInitialization

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class RangeArrayContext(ArrayInitializationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PseudocodeParser.ArrayInitializationContext
            super().__init__(parser)
            self.from_ = None # ExpressionContext
            self.to = None # ExpressionContext
            self.copyFrom(ctx)

        def ARR(self):
            return self.getToken(PseudocodeParser.ARR, 0)
        def LBRACK(self):
            return self.getToken(PseudocodeParser.LBRACK, 0)
        def TO(self):
            return self.getToken(PseudocodeParser.TO, 0)
        def RBRACK(self):
            return self.getToken(PseudocodeParser.RBRACK, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.ExpressionContext,i)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.NL)
            else:
                return self.getToken(PseudocodeParser.NL, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRangeArray" ):
                return visitor.visitRangeArray(self)
            else:
                return visitor.visitChildren(self)


    class ValueArrayContext(ArrayInitializationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PseudocodeParser.ArrayInitializationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ARR(self):
            return self.getToken(PseudocodeParser.ARR, 0)
        def LBRACK(self):
            return self.getToken(PseudocodeParser.LBRACK, 0)
        def RBRACK(self):
            return self.getToken(PseudocodeParser.RBRACK, 0)
        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.NL)
            else:
                return self.getToken(PseudocodeParser.NL, i)
        def expressionList(self):
            return self.getTypedRuleContext(PseudocodeParser.ExpressionListContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValueArray" ):
                return visitor.visitValueArray(self)
            else:
                return visitor.visitChildren(self)


    class SizeArrayContext(ArrayInitializationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PseudocodeParser.ArrayInitializationContext
            super().__init__(parser)
            self.size = None # ExpressionContext
            self.defaultVal = None # ExpressionContext
            self.copyFrom(ctx)

        def ARR(self):
            return self.getToken(PseudocodeParser.ARR, 0)
        def LPAREN(self):
            return self.getToken(PseudocodeParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(PseudocodeParser.RPAREN, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.ExpressionContext,i)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.NL)
            else:
                return self.getToken(PseudocodeParser.NL, i)
        def COMMA(self):
            return self.getToken(PseudocodeParser.COMMA, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSizeArray" ):
                return visitor.visitSizeArray(self)
            else:
                return visitor.visitChildren(self)



    def arrayInitialization(self):

        localctx = PseudocodeParser.ArrayInitializationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_arrayInitialization)
        self._la = 0 # Token type
        try:
            self.state = 188
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                localctx = PseudocodeParser.RangeArrayContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 118
                self.match(PseudocodeParser.ARR)
                self.state = 119
                self.match(PseudocodeParser.LBRACK)
                self.state = 123
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==53:
                    self.state = 120
                    self.match(PseudocodeParser.NL)
                    self.state = 125
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 126
                localctx.from_ = self.expression()
                self.state = 127
                self.match(PseudocodeParser.TO)
                self.state = 131
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==53:
                    self.state = 128
                    self.match(PseudocodeParser.NL)
                    self.state = 133
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 134
                localctx.to = self.expression()
                self.state = 138
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==53:
                    self.state = 135
                    self.match(PseudocodeParser.NL)
                    self.state = 140
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 141
                self.match(PseudocodeParser.RBRACK)
                pass

            elif la_ == 2:
                localctx = PseudocodeParser.SizeArrayContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 143
                self.match(PseudocodeParser.ARR)
                self.state = 144
                self.match(PseudocodeParser.LPAREN)
                self.state = 148
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==53:
                    self.state = 145
                    self.match(PseudocodeParser.NL)
                    self.state = 150
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 151
                localctx.size = self.expression()
                self.state = 160
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==30:
                    self.state = 152
                    self.match(PseudocodeParser.COMMA)
                    self.state = 156
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==53:
                        self.state = 153
                        self.match(PseudocodeParser.NL)
                        self.state = 158
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 159
                    localctx.defaultVal = self.expression()


                self.state = 165
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==53:
                    self.state = 162
                    self.match(PseudocodeParser.NL)
                    self.state = 167
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 168
                self.match(PseudocodeParser.RPAREN)
                pass

            elif la_ == 3:
                localctx = PseudocodeParser.ValueArrayContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 170
                self.match(PseudocodeParser.ARR)
                self.state = 171
                self.match(PseudocodeParser.LBRACK)
                self.state = 175
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,15,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 172
                        self.match(PseudocodeParser.NL) 
                    self.state = 177
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,15,self._ctx)

                self.state = 179
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8444799220711424) != 0):
                    self.state = 178
                    self.expressionList()


                self.state = 184
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==53:
                    self.state = 181
                    self.match(PseudocodeParser.NL)
                    self.state = 186
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 187
                self.match(PseudocodeParser.RBRACK)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MetadataContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AT(self):
            return self.getToken(PseudocodeParser.AT, 0)

        def ID(self):
            return self.getToken(PseudocodeParser.ID, 0)

        def LT(self):
            return self.getToken(PseudocodeParser.LT, 0)

        def GT(self):
            return self.getToken(PseudocodeParser.GT, 0)

        def metadataParams(self):
            return self.getTypedRuleContext(PseudocodeParser.MetadataParamsContext,0)


        def getRuleIndex(self):
            return PseudocodeParser.RULE_metadata

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMetadata" ):
                return visitor.visitMetadata(self)
            else:
                return visitor.visitChildren(self)




    def metadata(self):

        localctx = PseudocodeParser.MetadataContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_metadata)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 190
            self.match(PseudocodeParser.AT)
            self.state = 191
            self.match(PseudocodeParser.ID)
            self.state = 192
            self.match(PseudocodeParser.LT)
            self.state = 194
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8444249301319680) != 0):
                self.state = 193
                self.metadataParams()


            self.state = 196
            self.match(PseudocodeParser.GT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MetadataParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def metadataParam(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.MetadataParamContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.MetadataParamContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.COMMA)
            else:
                return self.getToken(PseudocodeParser.COMMA, i)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_metadataParams

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMetadataParams" ):
                return visitor.visitMetadataParams(self)
            else:
                return visitor.visitChildren(self)




    def metadataParams(self):

        localctx = PseudocodeParser.MetadataParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_metadataParams)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 198
            self.metadataParam()
            self.state = 203
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==30:
                self.state = 199
                self.match(PseudocodeParser.COMMA)
                self.state = 200
                self.metadataParam()
                self.state = 205
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MetadataParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(PseudocodeParser.ID, 0)

        def INT(self):
            return self.getToken(PseudocodeParser.INT, 0)

        def FLOAT(self):
            return self.getToken(PseudocodeParser.FLOAT, 0)

        def STRING(self):
            return self.getToken(PseudocodeParser.STRING, 0)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_metadataParam

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMetadataParam" ):
                return visitor.visitMetadataParam(self)
            else:
                return visitor.visitChildren(self)




    def metadataParam(self):

        localctx = PseudocodeParser.MetadataParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_metadataParam)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 206
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8444249301319680) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.StatementContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.StatementContext,i)


        def getRuleIndex(self):
            return PseudocodeParser.RULE_block

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = PseudocodeParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_block)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 211
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,21,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 208
                    self.statement() 
                self.state = 213
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,21,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUN(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.FUN)
            else:
                return self.getToken(PseudocodeParser.FUN, i)

        def ID(self):
            return self.getToken(PseudocodeParser.ID, 0)

        def LPAREN(self):
            return self.getToken(PseudocodeParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(PseudocodeParser.RPAREN, 0)

        def COLON(self):
            return self.getToken(PseudocodeParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(PseudocodeParser.BlockContext,0)


        def END(self):
            return self.getToken(PseudocodeParser.END, 0)

        def paramList(self):
            return self.getTypedRuleContext(PseudocodeParser.ParamListContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.NL)
            else:
                return self.getToken(PseudocodeParser.NL, i)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_functionDecl

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionDecl" ):
                return visitor.visitFunctionDecl(self)
            else:
                return visitor.visitChildren(self)




    def functionDecl(self):

        localctx = PseudocodeParser.FunctionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_functionDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 214
            self.match(PseudocodeParser.FUN)
            self.state = 215
            self.match(PseudocodeParser.ID)
            self.state = 216
            self.match(PseudocodeParser.LPAREN)
            self.state = 218
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==32 or _la==49:
                self.state = 217
                self.paramList()


            self.state = 220
            self.match(PseudocodeParser.RPAREN)
            self.state = 221
            self.match(PseudocodeParser.COLON)
            self.state = 223 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 222
                self.match(PseudocodeParser.NL)
                self.state = 225 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==53):
                    break

            self.state = 227
            self.block()
            self.state = 228
            self.match(PseudocodeParser.END)
            self.state = 229
            self.match(PseudocodeParser.FUN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.ParamContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.ParamContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.COMMA)
            else:
                return self.getToken(PseudocodeParser.COMMA, i)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_paramList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamList" ):
                return visitor.visitParamList(self)
            else:
                return visitor.visitChildren(self)




    def paramList(self):

        localctx = PseudocodeParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 231
            self.param()
            self.state = 236
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==30:
                self.state = 232
                self.match(PseudocodeParser.COMMA)
                self.state = 233
                self.param()
                self.state = 238
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(PseudocodeParser.ID, 0)

        def metadata(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.MetadataContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.MetadataContext,i)


        def getRuleIndex(self):
            return PseudocodeParser.RULE_param

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = PseudocodeParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 242
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32:
                self.state = 239
                self.metadata()
                self.state = 244
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 245
            self.match(PseudocodeParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForEachLoopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.FOR)
            else:
                return self.getToken(PseudocodeParser.FOR, i)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.ID)
            else:
                return self.getToken(PseudocodeParser.ID, i)

        def IN(self):
            return self.getToken(PseudocodeParser.IN, 0)

        def COLON(self):
            return self.getToken(PseudocodeParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(PseudocodeParser.BlockContext,0)


        def END(self):
            return self.getToken(PseudocodeParser.END, 0)

        def metadata(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.MetadataContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.MetadataContext,i)


        def LPAREN(self):
            return self.getToken(PseudocodeParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(PseudocodeParser.RPAREN, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.NL)
            else:
                return self.getToken(PseudocodeParser.NL, i)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_forEachLoop

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForEachLoop" ):
                return visitor.visitForEachLoop(self)
            else:
                return visitor.visitChildren(self)




    def forEachLoop(self):

        localctx = PseudocodeParser.ForEachLoopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_forEachLoop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 247
            self.match(PseudocodeParser.FOR)
            self.state = 251
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32:
                self.state = 248
                self.metadata()
                self.state = 253
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 255
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==27:
                self.state = 254
                self.match(PseudocodeParser.LPAREN)


            self.state = 257
            self.match(PseudocodeParser.ID)
            self.state = 258
            self.match(PseudocodeParser.IN)
            self.state = 259
            self.match(PseudocodeParser.ID)
            self.state = 261
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==28:
                self.state = 260
                self.match(PseudocodeParser.RPAREN)


            self.state = 263
            self.match(PseudocodeParser.COLON)
            self.state = 265 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 264
                self.match(PseudocodeParser.NL)
                self.state = 267 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==53):
                    break

            self.state = 269
            self.block()
            self.state = 270
            self.match(PseudocodeParser.END)
            self.state = 271
            self.match(PseudocodeParser.FOR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForLoopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.FOR)
            else:
                return self.getToken(PseudocodeParser.FOR, i)

        def LPAREN(self):
            return self.getToken(PseudocodeParser.LPAREN, 0)

        def assignment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.AssignmentContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.AssignmentContext,i)


        def expression(self):
            return self.getTypedRuleContext(PseudocodeParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(PseudocodeParser.RPAREN, 0)

        def COLON(self):
            return self.getToken(PseudocodeParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(PseudocodeParser.BlockContext,0)


        def END(self):
            return self.getToken(PseudocodeParser.END, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.COMMA)
            else:
                return self.getToken(PseudocodeParser.COMMA, i)

        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.SEMI)
            else:
                return self.getToken(PseudocodeParser.SEMI, i)

        def metadata(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.MetadataContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.MetadataContext,i)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.NL)
            else:
                return self.getToken(PseudocodeParser.NL, i)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_forLoop

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForLoop" ):
                return visitor.visitForLoop(self)
            else:
                return visitor.visitChildren(self)




    def forLoop(self):

        localctx = PseudocodeParser.ForLoopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_forLoop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 273
            self.match(PseudocodeParser.FOR)
            self.state = 277
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32:
                self.state = 274
                self.metadata()
                self.state = 279
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 280
            self.match(PseudocodeParser.LPAREN)
            self.state = 281
            self.assignment()
            self.state = 282
            _la = self._input.LA(1)
            if not(_la==30 or _la==31):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 283
            self.expression()
            self.state = 284
            _la = self._input.LA(1)
            if not(_la==30 or _la==31):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 285
            self.assignment()
            self.state = 286
            self.match(PseudocodeParser.RPAREN)
            self.state = 287
            self.match(PseudocodeParser.COLON)
            self.state = 289 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 288
                self.match(PseudocodeParser.NL)
                self.state = 291 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==53):
                    break

            self.state = 293
            self.block()
            self.state = 294
            self.match(PseudocodeParser.END)
            self.state = 295
            self.match(PseudocodeParser.FOR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileLoopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.WHILE)
            else:
                return self.getToken(PseudocodeParser.WHILE, i)

        def expression(self):
            return self.getTypedRuleContext(PseudocodeParser.ExpressionContext,0)


        def COLON(self):
            return self.getToken(PseudocodeParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(PseudocodeParser.BlockContext,0)


        def END(self):
            return self.getToken(PseudocodeParser.END, 0)

        def LPAREN(self):
            return self.getToken(PseudocodeParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(PseudocodeParser.RPAREN, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.NL)
            else:
                return self.getToken(PseudocodeParser.NL, i)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_whileLoop

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileLoop" ):
                return visitor.visitWhileLoop(self)
            else:
                return visitor.visitChildren(self)




    def whileLoop(self):

        localctx = PseudocodeParser.WhileLoopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_whileLoop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 297
            self.match(PseudocodeParser.WHILE)
            self.state = 299
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,32,self._ctx)
            if la_ == 1:
                self.state = 298
                self.match(PseudocodeParser.LPAREN)


            self.state = 301
            self.expression()
            self.state = 303
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==28:
                self.state = 302
                self.match(PseudocodeParser.RPAREN)


            self.state = 305
            self.match(PseudocodeParser.COLON)
            self.state = 307 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 306
                self.match(PseudocodeParser.NL)
                self.state = 309 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==53):
                    break

            self.state = 311
            self.block()
            self.state = 312
            self.match(PseudocodeParser.END)
            self.state = 313
            self.match(PseudocodeParser.WHILE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DoWhileLoopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DO(self):
            return self.getToken(PseudocodeParser.DO, 0)

        def block(self):
            return self.getTypedRuleContext(PseudocodeParser.BlockContext,0)


        def WHILE(self):
            return self.getToken(PseudocodeParser.WHILE, 0)

        def LPAREN(self):
            return self.getToken(PseudocodeParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(PseudocodeParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(PseudocodeParser.RPAREN, 0)

        def COLON(self):
            return self.getToken(PseudocodeParser.COLON, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.NL)
            else:
                return self.getToken(PseudocodeParser.NL, i)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_doWhileLoop

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoWhileLoop" ):
                return visitor.visitDoWhileLoop(self)
            else:
                return visitor.visitChildren(self)




    def doWhileLoop(self):

        localctx = PseudocodeParser.DoWhileLoopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_doWhileLoop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 315
            self.match(PseudocodeParser.DO)
            self.state = 317
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==29:
                self.state = 316
                self.match(PseudocodeParser.COLON)


            self.state = 320 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 319
                self.match(PseudocodeParser.NL)
                self.state = 322 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==53):
                    break

            self.state = 324
            self.block()
            self.state = 325
            self.match(PseudocodeParser.WHILE)
            self.state = 326
            self.match(PseudocodeParser.LPAREN)
            self.state = 327
            self.expression()
            self.state = 328
            self.match(PseudocodeParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.IF)
            else:
                return self.getToken(PseudocodeParser.IF, i)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.ExpressionContext,i)


        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.COLON)
            else:
                return self.getToken(PseudocodeParser.COLON, i)

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.BlockContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.BlockContext,i)


        def END(self):
            return self.getToken(PseudocodeParser.END, 0)

        def LPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.LPAREN)
            else:
                return self.getToken(PseudocodeParser.LPAREN, i)

        def RPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.RPAREN)
            else:
                return self.getToken(PseudocodeParser.RPAREN, i)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.NL)
            else:
                return self.getToken(PseudocodeParser.NL, i)

        def ELSEIF(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.ELSEIF)
            else:
                return self.getToken(PseudocodeParser.ELSEIF, i)

        def ELSE(self):
            return self.getToken(PseudocodeParser.ELSE, 0)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_ifStatement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStatement" ):
                return visitor.visitIfStatement(self)
            else:
                return visitor.visitChildren(self)




    def ifStatement(self):

        localctx = PseudocodeParser.IfStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_ifStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 330
            self.match(PseudocodeParser.IF)
            self.state = 332
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,37,self._ctx)
            if la_ == 1:
                self.state = 331
                self.match(PseudocodeParser.LPAREN)


            self.state = 334
            self.expression()
            self.state = 336
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==28:
                self.state = 335
                self.match(PseudocodeParser.RPAREN)


            self.state = 338
            self.match(PseudocodeParser.COLON)
            self.state = 340 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 339
                self.match(PseudocodeParser.NL)
                self.state = 342 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==53):
                    break

            self.state = 344
            self.block()
            self.state = 363
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==13:
                self.state = 345
                self.match(PseudocodeParser.ELSEIF)
                self.state = 347
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,40,self._ctx)
                if la_ == 1:
                    self.state = 346
                    self.match(PseudocodeParser.LPAREN)


                self.state = 349
                self.expression()
                self.state = 351
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==28:
                    self.state = 350
                    self.match(PseudocodeParser.RPAREN)


                self.state = 353
                self.match(PseudocodeParser.COLON)
                self.state = 355 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 354
                    self.match(PseudocodeParser.NL)
                    self.state = 357 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==53):
                        break

                self.state = 359
                self.block()
                self.state = 365
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 374
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==12:
                self.state = 366
                self.match(PseudocodeParser.ELSE)
                self.state = 367
                self.match(PseudocodeParser.COLON)
                self.state = 369 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 368
                    self.match(PseudocodeParser.NL)
                    self.state = 371 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==53):
                        break

                self.state = 373
                self.block()


            self.state = 376
            self.match(PseudocodeParser.END)
            self.state = 377
            self.match(PseudocodeParser.IF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionCallStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(PseudocodeParser.ID, 0)

        def LPAREN(self):
            return self.getToken(PseudocodeParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(PseudocodeParser.RPAREN, 0)

        def expressionList(self):
            return self.getTypedRuleContext(PseudocodeParser.ExpressionListContext,0)


        def getRuleIndex(self):
            return PseudocodeParser.RULE_functionCallStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCallStmt" ):
                return visitor.visitFunctionCallStmt(self)
            else:
                return visitor.visitChildren(self)




    def functionCallStmt(self):

        localctx = PseudocodeParser.FunctionCallStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_functionCallStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 379
            self.match(PseudocodeParser.ID)
            self.state = 380
            self.match(PseudocodeParser.LPAREN)
            self.state = 382
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8444799220711424) != 0):
                self.state = 381
                self.expressionList()


            self.state = 384
            self.match(PseudocodeParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(PseudocodeParser.RETURN, 0)

        def expression(self):
            return self.getTypedRuleContext(PseudocodeParser.ExpressionContext,0)


        def metadata(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.MetadataContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.MetadataContext,i)


        def getRuleIndex(self):
            return PseudocodeParser.RULE_returnStatement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStatement" ):
                return visitor.visitReturnStatement(self)
            else:
                return visitor.visitChildren(self)




    def returnStatement(self):

        localctx = PseudocodeParser.ReturnStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_returnStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 389
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32:
                self.state = 386
                self.metadata()
                self.state = 391
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 392
            self.match(PseudocodeParser.RETURN)
            self.state = 393
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BreakStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BREAK(self):
            return self.getToken(PseudocodeParser.BREAK, 0)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_breakStatement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreakStatement" ):
                return visitor.visitBreakStatement(self)
            else:
                return visitor.visitChildren(self)




    def breakStatement(self):

        localctx = PseudocodeParser.BreakStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_breakStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 395
            self.match(PseudocodeParser.BREAK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContinueStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONTINUE(self):
            return self.getToken(PseudocodeParser.CONTINUE, 0)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_continueStatement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinueStatement" ):
                return visitor.visitContinueStatement(self)
            else:
                return visitor.visitChildren(self)




    def continueStatement(self):

        localctx = PseudocodeParser.ContinueStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_continueStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 397
            self.match(PseudocodeParser.CONTINUE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.ExpressionContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.COMMA)
            else:
                return self.getToken(PseudocodeParser.COMMA, i)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.NL)
            else:
                return self.getToken(PseudocodeParser.NL, i)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_expressionList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpressionList" ):
                return visitor.visitExpressionList(self)
            else:
                return visitor.visitChildren(self)




    def expressionList(self):

        localctx = PseudocodeParser.ExpressionListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_expressionList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 399
            self.expression()
            self.state = 410
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==30:
                self.state = 400
                self.match(PseudocodeParser.COMMA)
                self.state = 404
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==53:
                    self.state = 401
                    self.match(PseudocodeParser.NL)
                    self.state = 406
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 407
                self.expression()
                self.state = 412
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalOrExpression(self):
            return self.getTypedRuleContext(PseudocodeParser.LogicalOrExpressionContext,0)


        def getRuleIndex(self):
            return PseudocodeParser.RULE_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = PseudocodeParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 413
            self.logicalOrExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogicalOrExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.left = None # LogicalAndExpressionContext
            self._OR = None # Token
            self.op = list() # of Tokens
            self._logicalAndExpression = None # LogicalAndExpressionContext
            self.right = list() # of LogicalAndExpressionContexts

        def logicalAndExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.LogicalAndExpressionContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.LogicalAndExpressionContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.OR)
            else:
                return self.getToken(PseudocodeParser.OR, i)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_logicalOrExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalOrExpression" ):
                return visitor.visitLogicalOrExpression(self)
            else:
                return visitor.visitChildren(self)




    def logicalOrExpression(self):

        localctx = PseudocodeParser.LogicalOrExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_logicalOrExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 415
            localctx.left = self.logicalAndExpression()
            self.state = 420
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==20:
                self.state = 416
                localctx._OR = self.match(PseudocodeParser.OR)
                localctx.op.append(localctx._OR)
                self.state = 417
                localctx._logicalAndExpression = self.logicalAndExpression()
                localctx.right.append(localctx._logicalAndExpression)
                self.state = 422
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogicalAndExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.left = None # ComparisonExpressionContext
            self._AND = None # Token
            self.op = list() # of Tokens
            self._comparisonExpression = None # ComparisonExpressionContext
            self.right = list() # of ComparisonExpressionContexts

        def comparisonExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.ComparisonExpressionContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.ComparisonExpressionContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.AND)
            else:
                return self.getToken(PseudocodeParser.AND, i)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_logicalAndExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalAndExpression" ):
                return visitor.visitLogicalAndExpression(self)
            else:
                return visitor.visitChildren(self)




    def logicalAndExpression(self):

        localctx = PseudocodeParser.LogicalAndExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_logicalAndExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 423
            localctx.left = self.comparisonExpression()
            self.state = 428
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==19:
                self.state = 424
                localctx._AND = self.match(PseudocodeParser.AND)
                localctx.op.append(localctx._AND)
                self.state = 425
                localctx._comparisonExpression = self.comparisonExpression()
                localctx.right.append(localctx._comparisonExpression)
                self.state = 430
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparisonExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PseudocodeParser.RULE_comparisonExpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class CompareExprContext(ComparisonExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PseudocodeParser.ComparisonExpressionContext
            super().__init__(parser)
            self.left = None # AdditiveExpressionContext
            self._EQEQ = None # Token
            self.op = list() # of Tokens
            self._NOTEQ = None # Token
            self._LESS_EQ = None # Token
            self._GREATER_EQ = None # Token
            self._LT = None # Token
            self._GT = None # Token
            self._tset658 = None # Token
            self._additiveExpression = None # AdditiveExpressionContext
            self.right = list() # of AdditiveExpressionContexts
            self.copyFrom(ctx)

        def additiveExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.AdditiveExpressionContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.AdditiveExpressionContext,i)

        def EQEQ(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.EQEQ)
            else:
                return self.getToken(PseudocodeParser.EQEQ, i)
        def NOTEQ(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.NOTEQ)
            else:
                return self.getToken(PseudocodeParser.NOTEQ, i)
        def LESS_EQ(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.LESS_EQ)
            else:
                return self.getToken(PseudocodeParser.LESS_EQ, i)
        def GREATER_EQ(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.GREATER_EQ)
            else:
                return self.getToken(PseudocodeParser.GREATER_EQ, i)
        def LT(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.LT)
            else:
                return self.getToken(PseudocodeParser.LT, i)
        def GT(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.GT)
            else:
                return self.getToken(PseudocodeParser.GT, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompareExpr" ):
                return visitor.visitCompareExpr(self)
            else:
                return visitor.visitChildren(self)



    def comparisonExpression(self):

        localctx = PseudocodeParser.ComparisonExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_comparisonExpression)
        self._la = 0 # Token type
        try:
            localctx = PseudocodeParser.CompareExprContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 431
            localctx.left = self.additiveExpression()
            self.state = 436
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 132147553763328) != 0):
                self.state = 432
                localctx._tset658 = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 132147553763328) != 0)):
                    localctx._tset658 = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.op.append(localctx._tset658)
                self.state = 433
                localctx._additiveExpression = self.additiveExpression()
                localctx.right.append(localctx._additiveExpression)
                self.state = 438
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditiveExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PseudocodeParser.RULE_additiveExpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class AddExprContext(AdditiveExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PseudocodeParser.AdditiveExpressionContext
            super().__init__(parser)
            self.left = None # MultiplicativeExpressionContext
            self._PLUS = None # Token
            self.op = list() # of Tokens
            self._MINUS = None # Token
            self._tset705 = None # Token
            self._multiplicativeExpression = None # MultiplicativeExpressionContext
            self.right = list() # of MultiplicativeExpressionContexts
            self.copyFrom(ctx)

        def multiplicativeExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.MultiplicativeExpressionContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.MultiplicativeExpressionContext,i)

        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.PLUS)
            else:
                return self.getToken(PseudocodeParser.PLUS, i)
        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.MINUS)
            else:
                return self.getToken(PseudocodeParser.MINUS, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddExpr" ):
                return visitor.visitAddExpr(self)
            else:
                return visitor.visitChildren(self)



    def additiveExpression(self):

        localctx = PseudocodeParser.AdditiveExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_additiveExpression)
        self._la = 0 # Token type
        try:
            localctx = PseudocodeParser.AddExprContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 439
            localctx.left = self.multiplicativeExpression()
            self.state = 444
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38 or _la==39:
                self.state = 440
                localctx._tset705 = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==38 or _la==39):
                    localctx._tset705 = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.op.append(localctx._tset705)
                self.state = 441
                localctx._multiplicativeExpression = self.multiplicativeExpression()
                localctx.right.append(localctx._multiplicativeExpression)
                self.state = 446
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicativeExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PseudocodeParser.RULE_multiplicativeExpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class MulExprContext(MultiplicativeExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PseudocodeParser.MultiplicativeExpressionContext
            super().__init__(parser)
            self.left = None # PowerExpressionContext
            self._STAR = None # Token
            self.op = list() # of Tokens
            self._SLASH = None # Token
            self._MOD = None # Token
            self._tset736 = None # Token
            self._powerExpression = None # PowerExpressionContext
            self.right = list() # of PowerExpressionContexts
            self.copyFrom(ctx)

        def powerExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.PowerExpressionContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.PowerExpressionContext,i)

        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.STAR)
            else:
                return self.getToken(PseudocodeParser.STAR, i)
        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.SLASH)
            else:
                return self.getToken(PseudocodeParser.SLASH, i)
        def MOD(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.MOD)
            else:
                return self.getToken(PseudocodeParser.MOD, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMulExpr" ):
                return visitor.visitMulExpr(self)
            else:
                return visitor.visitChildren(self)



    def multiplicativeExpression(self):

        localctx = PseudocodeParser.MultiplicativeExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_multiplicativeExpression)
        self._la = 0 # Token type
        try:
            localctx = PseudocodeParser.MulExprContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 447
            localctx.left = self.powerExpression()
            self.state = 452
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 147334558121984) != 0):
                self.state = 448
                localctx._tset736 = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 147334558121984) != 0)):
                    localctx._tset736 = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.op.append(localctx._tset736)
                self.state = 449
                localctx._powerExpression = self.powerExpression()
                localctx.right.append(localctx._powerExpression)
                self.state = 454
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PowerExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.left = None # UnaryExpressionContext
            self._POWER = None # Token
            self.op = list() # of Tokens
            self._unaryExpression = None # UnaryExpressionContext
            self.right = list() # of UnaryExpressionContexts

        def unaryExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PseudocodeParser.UnaryExpressionContext)
            else:
                return self.getTypedRuleContext(PseudocodeParser.UnaryExpressionContext,i)


        def POWER(self, i:int=None):
            if i is None:
                return self.getTokens(PseudocodeParser.POWER)
            else:
                return self.getToken(PseudocodeParser.POWER, i)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_powerExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPowerExpression" ):
                return visitor.visitPowerExpression(self)
            else:
                return visitor.visitChildren(self)




    def powerExpression(self):

        localctx = PseudocodeParser.PowerExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_powerExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 455
            localctx.left = self.unaryExpression()
            self.state = 460
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 456
                localctx._POWER = self.match(PseudocodeParser.POWER)
                localctx.op.append(localctx._POWER)
                self.state = 457
                localctx._unaryExpression = self.unaryExpression()
                localctx.right.append(localctx._unaryExpression)
                self.state = 462
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PseudocodeParser.RULE_unaryExpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class PrimaryExprContext(UnaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PseudocodeParser.UnaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def primaryExpression(self):
            return self.getTypedRuleContext(PseudocodeParser.PrimaryExpressionContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimaryExpr" ):
                return visitor.visitPrimaryExpr(self)
            else:
                return visitor.visitChildren(self)


    class UnaryMinusExprContext(UnaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PseudocodeParser.UnaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def MINUS(self):
            return self.getToken(PseudocodeParser.MINUS, 0)
        def unaryExpression(self):
            return self.getTypedRuleContext(PseudocodeParser.UnaryExpressionContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryMinusExpr" ):
                return visitor.visitUnaryMinusExpr(self)
            else:
                return visitor.visitChildren(self)



    def unaryExpression(self):

        localctx = PseudocodeParser.UnaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_unaryExpression)
        try:
            self.state = 466
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [39]:
                localctx = PseudocodeParser.UnaryMinusExprContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 463
                self.match(PseudocodeParser.MINUS)
                self.state = 464
                self.unaryExpression()
                pass
            elif token in [22, 23, 24, 27, 49, 50, 51, 52]:
                localctx = PseudocodeParser.PrimaryExprContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 465
                self.primaryExpression()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PseudocodeParser.RULE_primaryExpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ParenExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PseudocodeParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(PseudocodeParser.LPAREN, 0)
        def expression(self):
            return self.getTypedRuleContext(PseudocodeParser.ExpressionContext,0)

        def RPAREN(self):
            return self.getToken(PseudocodeParser.RPAREN, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpression" ):
                return visitor.visitParenExpression(self)
            else:
                return visitor.visitChildren(self)


    class AtomExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PseudocodeParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def atom(self):
            return self.getTypedRuleContext(PseudocodeParser.AtomContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomExpression" ):
                return visitor.visitAtomExpression(self)
            else:
                return visitor.visitChildren(self)


    class ArrayAccessExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PseudocodeParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(PseudocodeParser.ID, 0)
        def LBRACK(self):
            return self.getToken(PseudocodeParser.LBRACK, 0)
        def expression(self):
            return self.getTypedRuleContext(PseudocodeParser.ExpressionContext,0)

        def RBRACK(self):
            return self.getToken(PseudocodeParser.RBRACK, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayAccessExpression" ):
                return visitor.visitArrayAccessExpression(self)
            else:
                return visitor.visitChildren(self)


    class FunctionCallExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PseudocodeParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(PseudocodeParser.ID, 0)
        def LPAREN(self):
            return self.getToken(PseudocodeParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(PseudocodeParser.RPAREN, 0)
        def expressionList(self):
            return self.getTypedRuleContext(PseudocodeParser.ExpressionListContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCallExpression" ):
                return visitor.visitFunctionCallExpression(self)
            else:
                return visitor.visitChildren(self)



    def primaryExpression(self):

        localctx = PseudocodeParser.PrimaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_primaryExpression)
        self._la = 0 # Token type
        try:
            self.state = 484
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,58,self._ctx)
            if la_ == 1:
                localctx = PseudocodeParser.ParenExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 468
                self.match(PseudocodeParser.LPAREN)
                self.state = 469
                self.expression()
                self.state = 470
                self.match(PseudocodeParser.RPAREN)
                pass

            elif la_ == 2:
                localctx = PseudocodeParser.FunctionCallExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 472
                self.match(PseudocodeParser.ID)
                self.state = 473
                self.match(PseudocodeParser.LPAREN)
                self.state = 475
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8444799220711424) != 0):
                    self.state = 474
                    self.expressionList()


                self.state = 477
                self.match(PseudocodeParser.RPAREN)
                pass

            elif la_ == 3:
                localctx = PseudocodeParser.ArrayAccessExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 478
                self.match(PseudocodeParser.ID)
                self.state = 479
                self.match(PseudocodeParser.LBRACK)
                self.state = 480
                self.expression()
                self.state = 481
                self.match(PseudocodeParser.RBRACK)
                pass

            elif la_ == 4:
                localctx = PseudocodeParser.AtomExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 483
                self.atom()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(PseudocodeParser.ID, 0)

        def INT(self):
            return self.getToken(PseudocodeParser.INT, 0)

        def FLOAT(self):
            return self.getToken(PseudocodeParser.FLOAT, 0)

        def STRING(self):
            return self.getToken(PseudocodeParser.STRING, 0)

        def TRUE(self):
            return self.getToken(PseudocodeParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(PseudocodeParser.FALSE, 0)

        def NULL_VAL(self):
            return self.getToken(PseudocodeParser.NULL_VAL, 0)

        def getRuleIndex(self):
            return PseudocodeParser.RULE_atom

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtom" ):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)




    def atom(self):

        localctx = PseudocodeParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_atom)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 486
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8444249330679808) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





