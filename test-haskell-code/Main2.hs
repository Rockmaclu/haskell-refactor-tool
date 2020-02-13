oldFunction :: Int -> Int
oldFunction value
   | value * 5 <= 10 = 5
   | value * 5 > 10 = 2

lastFunction :: Int -> Int -> Int
lastFunction 1 2 = 10
lastFunction 2 3 = 20
lastFunction 3 4 = oldFunction 1
lastFunction 4 5 = oldFunction 2

branch2 :: Int -> Int
branch2 1 = 20
branch2 10 = lastFunction 1 2

penFunct :: Int -> Int
penFunct 2 = branch2 10
penFunct 3 = branch2 1
penFunct 4 = lastFunction 4 5 

mediumFunction :: Int -> Int -> Int
mediumFunction 2 3 = 1
mediumFunction 3 3 = 2
mediumFunction 10 3 = penFunct 4 
mediumFunction 50 1 = penFunct 2
 
newFunction :: Int -> Int -> Int
newFunction 1 1 = 2
newFunction 1 2 = mediumFunction 10 3
newFunction 1 4 = 22
newFunction 3 3 = 50
newFunction 2 2 = 10
newFunction 4 4 = 1
newFunction 5 5 = mediumFunction 50 1


calculator :: Int -> Int -> IO ()
calculator a b = putStrLn $ "a+b = " ++ show (newFunction a b)

main = do
   calculator 1 2

