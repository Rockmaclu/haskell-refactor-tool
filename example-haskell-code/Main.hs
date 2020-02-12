plus :: Int -> Int -> Int
plus = (+)

calculator :: Int -> Int -> IO ()
calculator a b = putStrLn $ "a+b = " ++ show (plus a b)

main = do
   calculator 1 2

