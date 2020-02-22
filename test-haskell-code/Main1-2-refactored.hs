penFunct :: Int -> Int
penFunct 2 = 10
penFunct 4 = (case (4, 5) of (1, 2) -> 10
                             (2, 3) -> 20
                             (3, 4) -> (case (1) of (value) | value * 5 <= 10 -> 5
                                                            | value * 5 > 10 -> 2)
                             (4, 5) -> (case (2) of (value) | value * 5 <= 10 -> 5
                                                            | value * 5 > 10 -> 2)) 

mediumFunction :: Int -> Int -> Int
mediumFunction 2 3 = 1
mediumFunction 3 3 = 2
mediumFunction 10 3 = penFunct 4 
 
newFunction :: Int -> Int -> Int
newFunction 1 1 = 2
newFunction 1 2 = mediumFunction 10 3
newFunction 1 4 = 22
newFunction 3 3 = 50
newFunction 2 2 = 10
newFunction 4 4 = 1


calculator :: Int -> Int -> IO ()
calculator a b = putStrLn $ "a+b = " ++ show (newFunction a b)

main = do
   calculator 1 2

