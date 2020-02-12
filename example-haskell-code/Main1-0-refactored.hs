lastFunction :: Int -> Int -> Int
lastFunction 1 2 = 10
lastFunction 2 3 = 20
lastFunction 3 4 = (case (1) of (value) | value * 5 <= 10 -> 5
                                        | value * 5 > 10 -> 2)
lastFunction 4 5 = (case (2) of (value) | value * 5 <= 10 -> 5
                                        | value * 5 > 10 -> 2)

penFunct :: Int -> Int
penFunct 2 = 10
penFunct 4 = lastFunction 4 5 

mediumFunction :: Int -> Int -> Int
mediumFunction 2 3 = 1
mediumFunction 3 3 = 2
mediumFunction 10 3 = penFunct 4 
 
main = do
   (putStrLn $ "a+b = " ++ show (case (1, 2) of (1, 1) -> 2
                                                (1, 2) -> mediumFunction 10 3
                                                (1, 4) -> 22
                                                (3, 3) -> 50
                                                (2, 2) -> 10
                                                (4, 4) -> 1))

