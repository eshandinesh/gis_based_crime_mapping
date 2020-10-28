import re
import datetime

geocoder={}
geocoder['house number 89 saraswati nagar new collectorate road gwalior madhya pradesh']=(78.20,26.21)
geocoder['house number 89 saraswati nagar new collectorate road gwalior']=(78.20,26.21)
geocoder['house number 89 saraswati nagar new collectorate road']=(78.20,26.21)
geocoder['house number 89 saraswati nagar']=(78.20,26.21)
geocoder['house number 1 model town new sirol road new collectorate gwalior madhya pradesh']=(78.2107057272421,26.1950998980701)
geocoder['house number 1 model town new sirol road new collectorate gwalior ']=(78.2107057272421,26.1950998980701)
geocoder['house number 1 model town new sirol road new collectorate']=(78.2107057272421,26.1950998980701)
geocoder['house number 1 model town new sirol road']=(78.2107057272421,26.1950998980701)
geocoder['house number 1 model town new new collectorate']=(78.2107057272421,26.1950998980701)
geocoder['house number 1 model town']=(78.2107057272421,26.1950998980701)
geocoder['house number 2 model town new sirol road new collectorate gwalior madhya pradesh']=(78.2109524904715,26.1951966479539)
geocoder['house number 2 model town new sirol road new collectorate gwalior']=(78.2109524904715,26.1951966479539)
geocoder['house number 2 model town new sirol road new collectorate']=(78.2109524904715,26.1951966479539)
geocoder['house number 2 model town new sirol road']=(78.2109524904715,26.1951966479539)
geocoder['house number 2 model town new new collectorate']=(78.2109524904715,26.1951966479539)
geocoder['house number 2 model town']=(78.2109524904715,26.1951966479539)
geocoder['house number 3 model town new sirol road new collectorate gwalior madhya pradesh']=(78.2106091677176,26.1953622319721)
geocoder['house number 3 model town new sirol road new collectorate gwalior ']=(78.2106091677176,26.1953622319721)
geocoder['house number 3 model town new sirol road new collectorate']=(78.2106091677176,26.1953622319721)
geocoder['house number 3 model town new sirol road']=(78.2106091677176,26.1953622319721)
geocoder['house number 3 model town new new collectorate']=(78.2106091677176,26.1953622319721)
geocoder['house number 3 model town']=(78.2106091677176,26.1953622319721)
geocoder['house number 4 model town new sirol road new collectorate gwalior madhya pradesh']=(78.2109498082625,26.1951436997993)
geocoder['house number 4 model town new sirol road new collectorate gwalior ']=(78.2109498082625,26.1951436997993)
geocoder['house number 4 model town new sirol road new collectorate']=(78.2109498082625,26.1951436997993)
geocoder['house number 4 model town new sirol road']=(78.2109498082625,26.1951436997993)
geocoder['house number 4 model town new new collectorate']=(78.2109498082625,26.1951436997993)
geocoder['house number 4 model town']=(78.2109498082625,26.1951436997993)
geocoder['house number 5 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2109296916949,26.1950763112039)
geocoder['house number 5 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2109296916949,26.1950763112039)
geocoder['house number 5 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2109296916949,26.1950763112039)
geocoder['house number 5 MODEL TOWN NEW SIROL ROAD']=(78.2109296916949,26.1950763112039)
geocoder['house number 5 MODEL TOWN NEW COLLECTORATE']=(78.2109296916949,26.1950763112039)
geocoder['house number 5 MODEL TOWN']=(78.2109296916949,26.1950763112039)
geocoder['house number 6 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2109149395453,26.1950281764691)
geocoder['house number 6 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2109149395453,26.1950281764691)
geocoder['house number 6 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2109149395453,26.1950281764691)
geocoder['house number 6 MODEL TOWN NEW SIROL ROAD']=(78.2109149395453,26.1950281764691)
geocoder['house number 6 MODEL TOWN NEW COLLECTORATE']=(78.2109149395453,26.1950281764691)
geocoder['house number 6 MODEL TOWN']=(78.2109149395453,26.1950281764691)
geocoder['house number 7 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2109068929182,26.1949776349761)
geocoder['house number 7 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2109068929182,26.1949776349761)
geocoder['house number 7 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2109068929182,26.1949776349761)
geocoder['house number 7 MODEL TOWN NEW SIROL ROAD']=(78.2109068929182,26.1949776349761)
geocoder['house number 7 MODEL TOWN NEW COLLECTORATE']=(78.2109068929182,26.1949776349761)
geocoder['house number 7 MODEL TOWN']=(78.2109068929182,26.1949776349761)
geocoder['house number 8 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2109068929182,26.1949776349761)
geocoder['house number 8 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2109068929182,26.1949776349761)
geocoder['house number 8 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2109068929182,26.1949776349761)
geocoder['house number 8 MODEL TOWN NEW SIROL ROAD']=(78.2109068929182,26.1949776349761)
geocoder['house number 8 MODEL TOWN NEW COLLECTORATE']=(78.2109068929182,26.1949776349761)
geocoder['house number 8 MODEL TOWN']=(78.2109068929182,26.1949776349761)
geocoder['house number 9 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2109068929182,26.1949776349761)
geocoder['house number 9 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2109068929182,26.1949776349761)
geocoder['house number 9 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2109068929182,26.1949776349761)
geocoder['house number 9 MODEL TOWN NEW SIROL ROAD']=(78.2109068929182,26.1949776349761)
geocoder['house number 9 MODEL TOWN NEW COLLECTORATE']=(78.2109068929182,26.1949776349761)
geocoder['house number 9 MODEL TOWN']=(78.2109068929182,26.1949776349761)
geocoder['house number 10 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2107057272421,26.1950998980701)
geocoder['house number 10 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2107057272421,26.1950998980701)
geocoder['house number 10 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2107057272421,26.1950998980701)
geocoder['house number 10 MODEL TOWN NEW SIROL ROAD']=(78.2107057272421,26.1950998980701)
geocoder['house number 10 MODEL TOWN NEW COLLECTORATE']=(78.2107057272421,26.1950998980701)
geocoder['house number 10 MODEL TOWN']=(78.2107057272421,26.1950998980701)
geocoder['house number 11 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2108465432154,26.1947826890121)
geocoder['house number 11 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2108465432154,26.1947826890121)
geocoder['house number 11 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2108465432154,26.1947826890121)
geocoder['house number 11 MODEL TOWN NEW SIROL ROAD']=(78.2108465432154,26.1947826890121)
geocoder['house number 11 MODEL TOWN NEW COLLECTORATE']=(78.2108465432154,26.1947826890121)
geocoder['house number 11 MODEL TOWN']=(78.2108465432154,26.1947826890121)
geocoder['house number 12 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2108398376929,26.1947345541559)
geocoder['house number 12 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2108398376929,26.1947345541559)
geocoder['house number 12 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2108398376929,26.1947345541559)
geocoder['house number 12 MODEL TOWN NEW SIROL ROAD']=(78.2108398376929,26.1947345541559)
geocoder['house number 12 MODEL TOWN NEW COLLECTORATE']=(78.2108398376929,26.1947345541559)
geocoder['house number 12 MODEL TOWN']=(78.2108398376929,26.1947345541559)
geocoder['house number 13 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2108331321703,26.1946828091633)
geocoder['house number 13 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2108331321703,26.1946828091633)
geocoder['house number 13 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2108331321703,26.1946828091633)
geocoder['house number 13 MODEL TOWN NEW SIROL ROAD']=(78.2108331321703,26.1946828091633)
geocoder['house number 13 MODEL TOWN NEW COLLECTORATE']=(78.2108331321703,26.1946828091633)
geocoder['house number 13 MODEL TOWN']=(78.2108331321703,26.1946828091633)
geocoder['house number 14 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2108210622298,26.1946262506568)
geocoder['house number 14 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2108210622298,26.1946262506568)
geocoder['house number 14 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2108210622298,26.1946262506568)
geocoder['house number 14 MODEL TOWN NEW SIROL ROAD']=(78.2108210622298,26.1946262506568)
geocoder['house number 14 MODEL TOWN NEW COLLECTORATE']=(78.2108210622298,26.1946262506568)
geocoder['house number 14 MODEL TOWN']=(78.2108210622298,26.1946262506568)
geocoder['house number 15 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2107888757216,26.1945841326021)
geocoder['house number 15 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2107888757216,26.1945841326021)
geocoder['house number 15 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2107888757216,26.1945841326021)
geocoder['house number 15 MODEL TOWN NEW SIROL ROAD']=(78.2107888757216,26.1945841326021)
geocoder['house number 15 MODEL TOWN NEW COLLECTORATE']=(78.2107888757216,26.1945841326021)
geocoder['house number 15 MODEL TOWN']=(78.2107888757216,26.1945841326021)
geocoder['house number 16 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2110879420267,26.1952435792527)
geocoder['house number 16 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2110879420267,26.1952435792527)
geocoder['house number 16 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2110879420267,26.1952435792527)
geocoder['house number 16 MODEL TOWN NEW SIROL ROAD']=(78.2110879420267,26.1952435792527)
geocoder['house number 16 MODEL TOWN NEW COLLECTORATE']=(78.2110879420267,26.1952435792527)
geocoder['house number 16 MODEL TOWN']=(78.2110879420267,26.1952435792527)
geocoder['house number 17 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2110638021456,26.1951870210185)
geocoder['house number 17 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2110638021456,26.1951870210185)
geocoder['house number 17 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2110638021456,26.1951870210185)
geocoder['house number 17 MODEL TOWN NEW SIROL ROAD']=(78.2110638021456,26.1951870210185)
geocoder['house number 17 MODEL TOWN NEW COLLECTORATE']=(78.2110638021456,26.1951870210185)
geocoder['house number 17 MODEL TOWN']=(78.2110638021456,26.1951870210185)
geocoder['house number 18 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.211051732205,26.1951172257129)
geocoder['house number 18 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.211051732205,26.1951172257129)
geocoder['house number 18 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.211051732205,26.1951172257129)
geocoder['house number 18 MODEL TOWN NEW SIROL ROAD']=(78.211051732205,26.1951172257129)
geocoder['house number 18 MODEL TOWN NEW COLLECTORATE']=(78.211051732205,26.1951172257129)
geocoder['house number 18 MODEL TOWN']=(78.211051732205,26.1951172257129)
geocoder['house number 19 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2110302745329,26.1950510404706)
geocoder['house number 19 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2110302745329,26.1950510404706)
geocoder['house number 19 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2110302745329,26.1950510404706)
geocoder['house number 19 MODEL TOWN NEW SIROL ROAD']=(78.2110302745329,26.1950510404706)
geocoder['house number 19 MODEL TOWN NEW COLLECTORATE']=(78.2110302745329,26.1950510404706)
geocoder['house number 19 MODEL TOWN']=(78.2110302745329,26.1950510404706)
geocoder['house number 20 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2110168634878,26.1950053124631)
geocoder['house number 20 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2110168634878,26.1950053124631)
geocoder['house number 20 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2110168634878,26.1950053124631)
geocoder['house number 20 MODEL TOWN NEW SIROL ROAD']=(78.2110168634878,26.1950053124631)
geocoder['house number 20 MODEL TOWN NEW COLLECTORATE']=(78.2110168634878,26.1950053124631)
geocoder['house number 20 MODEL TOWN']=(78.2110168634878,26.1950053124631)
geocoder['house number 21 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2110088168608,26.1949595844376)
geocoder['house number 21 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2110088168608,26.1949595844376)
geocoder['house number 21 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2110088168608,26.1949595844376)
geocoder['house number 21 MODEL TOWN NEW SIROL ROAD']=(78.2110088168608,26.1949595844376)
geocoder['house number 21 MODEL TOWN NEW COLLECTORATE']=(78.2110088168608,26.1949595844376)
geocoder['house number 21 MODEL TOWN']=(78.2110088168608,26.1949595844376)
geocoder['house number 22 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2109994291292,26.1949102462847)
geocoder['house number 22 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2109994291292,26.1949102462847)
geocoder['house number 22 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2109994291292,26.1949102462847)
geocoder['house number 22 MODEL TOWN NEW SIROL ROAD']=(78.2109994291292,26.1949102462847)
geocoder['house number 22 MODEL TOWN NEW COLLECTORATE']=(78.2109994291292,26.1949102462847)
geocoder['house number 22 MODEL TOWN']=(78.2109994291292,26.1949102462847)
geocoder['house number 23 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2109793125616,26.1948621114813)
geocoder['house number 23 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2109793125616,26.1948621114813)
geocoder['house number 23 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2109793125616,26.1948621114813)
geocoder['house number 23 MODEL TOWN NEW SIROL ROAD']=(78.2109793125616,26.1948621114813)
geocoder['house number 23 MODEL TOWN NEW COLLECTORATE']=(78.2109793125616,26.1948621114813)
geocoder['house number 23 MODEL TOWN']=(78.2109793125616,26.1948621114813)
geocoder['house number 24 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2109685837256,26.1948127732871)
geocoder['house number 24 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2109685837256,26.1948127732871)
geocoder['house number 24 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2109685837256,26.1948127732871)
geocoder['house number 24 MODEL TOWN NEW SIROL ROAD']=(78.2109685837256,26.1948127732871)
geocoder['house number 24 MODEL TOWN NEW COLLECTORATE']=(78.2109685837256,26.1948127732871)
geocoder['house number 24 MODEL TOWN']=(78.2109685837256,26.1948127732871)
geocoder['house number 25 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2109551726805,26.1947610283293)
geocoder['house number 25 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2109551726805,26.1947610283293)
geocoder['house number 25 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2109551726805,26.1947610283293)
geocoder['house number 25 MODEL TOWN NEW SIROL ROAD']=(78.2109551726805,26.1947610283293)
geocoder['house number 25 MODEL TOWN NEW COLLECTORATE']=(78.2109551726805,26.1947610283293)
geocoder['house number 25 MODEL TOWN']=(78.2109551726805,26.1947610283293)
geocoder['house number 26 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.210951149367,26.1947195825193)
geocoder['house number 26 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.210951149367,26.1947195825193)
geocoder['house number 26 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.210951149367,26.1947195825193)
geocoder['house number 26 MODEL TOWN NEW SIROL ROAD']=(78.210951149367,26.1947195825193)
geocoder['house number 26 MODEL TOWN NEW COLLECTORATE']=(78.210951149367,26.1947195825193)
geocoder['house number 26 MODEL TOWN']=(78.210951149367,26.1947195825193)
geocoder['house number 27 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2109323739039,26.194658210541)
geocoder['house number 27 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2109323739039,26.194658210541)
geocoder['house number 27 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2109323739039,26.194658210541)
geocoder['house number 27 MODEL TOWN NEW SIROL ROAD']=(78.2109323739039,26.194658210541)
geocoder['house number 27 MODEL TOWN NEW COLLECTORATE']=(78.2109323739039,26.194658210541)
geocoder['house number 27 MODEL TOWN']=(78.2109323739039,26.194658210541)
geocoder['house number 28 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2109135984408,26.1945992452764)
geocoder['house number 28 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2109135984408,26.1945992452764)
geocoder['house number 28 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2109135984408,26.1945992452764)
geocoder['house number 28 MODEL TOWN NEW SIROL ROAD']=(78.2109135984408,26.1945992452764)
geocoder['house number 28 MODEL TOWN NEW COLLECTORATE']=(78.2109135984408,26.1945992452764)
geocoder['house number 28 MODEL TOWN']=(78.2109135984408,26.1945992452764)
geocoder['house number 29 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2113313085772,26.1949806350944)
geocoder['house number 29 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2113313085772,26.1949806350944)
geocoder['house number 29 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2113313085772,26.1949806350944)
geocoder['house number 29 MODEL TOWN NEW SIROL ROAD']=(78.2113313085772,26.1949806350944)
geocoder['house number 29 MODEL TOWN NEW COLLECTORATE']=(78.2113313085772,26.1949806350944)
geocoder['house number 29 MODEL TOWN']=(78.2113313085772,26.1949806350944)
geocoder['house number 30 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2113192386366,26.1949144497745)
geocoder['house number 30 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2113192386366,26.1949144497745)
geocoder['house number 30 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2113192386366,26.1949144497745)
geocoder['house number 30 MODEL TOWN NEW SIROL ROAD']=(78.2113192386366,26.1949144497745)
geocoder['house number 30 MODEL TOWN NEW COLLECTORATE']=(78.2113192386366,26.1949144497745)
geocoder['house number 30 MODEL TOWN']=(78.2113192386366,26.1949144497745)
geocoder['house number 31 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2113031453825,26.1948578913804)
geocoder['house number 31 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2113031453825,26.1948578913804)
geocoder['house number 31 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2113031453825,26.1948578913804)
geocoder['house number 31 MODEL TOWN NEW SIROL ROAD']=(78.2113031453825,26.1948578913804)
geocoder['house number 31 MODEL TOWN NEW COLLECTORATE']=(78.2113031453825,26.1948578913804)
geocoder['house number 31 MODEL TOWN']=(78.2113031453825,26.1948578913804)
geocoder['house number 32 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2112790055014,26.1948145700388)
geocoder['house number 32 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2112790055014,26.1948145700388)
geocoder['house number 32 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2112790055014,26.1948145700388)
geocoder['house number 32 MODEL TOWN NEW SIROL ROAD']=(78.2112790055014,26.1948145700388)
geocoder['house number 32 MODEL TOWN NEW COLLECTORATE']=(78.2112790055014,26.1948145700388)
geocoder['house number 32 MODEL TOWN']=(78.2112790055014,26.1948145700388)
geocoder['house number 33 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2112749821878,26.1947724520522)
geocoder['house number 33 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2112749821878,26.1947724520522)
geocoder['house number 33 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2112749821878,26.1947724520522)
geocoder['house number 33 MODEL TOWN NEW SIROL ROAD']=(78.2112749821878,26.1947724520522)
geocoder['house number 33 MODEL TOWN NEW COLLECTORATE']=(78.2112749821878,26.1947724520522)
geocoder['house number 33 MODEL TOWN']=(78.2112749821878,26.1947724520522)
geocoder['house number 34 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2112535245157,26.1947158935892)
geocoder['house number 34 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2112535245157,26.1947158935892)
geocoder['house number 34 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2112535245157,26.1947158935892)
geocoder['house number 34 MODEL TOWN NEW SIROL ROAD']=(78.2112535245157,26.1947158935892)
geocoder['house number 34 MODEL TOWN NEW COLLECTORATE']=(78.2112535245157,26.1947158935892)
geocoder['house number 34 MODEL TOWN']=(78.2112535245157,26.1947158935892)
geocoder['house number 35 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2112293846346,26.1946641485883)
geocoder['house number 35 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2112293846346,26.1946641485883)
geocoder['house number 35 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2112293846346,26.1946641485883)
geocoder['house number 35 MODEL TOWN NEW SIROL ROAD']=(78.2112293846346,26.1946641485883)
geocoder['house number 35 MODEL TOWN NEW COLLECTORATE']=(78.2112293846346,26.1946641485883)
geocoder['house number 35 MODEL TOWN']=(78.2112293846346,26.1946641485883)
geocoder['house number 36 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2111314840055,26.1946497081189)
geocoder['house number 36 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2111314840055,26.1946497081189)
geocoder['house number 36 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2111314840055,26.1946497081189)
geocoder['house number 36 MODEL TOWN NEW SIROL ROAD']=(78.2111314840055,26.1946497081189)
geocoder['house number 36 MODEL TOWN NEW COLLECTORATE']=(78.2111314840055,26.1946497081189)
geocoder['house number 36 MODEL TOWN']=(78.2111314840055,26.1946497081189)
geocoder['house number 37 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2112347490526,26.1949361104288)
geocoder['house number 37 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2112347490526,26.1949361104288)
geocoder['house number 37 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2112347490526,26.1949361104288)
geocoder['house number 37 MODEL TOWN NEW SIROL ROAD']=(78.2112347490526,26.1949361104288)
geocoder['house number 37 MODEL TOWN NEW COLLECTORATE']=(78.2112347490526,26.1949361104288)
geocoder['house number 37 MODEL TOWN']=(78.2112347490526,26.1949361104288)
geocoder['house number 38 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.2112132913805,26.1948735351943)
geocoder['house number 38 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.2112132913805,26.1948735351943)
geocoder['house number 38 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.2112132913805,26.1948735351943)
geocoder['house number 38 MODEL TOWN NEW SIROL ROAD']=(78.2112132913805,26.1948735351943)
geocoder['house number 38 MODEL TOWN NEW COLLECTORATE']=(78.2112132913805,26.1948735351943)
geocoder['house number 38 MODEL TOWN']=(78.2112132913805,26.1948735351943)
geocoder['house number 39 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR madhya pradesh']=(78.211203903649,26.1948362307116)
geocoder['house number 39 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE GWALIOR ']=(78.211203903649,26.1948362307116)
geocoder['house number 39 MODEL TOWN NEW SIROL ROAD NEW COLLECTORATE']=(78.211203903649,26.1948362307116)
geocoder['house number 39 MODEL TOWN NEW SIROL ROAD']=(78.211203903649,26.1948362307116)
geocoder['house number 39 MODEL TOWN NEW COLLECTORATE']=(78.211203903649,26.1948362307116)
geocoder['house number 39 MODEL TOWN']=(78.211203903649,26.1948362307116)


rep='model town me Theft hui hai house number 4 '

colonies=['model town','saraswati nagar','Mahesh Pura','Air Force','Army','Morar','Lalit Pura','Kashipura Morar','Sutar Pura','Shiv Nagar Goshipura','Shindia Nagar','New Colony Ghosipura','Vinay Nagar','Hathi Khana','Suraiya Pura','Tikoniya Morar','Bai Sahab Ke Pared','New Darpan Colony','Sarthak Appt','Station Bajariya','Shastri Nagar','Madhav Nagar','Vinay Nagar','Chandra Nagar Krupal Ashram Ke Samne','Ghasmandi','Nai Vasti','Aremy Cant','Bangali Colony Morar','Bhirtarwar','Siyaipura Morar','Kashipura','Sutar Pura','Singh Pur Road','Nagar Nigam','Mh Road','Teyagi Nagar Gwalior','Nibua Pura','Usha Colony','Gydha','Anand Nagar','Shabd Pratap Ashram','Kishan Bagh','Bara Gaon','Govendra Colony','Hajira','Indra Nagar','Janak Tal','Eslam Pura','Rama Ji Ka Pura','Jadhav Colony Bhodapur','Chota Bajar','Dabragao','No Mahlaa','Koteshwer Road','Ghatam Pur','Ghasmandi','Aau Khana','Gurdwara Durg','The Scindia School Fort','Charshehar Ka Naka','Soda Ka Kua','Karigaro Ki Gali','Tansen Takij Gwl','Goldaj Gwalior','Sindhiya School','Baba Kapoor Ke Pass','Kesho Bag','Lakhera Gali','Subash Puri','Shitla Puri','Lakhera Gali','Goshpura','Birla Nagar','Anaj Mandi','Shubash Nagar','Gadhai Pura','Kotawala Mohlla','Rangiyana Mohhalla','Tansen Nagar','Pachepada','Tansen Nagar','Sewanagar','Khidaki Mohhalla','Kota Mohalla','Godri Mohalla','Loha Mandi Jain Mandi','Sewa Nagar','Noorganj','New Tulsivihar','New Saket Naga','Goshpura No','Shabd Pratap Ashram','Khwaja Nagar Gwl','Charshehar Ka Naka','Ramtapura Gwl','Nurganj Gwl','Ramtapura Gwl','Bada','Jain Mandir Anand Nagar','Saf Colony','Thatipur','Gwalior','Thatipur','Madvi Nagar','Besnopuram Gwalior','Maa Vaishnopuram Gwalior','Gopal Pura','Mahendra Nagar','Vijay Nagar','Gadai Pura','Jati Ki Line','Tansen Nagar','Sanjay Nagar','Goswami Nagar','Gadai Pura','Mahesh Pura','Citycenter','Gudi Guda Ka Naka','Sudama Puri','Pragti Nagar','Resham Mil','New Colony','New Kanchmil','Aara Mill','Resham Mill','Alkapuri Colony','Maharajpura','Birla Nagar','New Coloni','Railway Colony','Aanad Nagar','Narayan Vihar','Aditya Puram','D D Nagar','Maharaj Pura','Janak Puri','Shatabdipuram','Laxmangrah','Radha Krishna Puri','Pinto Park','Aadarsh Nagar','Suraiyapura Morar','Madik Ki Got','Sukram Colony','Bhadroli','Rj Puram','Narayan Vihar','Atal Nagar','Bsf Colony','Ram Vihar','Gyatree Vihar Colony Pinto Park','City Center','Gole Ka Mandir','Darpan Colony','Govindpuri','Mits Gwalior','Kunj Bihar','Gol Pahadiya','C P Colony','Preetraj Colony','Mahal Gaon','Preetam Vihar Colony','Ganesh Colony Pinto Park','Jaderua Kala Pinto Park','Surya Vihar Colony','Hanuman Nagar','Adarshpura','Dd Nagar','Kakka Vihar','Shatabdipuram','Aditya Puram','Bhagat Singh Nagar','Beldar Pura','Nana Nagar','Astik Dev Nagar','Surya Vihar Colony','Shiv Colony','Nadi Parbtal','New Rachna Nagar','Kabi Nagar','Amaltash Colony','Vijay Laxmi Nagar','Atal Vihar','Shyam Nagar','Rachna Nagar','Vayu Nagar','Balram Nagar','Goverdhan Colony','Dharamveer Petrol Pump','Adarshpuram Colony','Murar','Ganga Nagar','Pushkar Colony','Ram Nagar','Ganga Vihar','Adarsh Nagar','Tripti Nager','Gayan Jyoti','Jhatbadipura Colony','Lakshmangar','Gayatri Vihar','Samarth Nagar','Gareduea','Vaishnavi Puram Gwl','Sapark Nagar','Jaderuakalan','New Ram Vihar Morar','Lakkad Khana','Ramdas Ghati Sunaro Ki Bagiya','Bhooteshwer Colony','Gulmohar City','Bahodapur','Banshipura','Siv Colony','Govardhan Colony','Raddhir Colony','Kalpi Brij','Nadi Paar Tal','Marimata Mahal Goan','Karmai Pawas Colony','Darpan Colony','Pinto Park','Laxmiganj','Tansen Nagar','Siddeshwar Nagar','Sainik Colony','Ashok Colony','Jagjeevan Nagar','Nadhi Par Taal','Adersh Colony','Goleka Mandir','Hanuman Nagar','Gole Ka Mandir','Narayan Vihar','Indrmadi Nagar','Pancshil Nagar','Krishna Nagar','Gobardhan Colony','Windsor Hills','Godam Basti Vivek Nagar Baraiya Wali Gali Thatipur','Birla Nagar','Kanti Nagar','Jiwaji Nagar','Dullpur','Sankuntla Puri','Shastri Nagar','Darpan Colony','Gopal Pura','Suresh Nagar Thatipur','Khalipa Colony','Nehru Colony','Basti Godam','Godam Basti','Gandhi Road','Ashok Coloni','Sidhart Nagar','Lohiya Bazar','Shinde Ki Chavani','Subhash Bada','Samadiya Collony','Chawari Bazar','Gotam Nagar','Jiwaji Nagar','City Center Gwalior','Tripati Nagar Morar','Siddeswar Nagar','Tripati Nagar Thatipur','Kabir Colony Thatipur','Shree Nagar Colony','Jhodha Nagar','Shiv Nagar','Shree Ram Colony','Jagjivan Nagar Morar','Om Nagar Morar','Galla Kothar','Sanjay Nagar Thatipur','Om Nagar Thatipur','Durakadhis Colony','Kumarpura','Bheemnagar','Gotam Pura','Badu Oar Tak','Suresh Nagar Thatipur','Sarvodya','Vivek Nagar','Nehru Collony Thatipir','Birla Nagar','New Pinto Colony','Mayur Nagar','Shakti Vihar','Fort View Colony','Jiwaji Nagar','R K Puram','Shivaji Nagar','New Jiwaji','Bhagwan Colony','Shankat Mochan Nagar','A Krishna Vihar Colony','Jyoti Nagar','B Atal Nagar','New Suresh Nagar','Ashok Colony Morar','Kevnet Wali Gali','Badbari Mohala','Dwarkdheer Colony','Koteshwer','Pnchshil Nagar','Shree Ram Colony','Gandhi Nagar','Aarab Shabh Ki Darga Morar','Shashtrinagar','Kabir Ashram Murar','Ambedkar Nagar','Gopal Pura','Om Nagar Thatipur Gwalior','Gautam Nagar','Ambedkar Nagar','Ambedkar Park','Shiv Ji Nagar','Chambal Colony','Madhav Inkalev','Suresh Nagar Thatipur','Mohan Nagar','Jiwaji Nagar','Sai Amrat Aparment','Prem Nagar','Laderi','Shashtrinagar','Kalpi Brij','Rivar View Colony','Suri Nagar','Bejal Kothi','Aazad Nagar','Kishan Puri','Naka Chandrawadi','Durga Colony','Lochan Nagar','Ramkala Nagar','Basnt Nagar','Chetak Complex','Haxer Colony Thatipur','Sindhi Colony Garam Sadak Morar Gwalior','Ramkal Nagar','Tiyagi Nagar','Singhpur Road','Tikoniya','Shivhare Colony','Nadipar Taal','Sudamapuri','Gas Mandi','Hanuman Colony','Ghasmandi','Kashipura','Prithvi Raj Marg','Parshuram Colony','Bhavati Colony','Mera','Gadai Pura','Ram Nagar','Narmada','Baradari','Ashok Colony','Sarika Nagar','Taraganj','Peepal Wali Gali Chik Santar','Kumarpura','Front Of Chick Santarsadar Bazar Morar','Sankar Pur','Anand Nagar','Mehra Colony','Chohan Pyau','Shiv Nagar','Jagjeevan Nagar','Kumar Pura','Darpan Colony','Patel Nagar','House No Sharda Vihar Near New High Court','Saya Appt University Road','Raghvendra Nagar Behind Ag Office Gwalior','A Govindpuri','Mahalgao','Gandhi Road','Thathipur','Gayatri Vihar','Darpan Colony','Mahal Gaon Karoli Mata Mandir','Naka Chandrawadani','Ganga Vihar','Jiwaji Ganj Shani Dev Mandir Ke Pass','Drp Line','Shacbd Pratap Ashram','Ravi Nagar','Ghosipura','Vinay Nagar','Kante Sahab Ka Bag','Jail Road','Fort View Colone','Urvai Gate','Gahoe Colony','Shri Vihar Colony','Khatke Sahab Ki Chatri','Khati Ghati','R P Colony','Anupam Nager','Vivekanand Colony','Balwant Nagar','New Railway Colony','Patel Nagar','Kailask Vihar City Center','Rajni Gandha Appt Green Garden','Golden Estate Behind Akashdeep Apt City Center','Gokul Appt City Center 301','F 319 Silver Estate University','Thatipur Murar','Thatipur Gram','Tansenroad','Vinayak Appt','Marimata Mahal Gao Gwalior','Naugja Road Shinde Ki Chawani','53 B Manik Vilas Colony Gwl','Kanti Nagar','Laxmanpura','New Saket Agar','Marimata Mahal Gao Gwalior','Gopalchal Parvat','Kedapati Colony Mahal Gao','Ravi Nagar','Dwarkapur','Virangana Baai','S Khushal Nagar','Padav','Shinde Ki Chawni','Kamal Singh Ka Bag','Sindha Bihar Colony','Laxman Talaiya','Shubham Complex','Defence Colony Gandhi Nagar','Aliza Bag','Kumhar Ka Mohalla','Koriyo Ka Mohhalla','Kamal Singh Ka Bag','Shinde Ki Chhawani','C B Palace Shinde Ki Chhawani','Madho Ganj','Adarsh Colony','Falka Bazar','Pardi Mohhala','Jari Pathka','Baban Payega','Kailash Talkies Ke Peechhe','Danaoli','Mochi Oli','Shekh Ki Bageeya Jiwaji Gang','Jiwaji Ganj','Falka Bazar','Chitra Takij Ke Peeche','Johari Colony Nai Sadak','Batore Wali Gali','Laxmi Ganj','Nai Sadak','Sebe Hi Goath','Johari Colony Nai Sadak','Batore Wali Gali','Bahodapur','Aptea Ki Payega','Kamal Singh Ka Baag','Jagat Khan Ki Goath','Gende Wali Sadak','Jalal Khan Ki Goath','Phalaka Bazar','Dal Bazar','Shinde Ki Chhawani','Sube Ki Goth','Bajrang Colony','Sanjay Nagar','Gol Paharia','Khatik Mohalla','Bahodapur','Ab Road Laxmi Ganj','Ekta Colony','Naya Pura','Madhav Nagar','Ayodhya Nagar Kumharo Ka Mohhala','Beldar Ka Pura','Gol Pahadiya','Harkotashir','Lalkuar Ka Pura','Navgraha Colony','Laxmi Ganj','Shriram Colony','Loh Gad','Jagrati Nagar Laxmi Gang','Shiv Nagar Tighra','Janak Puri','Beldar Pura','Girraj Colony','Shankar Colony','Harijan Colony','Ganesh Mandir','Mehandi Wali Sayed Goal Phadiya','Patankar Ka Bada','Gol Paharia','Bai Sahab Ka Bada','Shinde Ki Mandali','Jatar Sahab Ki Gali','Padav','Lele Ki Bajariya','Pattal Wali Gali Dholi Bua Ka Pul','Sath Bhai Ki Ghot','Loh Gad','Bul Bula Saroj Enter College Ke Paas Gwa','Vinay Nagar','Kamal Singh Ka Bag','Opp Modern Foudation Apna Ghar','Chandra Nagar','Mija Pur Ghans Mandi Bhodapur','Ravindra Nagar Ladehdi','Ghatam Pur','Ghasmandi','Koteshwer','Sheel Nagar','Auhakhana','Chandra Nagar Gwalior','Indra Colony Koteswar Road','Chandra Nagar','Bul Bula Saroj Enter College Ke Paas Gwa','Vinay Nagar','Kamal Singh Ka Bag','Opp Modern Foudation Apna Ghar','Chandra Nagar','Chandra Nagar','Ravindra Nagar Ladehdi','Ghatam Pur','Ghasmandi','Koteshwer','Sheel Nagar','Auhakhana','Chandra Nagar Gwalior','Indra Colony Koteswar Road','Chandra Nagar','Bharti Bua Ka Bada','Chawadi Bazar','Fadnis Ki Goth','Sutapura M H Road Ke Pichhe','Khasgi Bazar','Chatri Bazar','Janagang Road','Kadam Sahab Ki Goth','Hanuman Choraha','Pahad Gad','Laxmi Ganj','Shinde Ki Goth','Phadnis Ka Bada','Fadnis Ki Goth','Batase Wali Gali','Jagrati Nagar','Uda Ji Payaga','Doulat Ganj','Dana Oli Fozdaro Ka Mohalla','Nai Sadak','Falka Bazar','Sathe Ki Goth','Bhau Ka Bazar','Bakshi Ki Goth','Chitnish Ki Goth','Mochi Oli','Kasera Oli','Danaolli','Sarafa','Taksal Gali','Deedwana Oli Fogdaro Ka Bada','Deedwana Oli','Nehar Khana','Didwana Oli Swarna Jain Mandir','Deedwana Oli Maheswari Dharam Shala Ke Samne','Deedwana Oli Sarafa Bazar','Parakhaji Ka Bada','Daulatganj','Subhash Bada','Nai Sadak','Nadi Paar Taal Murar']

landmark=['new collectorate','vivekanand needam','gwalior collectorate office','M P C T engineering college','elixir m k city','d b city','police adhikshak e o w','sharda balgram','jiwaji university','jan mitra office','ram vatika','karoli mata temple','bijasan mata mandir','sophia homeopathic medical college','institute of tourism and management','indian post office','gwalior glory school','High court building','hanuman temple','madhuwan enclave','royal enclave','roop singh stadium','captain roop singh stadium','lakshmibai National Institute Of Physical Education','l n i p','Scindia kanya vidyalaya']

road_name=['bhind road','sagartal road','lal sadak','koteshwar road','tansen road','racecourse road','gandhi road','bus stand road','sachin tendulkar road','sirol link road','new collectorate road','sirol main road','new collectorate link road','outer circular road','behat road','jhansi road','main road','maharani laxmibai road','s k v road ','phool bagh road','kila gate road','jail road','khedapati temple road','mela road','sun city road','kalpi road','mall road','s l p road','badagaon road','battery road','bansipura road','singhpur road','shivaji road','']

city_name=['gwalior']

crime_type=['murder','rape','kidnapping','abduction','grievous hurt','dacoity','theft','causing simple & grevious injuries under Rash Driving','Causing Death by Negligence','Criminal Trespass/Burglary','Cruelty by Husband or his Relatives','Cheating','Assault on Women with intent to outrage her Modesty','Rioting','Criminal Breach of Trust','Forgery','Cyber Crime','Counterfeiting','Prevention of Corruption Act','Cheating','Crime against Children','Crime against SCs','Crime against Senior Citizens','Crime against STs','Economic Offences']

state_name=['madhya pradesh']
premise_type=['house number','flat number','shop number']


def house_num():
    house_number=[]
    for i in range(100000):
        house_number.append(str(i))
    return house_number


def colony_extractor():
    result=re.findall(r'\w+',rep)
    a=[]
    for i in range(len(result)):
        a.append(result[i])
    for i in range(len(result)):
        b = result[i]
        for j in range(len(result)):
            if i+j+1<len(result):
                b=b+' '+result[i+j+1]
                a.append(b)
    for x in range(len(a)):
        if a[x].lower() in colonies:
            return a[x]


def house_number_extractor():
    result=re.findall(r'\w+',rep)
    a=[]
    for i in range(len(result)):
        a.append(result[i])
    for i in range(len(result)):
        b = result[i]
        for j in range(len(result)):
            if i+j+1<len(result):
                b=b+' '+result[i+j+1]
                a.append(b)
    for x in range(len(a)):
        if a[x].lower() in house_num():
            return a[x]

def road_name_extractor():
    result = re.findall(r'\w+', rep)
    a = []
    for i in range(len(result)):
        a.append(result[i])
    for i in range(len(result)):
        b = result[i]
        for j in range(len(result)):
            if i + j + 1 < len(result):
                b = b + ' ' + result[i + j + 1]
                a.append(b)
    for x in range(len(a)):
        if a[x].lower() in road_name:
            return a[x]

def city_name_extractor():
    result = re.findall(r'\w+', rep)
    a = []
    for i in range(len(result)):
        a.append(result[i])
    for i in range(len(result)):
        b = result[i]
        for j in range(len(result)):
            if i + j + 1 < len(result):
                b = b + ' ' + result[i + j + 1]
                a.append(b)
    for x in range(len(a)):
        if a[x].lower() in city_name:
            return a[x]

def state_name_extractor():
    result = re.findall(r'\w+',rep)
    a = []
    for i in range(len(result)):
        a.append(result[i])
    for i in range(len(result)):
        b = result[i]
        for j in range(len(result)):
            if i + j + 1 < len(result):
                b = b + ' ' + result[i + j + 1]
                a.append(b)
    for x in range(len(a)):
        if a[x].lower() in state_name:
            return a[x]

def other_landmark_extractor():
    result = re.findall(r'\w+', rep)
    a = []
    for i in range(len(result)):
        a.append(result[i])
    for i in range(len(result)):
        b = result[i]
        for j in range(len(result)):
            if i + j + 1 < len(result):
                b = b + ' ' + result[i + j + 1]
                a.append(b)
    for x in range(len(a)):
        if a[x].lower() in landmark:
            return a[x]

def crime_name_extractor():
    result = re.findall(r'\w+',rep)
    a = []
    for i in range(len(result)):
        a.append(result[i])
    for i in range(len(result)):
        b = result[i]
        for j in range(len(result)):
            if i + j + 1 < len(result):
                b = b + ' ' + result[i + j + 1]
                a.append(b)
    for x in range(len(a)):
        if a[x].lower() in crime_type:
            return a[x]

def premise():
    result = re.findall(r'\w+',rep)
    a = []
    for i in range(len(result)):
        a.append(result[i])
    print (result)
    for i in range(len(result)):
        b = result[i]
        for j in range(len(result)):
            if i + j + 1 < len(result):
                b = b + ' ' + result[i + j + 1]
                a.append(b)
    print (a)
    for x in range(len(a)):
        if a[x].lower() in premise_type:
            return a[x]




def address():
    a=''
    pre=premise()
    colony=colony_extractor()
    house_number=house_number_extractor()
    road_name=road_name_extractor()
    city_name=city_name_extractor()
    state_name=state_name_extractor()
    landmark=other_landmark_extractor()
    l=[pre,house_number,colony,road_name,landmark,city_name,state_name]
    for i in l:
        if i ==None:
            continue
        else:
            a=a+' '+i+' '
    return a

def crime():
    crime=crime_name_extractor()
    return crime

def day_date_time():
    samay={}
    weekday = {}
    weekday['0'] = 'SUNDAY'
    weekday['1'] = 'MONDAY'
    weekday['2'] = 'TUESDAY'
    weekday['3'] = 'WEDNESDAY'
    weekday['4'] = 'THRUSDAY'
    weekday['5'] = 'FRIDAY'
    weekday['6'] = 'SATURDAY'
    now = datetime.datetime.now()
    samay['YEAR']=now.year
    samay['MONTH']=now.month
    samay['DAY']=now.day
    samay['HOUR']=now.hour
    samay['MINUTE']=now.minute
    samay['SECONDS']=now.second
    samay['MICROSECONDS']=now.microsecond
    samay['WEEKEND NAME']=weekday[now.strftime("%w")]
    return samay

def cord_extractor():
    add=' '.join(address().split())
    print(add)
    print (geocoder[add],crime())

cord_extractor()