
-- |HTFDI declare variable types before assignment?

-- i can do this:
x = 2 :: Integer
-- or this
2 :: Integer
2 :: Float

-- but not this:
x :: Integer
x = 2
-- why bartosz, why???? :(
-- also cant do this
x :: Char


