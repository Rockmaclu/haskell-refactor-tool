oldFunction :: Int -> Int
oldFunction value
   | value * 5 <= 10 = 5
   | value * 5 > 10 = 2

lastFunction :: Int -> Int -> Int
lastFunction 1 2 = 10
lastFunction 2 3 = 20
lastFunction 3 4 = oldFunction 1
lastFunction 4 5 = oldFunction 2

penFunct :: Int -> Int
penFunct 2 = 10
penFunct 4 = lastFunction 4 5 

newFunction :: Int -> Int -> Int
newFunction 1 1 = 2
newFunction 1 2 = (case (10, 3) of (2, 3) -> 1
                                   (3, 3) -> 2
                                   (10, 3) -> penFunct 4)
newFunction 1 4 = 22
newFunction 3 3 = 50
newFunction 2 2 = 10
newFunction 4 4 = 1


calculator :: Int -> Int -> IO ()
calculator a b = putStrLn $ "a+b = " ++ show (newFunction a b)

main = do
   calculator 1 2

